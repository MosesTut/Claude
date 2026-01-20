from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.preference import Preference
from app.schemas.preference import PreferenceCreate, PreferenceResponse
from app.utils.auth import get_current_user
from typing import Optional

router = APIRouter(prefix="/preferences", tags=["Preferences"])


@router.post("", response_model=PreferenceResponse, status_code=status.HTTP_201_CREATED)
async def save_preferences(
    preference_data: PreferenceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Save or update user travel preferences

    This endpoint stores the preferences collected from the PreferencesScreen.
    If preferences already exist, they are updated. Otherwise, new preferences are created.
    """

    # Check if preferences already exist
    existing_pref = db.query(Preference).filter(
        Preference.user_id == current_user.id
    ).first()

    if existing_pref:
        # Update existing preferences
        for key, value in preference_data.dict(exclude_unset=True).items():
            setattr(existing_pref, key, value)
        db.commit()
        db.refresh(existing_pref)
        return PreferenceResponse.from_orm(existing_pref)
    else:
        # Create new preferences
        new_pref = Preference(
            user_id=current_user.id,
            **preference_data.dict(exclude_unset=True)
        )
        db.add(new_pref)
        db.commit()
        db.refresh(new_pref)
        return PreferenceResponse.from_orm(new_pref)


@router.get("", response_model=Optional[PreferenceResponse])
async def get_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve user's saved travel preferences

    Returns None if no preferences have been saved yet.
    """

    preference = db.query(Preference).filter(
        Preference.user_id == current_user.id
    ).first()

    if not preference:
        return None

    return PreferenceResponse.from_orm(preference)
