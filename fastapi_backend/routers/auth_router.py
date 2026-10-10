"""Routeur d'Authentification (Inscription, Connexion, Tokens)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from utils import get_db, create_access_token
from models.user import UserCreate, UserLogin, UserOut, TokenResponse
from services.auth_service import auth_service_instance

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Crée un nouveau compte utilisateur dans SQL Server."""
    return auth_service_instance.register(db, user_in)


@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Authentifie l'utilisateur et délivre un token JWT."""
    user = auth_service_instance.authenticate(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects."
        )

    access_token = create_access_token(data={"sub": str(user.id), "username": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }
