from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.user import User
from app.models.subscription import Subscription
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.utils.auth import verify_password, get_password_hash, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account

    CRITICAL: Users must accept AI disclosure and data use terms during signup
    """

    # Validate consent checkboxes
    if not user_data.ai_disclosure_accepted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must accept the AI disclosure to continue"
        )

    if not user_data.data_use_accepted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must accept the data use terms to continue"
        )

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        display_name=user_data.display_name,
        ai_disclosure_accepted=user_data.ai_disclosure_accepted,
        data_use_accepted=user_data.data_use_accepted,
        last_login_at=datetime.utcnow()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create free tier subscription
    subscription = Subscription(
        user_id=new_user.id,
        tier="free",
        status="active"
    )
    db.add(subscription)
    db.commit()

    # Generate JWT token
    access_token = create_access_token(data={"sub": str(new_user.id)})

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.from_orm(new_user)
    )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user and return JWT token
    """

    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if account is active
    if not user.is_active or user.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive or deleted"
        )

    # Update last login timestamp
    user.last_login_at = datetime.utcnow()
    db.commit()

    # Generate JWT token
    access_token = create_access_token(data={"sub": str(user.id)})

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )
