from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.database import get_db
from app.controllers import user_controller
from app.dependencies import admin_only
from app.models.user import UserRole
from app.schemas.user import UserResponse, UserDeleteResponse

router = APIRouter(prefix="/users", tags=["Utilisateurs"])

@router.get("/", response_model=List[UserResponse])
def read_users(
    skip: int = Query(0), 
    limit: int = Query(100), 
    db: Session = Depends(get_db),
    current_user = Depends(admin_only)  # <--- IL MANQUAIT ÇA !
):
    return user_controller.get_all_users(db, skip=skip, limit=limit)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(
    username: str = Form(..., description="Nom de l'utilisateur"),
    email: str = Form(..., description="Adresse email"),
    password: str = Form(..., description="Mot de passe"),
    role: UserRole = Form(UserRole.AGENT_ACCUEIL),
    is_active: bool = Form(True),
    db: Session = Depends(get_db),
    current_user = Depends(admin_only)
):
    """**Créer un employé** : Saisissez les infos et choisissez le rôle dans la liste."""
    return user_controller.create_new_user(db, username, email, password, role, is_active)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int = Path(...), db: Session = Depends(get_db)):
    user = user_controller.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int = Path(...),
    username: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    role: Optional[UserRole] = Form(None),
    is_active: Optional[bool] = Form(None),
    db: Session = Depends(get_db),
    current_user = Depends(admin_only)
):
    """**Modifier un employé** : Modifiez les champs souhaités via le formulaire."""
    updated = user_controller.update_user_in_db(db, user_id, username, email, password, role, is_active)
    if not updated:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return updated

@router.delete("/{user_id}", response_model=UserDeleteResponse)
def delete_user(user_id: int = Path(...), db: Session = Depends(get_db), current_user = Depends(admin_only)):
    if not user_controller.delete_user(db, user_id=user_id):
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"message": "Utilisateur désactivé avec succès"}