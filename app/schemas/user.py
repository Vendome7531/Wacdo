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

class UserSchema(UserBase):
    id: int

class Config:
     from_attributes = True