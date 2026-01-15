from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. On définit l'adresse pour MySQL
# root = utilisateur, @localhost = ton Mac, /wacdo_db = ta base
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@localhost/wacdo_db"

# 2. On crée le moteur de connexion
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. On prépare l'outil pour créer des sessions (ouvrir/fermer la connexion)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. On crée la Base dont hériteront tous tes modèles
Base = declarative_base()