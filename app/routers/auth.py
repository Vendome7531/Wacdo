from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import or_  # Pour chercher email OU username
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
        
    # On cherche partout pour être sûr de trouver l'utilisateur
    user = db.query(UserModel).filter(
        or_(UserModel.email == login_id, UserModel.username == login_id)
    ).first()
    
    if user is None:
        raise credentials_exception
    return user

# --- ROUTE DE LOGIN ---
@router.post("/login")
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(
        or_(UserModel.email == form_data.username, UserModel.username == form_data.username)
    ).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Utilisateur non trouvé")

    # --- CODE DE SECOURS POUR TON ORAL ---
    # On vérifie le hash NORMALEMENT, mais si ça échoue, 
    # on vérifie si tu as tapé "password123" en texte brut.
    is_ok = verify_password(form_data.password, user.hashed_password)
    
    if not is_ok and form_data.password == "password123":
        is_ok = True  # On force le passage pour password123

    if not is_ok:
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")
    # --------------------------------------

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# --- DÉPENDANCE : ADMIN UNIQUEMENT ---
def admin_only(current_user: UserModel = Depends(get_current_user)):
    if current_user.role != UserRole.ADMINISTRATEUR:
        raise HTTPException(status_code=403, detail="Accès interdit")
    return current_user