import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # <--- L'outil magique
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.database.database import get_db
from app.models.user import UserModel
from app.schemas.user import Token
from app.dependencies import SECRET_KEY, ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = 480

router = APIRouter(tags=["Authentification"])

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), # <--- FastAPI gère tout ici
    db: Session = Depends(get_db)
):
    """
    **Authentification OAuth2 Standard** : Utilise le bouton 'Authorize' en haut de Swagger.
    """
    # FastAPI met automatiquement ce qui est saisi dans 'username' et 'password'
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    
    if not user or not bcrypt.checkpw(form_data.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Le 'sub' (subject) du token est le username de l'utilisateur
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}