"""Service d'authentification et gestion des comptes utilisateurs."""

from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.user import UserModel, UserCreate
from utils import hash_password, verify_password, create_access_token


class AuthService:
    """Gère l'inscription, la connexion et les tokens JWT."""

    def register(self, db: Session, user_in: UserCreate) -> UserModel:
        # Vérifier si l'utilisateur existe déjà
        existing = db.query(UserModel).filter(
            (UserModel.username == user_in.username) | (UserModel.email == user_in.email)
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ce nom d'utilisateur ou cet email est déjà utilisé."
            )

        new_user = UserModel(
            username=user_in.username,
            email=user_in.email,
            full_name=user_in.full_name or user_in.username,
            hashed_password=hash_password(user_in.password),
            role="client",
            balance=1250.50,
            savings_balance=3200.00,
            current_track="courant",
            xp_points=50,
            level=1,
            advisor_share_consent=False
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def authenticate(self, db: Session, username: str, password: str) -> Optional[UserModel]:
        user = db.query(UserModel).filter(UserModel.username == username).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user


auth_service_instance = AuthService()
