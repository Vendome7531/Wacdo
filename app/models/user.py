from sqlalchemy import Column, Integer, String, Enum as SqlEnum
import enum
from app.database.database import Base
from sqlalchemy.orm import relationship

# Définition des rôles selon ta demande
class UserRole(enum.Enum):
    ADMINISTRATEUR = "administrateur"
    AGENT_ACCUEIL = "agent_accueil"
    PREPARATEUR_COMMANDE = "preparateur_commande"
    CLIENT = "client" # Optionnel, mais utile pour passer commande

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    # Le champ rôle avec une valeur par défaut
    role = Column(SqlEnum(UserRole), default=UserRole.CLIENT, nullable=False)

    orders = relationship("OrderModel", back_populates="user")