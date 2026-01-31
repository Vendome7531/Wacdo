from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

# On réutilise les mêmes rôles que dans le modèle
class UserRole(str, Enum):
    ADMINISTRATEUR = "administrateur"
    AGENT_ACCUEIL = "agent_accueil"
    PREPARATEUR_COMMANDE = "preparateur_commande"
    CLIENT = "client"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.CLIENT

class UserCreate(UserBase):
    password: str # Le mot de passe qu'on reçoit à la création

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None  # Permet de changer le mot de passe
    role: Optional[UserRole] = None # Permet à un admin de changer le rôle

class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole
    is_active: bool 
    
    class Config:
        from_attributes = True

    