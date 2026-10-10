"""Service de gestion du profil client."""

from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from models.user import UserModel, UserUpdate


class ProfileService:
    """Récupère et met à jour les informations du profil client."""

    def get_profile(self, db: Session, user_id: int) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.id == user_id).first()

    def update_profile(self, db: Session, user_id: int, update_data: UserUpdate) -> Optional[UserModel]:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None

        if update_data.full_name is not None:
            user.full_name = update_data.full_name
        if update_data.monthly_income is not None:
            user.monthly_income = update_data.monthly_income
        if update_data.monthly_expenses is not None:
            user.monthly_expenses = update_data.monthly_expenses
        if update_data.current_track is not None:
            user.current_track = update_data.current_track
        if update_data.advisor_share_consent is not None:
            user.advisor_share_consent = update_data.advisor_share_consent

        db.commit()
        db.refresh(user)
        return user


profile_service_instance = ProfileService()
