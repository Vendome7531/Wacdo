from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

# 1. Schéma pour la connexion (Login)
class UserLogin(BaseModel):
    username: str = Field(..., json_schema_extra={"example": "jdupont"}, description="Nom d'utilisateur de l'employé")
    password: str = Field(..., json_schema_extra={"example": "MonMotDePasseSecurise123"}, description="Mot de passe personnel")

# 2. Schéma pour la création d'utilisateur (Inscription)
class UserCreate(BaseModel):
    username: str = Field(..., json_schema_extra={"example": "m.martin"}, description="Identifiant unique pour le restaurant")
    email: EmailStr = Field(..., json_schema_extra={"example": "marianne.martin@wacdo.fr"}, description="Email professionnel")
    password: str = Field(..., min_length=8, json_schema_extra={"example": "Wacdo2024!"}, description="Mot de passe (8 caractères min.)")
    role: str = Field(..., json_schema_extra={"example": "preparateur_commande"}, description="Rôle : administrateur, agent_accueil ou preparateur_commande")
    is_active: Optional[bool] = Field(True, json_schema_extra={"example": True}, description="Statut initial du compte")

# 3. Schéma pour la mise à jour
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, json_schema_extra={"example": "nouveau.email@wacdo.fr"}, description="Nouvel email si changement")
    role: Optional[str] = Field(None, json_schema_extra={"example": "administrateur"}, description="Nouveau rôle si changement")
    is_active: Optional[bool] = Field(None, json_schema_extra={"example": False}, description="Désactiver ou réactiver le compte")

# 4. Schéma pour la réponse
class UserResponse(BaseModel):
    id: int = Field(..., json_schema_extra={"example": 1})
    username: str = Field(..., json_schema_extra={"example": "jdupont"})
    email: EmailStr = Field(..., json_schema_extra={"example": "jean.dupont@wacdo.fr"})
    role: str = Field(..., json_schema_extra={"example": "administrateur"})
    is_active: bool = Field(..., json_schema_extra={"example": True})

    # Nouvelle syntaxe Pydantic V2 pour remplacer class Config
    model_config = ConfigDict(from_attributes=True)

# 5. Schémas pour la sécurité et les messages
class Token(BaseModel):
    access_token: str = Field(..., description="Le jeton d'accès JWT à inclure dans le header")
    token_type: str = Field(..., json_schema_extra={"example": "bearer"})

class UserDeleteResponse(BaseModel):
    message: str = Field(..., json_schema_extra={"example": "Les accès de cet employé ont été révoqués avec succès"})