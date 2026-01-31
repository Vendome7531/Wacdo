from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.database.database import Base
import enum

# Si tu as un Enum pour les rôles
class UserRole(str, enum.Enum):
    ADMINISTRATEUR = "admin"
    EMPLOYE = "employe"

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYE)
    is_active = Column(Boolean, default=True) # <-- Maintenant 'Boolean' est reconnu

    # Relations
    orders = relationship("OrderModel", back_populates="user")