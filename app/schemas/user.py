from pydantic import BaseModel, EmailStr
from typing import Optional

# Schéma pour la connexion (Login)
class UserLogin(BaseModel):
    username: str
    password: str

# Schéma pour le Token JWT
class Token(BaseModel):
    access_token: str
    token_type: str

# Schéma pour la création d'utilisateur
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str  # admin, accueil, preparation
    is_active: Optional[bool] = True

# Schéma pour la réponse (Lecture seule)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True