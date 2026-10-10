"""Utilitaires transversaux pour FastAPI : Base de données MSSQL, Sécurité JWT et Calculs."""

import os
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from jose import JWTError, jwt
import hashlib

# -------------------------------------------------------------
# 1. Chargement du fichier .env depuis la racine du projet
# -------------------------------------------------------------
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
ENV_PATH = PROJECT_ROOT / ".env"

if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    load_dotenv()

# Clés secrètes & JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "yello_secret_key_default_123456")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# OpenAI
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gpt-4o-mini")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "text-embedding-3-small")

# -------------------------------------------------------------
# 2. Configuration & Connexion Base de Données (SQLite ou MSSQL)
# -------------------------------------------------------------
DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()

MSSQL_SERVER = os.getenv("MSSQL_SERVER", "localhost")
MSSQL_PORT = os.getenv("MSSQL_PORT", "1433")
MSSQL_DATABASE = os.getenv("MSSQL_DATABASE", "YELLOWBANK")
MSSQL_USER = os.getenv("MSSQL_USER", "")
MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD", "")
MSSQL_TRUSTED = os.getenv("MSSQL_TRUSTED_CONNECTION", "yes").lower() in ("yes", "true", "1")
MSSQL_DRIVER = os.getenv("MSSQL_DRIVER", "ODBC Driver 18 for SQL Server")
MSSQL_ENCRYPT = os.getenv("MSSQL_ENCRYPT", "no")
MSSQL_TRUST_CERT = os.getenv("MSSQL_TRUST_SERVER_CERTIFICATE", "yes")

Base = declarative_base()

if DB_TYPE == "sqlite":
    DB_PATH = BACKEND_DIR / "yello.db"
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    print(f"[SQLite] Base de donnees locale active : {DB_PATH.name}")
else:
    # Construction de la chaîne de connexion ODBC pour MSSQL
    if MSSQL_TRUSTED:
        odbc_str = (
            f"DRIVER={{{MSSQL_DRIVER}}};"
            f"SERVER={MSSQL_SERVER},{MSSQL_PORT};"
            f"DATABASE={MSSQL_DATABASE};"
            f"Trusted_Connection=yes;"
            f"Encrypt={MSSQL_ENCRYPT};"
            f"TrustServerCertificate={MSSQL_TRUST_CERT};"
        )
    else:
        odbc_str = (
            f"DRIVER={{{MSSQL_DRIVER}}};"
            f"SERVER={MSSQL_SERVER},{MSSQL_PORT};"
            f"DATABASE={MSSQL_DATABASE};"
            f"UID={MSSQL_USER};"
            f"PWD={MSSQL_PASSWORD};"
            f"Encrypt={MSSQL_ENCRYPT};"
            f"TrustServerCertificate={MSSQL_TRUST_CERT};"
        )

    params = urllib.parse.quote_plus(odbc_str)
    SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

    try:
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            fast_executemany=True,
            pool_pre_ping=True
        )
        with engine.connect() as conn:
            pass
        print("[MSSQL] Connexion a Microsoft SQL Server reussie.")
    except Exception as e:
        print(f"[SQL Server] Non accessible ({e}). Bascule automatique vers SQLite local.")
        DB_PATH = BACKEND_DIR / "yello.db"
        SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
        engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Générateur de session de base de données pour FastAPI Depends."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------------------------
# 3. Sécurité : Hachage & Tokens JWT
# -------------------------------------------------------------
def hash_password(password: str) -> str:
    """Hache un mot de passe avec SHA-256 et un sel interne."""
    salt = "archipel_yello_salt_2026"
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie si le mot de passe correspond au hash."""
    return hash_password(plain_password) == hashed_password


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Génère un token JWT signé."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Décode et valide un token JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# -------------------------------------------------------------
# 4. Calculs Financiers Métier
# -------------------------------------------------------------
def calculate_debt_ratio(monthly_income: float, monthly_charges: float) -> float:
    """Calcule le taux d'endettement en pourcentage (plafond HCSF : 35%)."""
    if monthly_income <= 0:
        return 0.0
    return round((monthly_charges / monthly_income) * 100, 2)


def estimate_borrowing_capacity(monthly_income: float, existing_loans: float, duration_years: int = 20, rate: float = 0.035) -> Dict[str, float]:
    """Estime la capacité d'emprunt maximale respectant le taux d'endettement légal."""
    max_monthly_payment = max(0.0, (monthly_income * 0.35) - existing_loans)
    if max_monthly_payment <= 0:
        return {"max_monthly_payment": 0.0, "total_capacity": 0.0}
    
    # Formule mensualité crédit : M = C * [r / (1 - (1+r)^-n)]
    r = rate / 12.0
    n = duration_years * 12
    if r > 0:
        total_capacity = max_monthly_payment * ((1 - (1 + r)**(-n)) / r)
    else:
        total_capacity = max_monthly_payment * n
        
    return {
        "max_monthly_payment": round(max_monthly_payment, 2),
        "total_capacity": round(total_capacity, 2),
    }
