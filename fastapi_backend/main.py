"""Point d'entrée principal de l'application FastAPI Yello (Yello)."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils import Base, engine, SessionLocal, hash_password
from models.user import UserModel
from models.mission import MissionModel, UserBadgeModel
from routers import auth_router, onboarding_router, chat_router, gamification_router, profile_router
from services.gamification_service import gamification_service_instance

# Initialisation de l'application FastAPI
app = FastAPI(
    title="🏝️ Yello — API Bancaire & IA Conversationnelle",
    description="Backend microservices pour Yello combinant SQL Server, Multi-agents RAG et Gamification.",
    version="1.0.0"
)

# Configuration CORS pour autoriser Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montage des Routeurs
app.include_router(auth_router.router)
app.include_router(onboarding_router.router)
app.include_router(chat_router.router)
app.include_router(gamification_router.router)
app.include_router(profile_router.router)


@app.on_event("startup")
def on_startup():
    """Initialise les tables dans SQL Server et insère les données de démarrage si nécessaire."""
    print("[Startup] Demarrage de l'API Yello...")
    try:
        # Création automatique des tables
        Base.metadata.create_all(bind=engine)
        print("[Startup] Schema de base de donnees synchronise.")
        
        # Initialisation d'un compte de démonstration et des missions
        db = SessionLocal()
        try:
            gamification_service_instance.initialize_default_missions(db)
            
            demo_user = db.query(UserModel).filter(UserModel.username == "demo").first()
            if not demo_user:
                demo_user = UserModel(
                    username="demo",
                    email="demo@yello.fr",
                    full_name="Alexandre Dupont",
                    hashed_password=hash_password("demo123"),
                    role="client",
                    balance=1450.80,
                    savings_balance=3500.00,
                    monthly_income=2600.00,
                    monthly_expenses=700.00,
                    current_track="courant",
                    xp_points=120,
                    level=1,
                    advisor_share_consent=True
                )
                db.add(demo_user)
                db.commit()
                db.refresh(demo_user)
                
                # Badge initial de test
                b = UserBadgeModel(
                    user_id=demo_user.id,
                    badge_name="Bienvenue a bord",
                    badge_icon="[Yello]",
                    description="A rejoint l'aventure Yello."
                )
                db.add(b)
                db.commit()
                print("[Startup] Utilisateur de demo initialise ('demo' / 'demo123').")
        finally:
            db.close()
    except Exception as e:
        print(f"[Startup] Avertissement lors de la synchronisation de la DB : {e}")


@app.get("/", tags=["Santé"])
def root():
    """Vérification de l'état de santé du backend."""
    return {
        "app": "Yello API (Yello)",
        "status": "healthy",
        "version": "1.0.0",
        "docs_url": "/docs"
    }


@app.get("/health", tags=["Santé"])
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
