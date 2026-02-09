import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. On récupère la variable d'environnement de Render
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://root:@localhost/wacdo_db"
)

# 2. Correction automatique du driver (pour transformer mysql:// en mysql+pymysql://)
if SQLALCHEMY_DATABASE_URL.startswith("mysql://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

# 3. Création du moteur de base de données
# Le paramètre pool_pre_ping=True aide à maintenir la connexion avec Aiven
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True
)

# 4. Configuration de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Classe de base pour tes modèles
Base = declarative_base()

# 6. Fonction pour récupérer la connexion (utilisée dans tes routes)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()