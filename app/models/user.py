from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base
import enum

# 1. Définition des rôles (Enum)
class UserRole(str, enum.Enum):
    ADMINISTRATEUR = "administrateur"
    AGENT_ACCUEIL = "agent_accueil"          
    PREPARATEUR = "preparateur_commande"

# 2. Définition du modèle de table
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # On utilise la valeur par défaut de l'Enum
    role = Column(String(50), default=UserRole.AGENT_ACCUEIL.value, nullable=False)
    
    is_active = Column(Boolean, default=True) 

    # Relation avec les commandes 
    orders = relationship("OrderModel", back_populates="user")