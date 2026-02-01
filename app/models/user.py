from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.database.database import Base
import enum

# Définition des rôles
class UserRole(str, enum.Enum):
    ADMINISTRATEUR = "admin"
    AGENT_ACCUEIL = "agent_accueil"          
    PREPARATEUR = "preparateur_commande"

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Enum pour le rôle
    role = Column(Enum(UserRole), default=UserRole.AGENT_ACCUEIL, nullable=False)
    
    is_active = Column(Boolean, default=True) 

    # Relation avec les commandes
    orders = relationship("OrderModel", back_populates="user")