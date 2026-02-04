import bcrypt
from typing import Annotated  
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt

from app.database.database import get_db
from app.models.user import UserModel
from app.schemas.user import Token
from app.dependencies import SECRET_KEY, ALGORITHM


ACCESS_TOKEN_EXPIRE_MINUTES = 480

router = APIRouter(tags=["Authentification"])

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login", response_model=Token)
def login(
    username: Annotated[str, Form(description="Identifiant (email ou pseudo)")] = "", 
    password: Annotated[str, Form(description="Mot de passe sécurisé")] = "",
    db: Session = Depends(get_db)
):
    """
    **Authentification Wacdo** : Permet d'obtenir un jeton d'accès pour utiliser l'API.
    """
    # Puisqu'on met "" par défaut pour vider les cases, on vérifie manuellement
    if not username or not password:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

    user = db.query(UserModel).filter(UserModel.username == username).first()
    
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}