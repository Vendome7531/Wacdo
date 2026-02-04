from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# 1. Schéma pour la connexion (Login)
class UserLogin(BaseModel):
    username: str = Field(..., example="jdupont", description="Nom d'utilisateur de l'employé")
    password: str = Field(..., example="MonMotDePasseSecurise123", description="Mot de passe personnel")

# 2. Schéma pour la création d'utilisateur (Inscription)
class UserCreate(BaseModel):
    username: str = Field(..., example="m.martin", description="Identifiant unique pour le restaurant")
    email: EmailStr = Field(..., example="marianne.martin@wacdo.fr", description="Email professionnel")
    password: str = Field(..., min_length=8, example="Wacdo2024!", description="Mot de passe (8 caractères min.)")
    role: str = Field(..., example="preparateur_commande", description="Rôle : administrateur, agent_accueil ou preparateur_commande")
    is_active: Optional[bool] = Field(True, example=True, description="Statut initial du compte")

# 3. Schéma pour la mise à jour (C'est celui qui te manquait !)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, example="nouveau.email@wacdo.fr", description="Nouvel email si changement")
    role: Optional[str] = Field(None, example="administrateur", description="Nouveau rôle si changement")
    is_active: Optional[bool] = Field(None, example=False, description="Désactiver ou réactiver le compte")

# 4. Schéma pour la réponse (Ce qui s'affiche dans Swagger après une requête)
class UserResponse(BaseModel):
    id: int = Field(..., example=1)
    username: str = Field(..., example="jdupont")
    email: EmailStr = Field(..., example="jean.dupont@wacdo.fr")
    role: str = Field(..., example="administrateur")
    is_active: bool = Field(..., example=True)

    class Config:
        from_attributes = True

# 5. Schémas pour la sécurité et les messages
class Token(BaseModel):
    access_token: str = Field(..., description="Le jeton d'accès JWT à inclure dans le header")
    token_type: str = Field(..., example="bearer")

class UserDeleteResponse(BaseModel):
    message: str = Field(..., example="Les accès de cet employé ont été révoqués avec succès")