from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
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
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(UserModel).filter(UserModel.email == email).first()
    
    if user is None:
        raise credentials_exception
        
    # Sécurité Soft Delete : Un utilisateur désactivé ne peut plus rien faire
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

# --- ROUTE DE LOGIN ---
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # On cherche l'utilisateur (le champ 'username' du form contient l'email ici)
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    
    # Vérification mot de passe
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Vérification si compte actif
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ce compte a été désactivé. Veuillez contacter un administrateur."
        )

    # Génération du JWT
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- UTILITAIRE : RÔLES À LA CARTE (Optionnel) ---
def role_required(allowed_roles: list[UserRole]):
    def decorator(current_user: UserModel = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissions insuffisantes."
            )
        return current_user
    return decorator