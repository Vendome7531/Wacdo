from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Schéma pour la connexion (Login)
class UserLogin(BaseModel):
    username: str = Field(..., example="jdupont", description="Nom d'utilisateur de l'employé")
    password: str = Field(..., example="MonMotDePasseSecurise123", description="Mot de passe personnel")

# Schéma pour la création d'utilisateur (Inscription)
class UserCreate(BaseModel):
    username: str = Field(..., example="m.martin", description="Identifiant unique pour le restaurant")
    email: EmailStr = Field(..., example="marianne.martin@wacdo.fr", description="Email professionnel")
    password: str = Field(..., min_length=8, example="Wacdo2024!", description="Mot de passe (8 caractères min.)")
    role: str = Field(..., example="preparateur_commande", description="Rôle : administrateur, agent_accueil ou preparateur_commande")
    is_active: Optional[bool] = Field(True, example=True, description="Statut du compte")

# Schéma pour la réponse (Ce qui s'affiche dans Swagger)
class UserResponse(BaseModel):
    id: int = Field(..., example=1)
    username: str = Field(..., example="jdupont")
    email: EmailStr = Field(..., example="jean.dupont@wacdo.fr")
    role: str = Field(..., example="administrateur")
    is_active: bool = Field(..., example=True)

    class Config:
        from_attributes = True

# Schéma pour le Token JWT
class Token(BaseModel):
    access_token: str = Field(..., description="Le jeton d'accès à inclure dans le header Authorization")
    token_type: str = Field(..., example="bearer")

class UserDeleteResponse(BaseModel):
    message: str = Field(..., example="Les accès de cet employé ont été révoqués avec succès")