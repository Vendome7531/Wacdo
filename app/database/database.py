from sqlalchemy import create_engine
# CHANGEMENT ICI : On importe declarative_base directement depuis orm
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost/wacdo_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# C'est ici que le warning disparaîtra
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


