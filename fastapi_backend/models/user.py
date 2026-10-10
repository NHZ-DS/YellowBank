"""Modèles Utilisateur (SQLAlchemy & Pydantic)."""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from pydantic import BaseModel, EmailStr, Field

from utils import Base


# -------------------------------------------------------------
# Modèle SQLAlchemy (Table SQL Server : users)
# -------------------------------------------------------------
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), default="")
    role = Column(String(20), default="client")  # 'client', 'advisor', 'admin'
    
    # Données financières
    balance = Column(Float, default=1250.50)
    savings_balance = Column(Float, default=3200.00)
    monthly_income = Column(Float, default=2400.00)
    monthly_expenses = Column(Float, default=650.00)
    
    # Gamification & Parcours Yellow
    current_track = Column(String(30), default="courant")  # 'courant', 'pea', 'projets'
    xp_points = Column(Integer, default=50)
    level = Column(Integer, default=1)
    
    # RGPD & Consentement Conseiller
    advisor_share_consent = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# -------------------------------------------------------------
# Schémas Pydantic (Validation & API)
# -------------------------------------------------------------
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    monthly_income: Optional[float] = None
    monthly_expenses: Optional[float] = None
    current_track: Optional[str] = None
    advisor_share_consent: Optional[bool] = None


class UserOut(UserBase):
    id: int
    role: str
    balance: float
    savings_balance: float
    monthly_income: float
    monthly_expenses: float
    current_track: str
    xp_points: int
    level: int
    advisor_share_consent: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
