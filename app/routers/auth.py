from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import or_
from jose import JWTError, jwt
from datetime import datetime, timedelta

from app.database.database import get_db
from app.models.user import UserModel, UserRole 
from app.core.security import verify_password, create_access_token, SECRET_KEY, ALGORITHM

router = APIRouter(tags=["Authentification"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- RÉCUPÉRATION DE L'UTILISATEUR VIA TOKEN ---
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Session invalide ou expirée",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login_id: str = payload.get("sub")
        if login_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    # On cherche l'utilisateur par son username ou email
    user = db.query(UserModel).filter(
        or_(UserModel.email == login_id, UserModel.username == login_id)
    ).first()
    
    if user is None:
        raise credentials_exception
        
    # Sécurité supplémentaire : si le compte est inactif, on bloque l'accès aux routes
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ce compte est désactivé."
        )
        
    return user

# --- DÉPENDANCE : ADMIN UNIQUEMENT ---
def admin_only(current_user: UserModel = Depends(get_current_user)):
    if current_user.role != UserRole.ADMINISTRATEUR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès interdit : Administrateur requis."
        )
    return current_user

# --- ROUTE DE LOGIN (NETTOYÉE) ---
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Recherche de l'utilisateur
    user = db.query(UserModel).filter(
        or_(UserModel.email == form_data.username, UserModel.username == form_data.username)
    ).first()
    
    # 2. Vérification stricte du mot de passe haché 
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Vérification si le compte est actif
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ce compte a été désactivé."
        )

    # 4. Génération du Token JWT
    # On utilise le username comme identifiant unique dans le token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}