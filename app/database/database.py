import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. On récupère l'URL (Celle de Render sans le ?ssl_mode)
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://root:@localhost/wacdo_db"
)

# 2. Configuration spécifique pour le SSL d'Aiven
# On crée un dictionnaire d'arguments : si on est sur Aiven, on active le SSL
connect_args = {}
if "aivencloud.com" in SQLALCHEMY_DATABASE_URL:
    connect_args = {"ssl": {"ca": None}} # Ça force PyMySQL à utiliser le SSL

# 3. Création de l'engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()