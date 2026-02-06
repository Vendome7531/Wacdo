from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import UserModel, UserRole 

SECRET_KEY = "votre_cle_secrete_tres_securisee"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Session invalide ou expirée",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None: raise credentials_exception
    except JWTError: raise credentials_exception
        
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user is None: raise credentials_exception
    return user

# --- LES VERROUS ---

def admin_only(current_user: UserModel = Depends(get_current_user)):
    if current_user.role != UserRole.ADMINISTRATEUR.value:
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    return current_user

def accueil_only(current_user: UserModel = Depends(get_current_user)):
    # L'admin a aussi accès aux fonctions de l'accueil
    if current_user.role not in [UserRole.AGENT_ACCUEIL.value, UserRole.ADMINISTRATEUR.value]:
        raise HTTPException(status_code=403, detail="Accès réservé au personnel d'accueil")
    return current_user

def preparation_only(current_user: UserModel = Depends(get_current_user)):
    # L'admin a aussi accès aux fonctions de préparation
    if current_user.role not in [UserRole.PREPARATEUR.value, UserRole.ADMINISTRATEUR.value]:
        raise HTTPException(status_code=403, detail="Accès réservé au personnel de préparation")
    return current_user