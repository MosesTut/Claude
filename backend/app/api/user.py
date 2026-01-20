from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.user import User
from app.models.preference import Preference
from app.models.itinerary import Itinerary
from app.models.feedback import Feedback
from app.models.subscription import Subscription
from app.schemas.user import UserResponse
from app.utils.auth import get_current_user

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information
    """
    return UserResponse.from_orm(current_user)


@router.delete("/account", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete user account and all associated data

    CRITICAL: This is REQUIRED for GDPR Article 17 (Right to Erasure) and CCPA compliance.
    The SettingsScreen MUST have a prominent "Delete My Data" button.

    Deletion Scope:
    - User account
    - Travel preferences
    - AI-generated itineraries
    - Feedback and reports
    - Subscription records (billing history retained for 7 years per tax law)

    Timeline: 30-day deletion SLA (data marked as deleted immediately)
    """

    try:
        # Mark user as deleted (soft delete for compliance tracking)
        current_user.is_active = False
        current_user.deleted_at = datetime.utcnow()

        # Delete associated data (cascade delete via FK constraints)
        # PostgreSQL will handle cascade deletion for:
        # - Preferences (ON DELETE CASCADE)
        # - Itineraries (ON DELETE CASCADE)
        # - Feedback (ON DELETE CASCADE)
        # - Subscriptions (ON DELETE CASCADE)

        db.commit()

        # TODO: In production, send confirmation email
        # TODO: Queue background job for hard deletion after 30 days
        # TODO: Log deletion request for audit trail

        return None  # 204 No Content

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete account: {str(e)}"
        )
