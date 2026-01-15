from sqlalchemy import Column, Integer, String, Float, Boolean
from pydantic import BaseModel
from database import Base

# C'est ici qu'on définit la table qui sera créée dans MySQL ou PostgreSQL
class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)

# 2. Le Schéma Pydantic (Le filtre de SÉCURITÉ exigé par ton sujet)
# Il vérifie que ce que l'utilisateur envoie est correct avant d'aller en base
class ProductSchema(BaseModel):
    name: str
    description: str
    price: float
    is_available: bool = True

    class Config:
        from_attributes = True