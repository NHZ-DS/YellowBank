"""Modèles de Gamification : Missions, Badges et Progression."""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from utils import Base


# -------------------------------------------------------------
# Modèles SQLAlchemy (Tables SQL Server : missions, user_missions, user_badges)
# -------------------------------------------------------------
class MissionModel(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    track = Column(String(30), nullable=False)  # 'courant', 'pea', 'projets'
    title = Column(String(150), nullable=False)
    description = Column(String(500), nullable=False)
    xp_reward = Column(Integer, default=50)
    badge_reward = Column(String(100), nullable=True)
    is_challenge = Column(Boolean, default=False)


class UserMissionModel(Base):
    __tablename__ = "user_missions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)
    status = Column(String(20), default="available")  # 'available', 'in_progress', 'completed'
    completed_at = Column(DateTime, nullable=True)


class UserBadgeModel(Base):
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    badge_name = Column(String(100), nullable=False)
    badge_icon = Column(String(100), default="🏆")
    description = Column(String(255), default="")
    unlocked_at = Column(DateTime, default=datetime.utcnow)


# -------------------------------------------------------------
# Schémas Pydantic
# -------------------------------------------------------------
class MissionOut(BaseModel):
    id: int
    track: str
    title: str
    description: str
    xp_reward: int
    badge_reward: Optional[str] = None
    is_challenge: bool
    status: str = "available"  # Statut pour l'utilisateur courant

    class Config:
        from_attributes = True


class BadgeOut(BaseModel):
    id: int
    badge_name: str
    badge_icon: str
    description: str
    unlocked_at: datetime

    class Config:
        from_attributes = True


class GamificationProfileOut(BaseModel):
    user_id: int
    xp_points: int
    level: int
    current_track: str
    badges: List[BadgeOut]
    active_missions: List[MissionOut]
    completed_missions_count: int
