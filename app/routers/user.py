from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.controllers import user_controller
from app.schemas import user as user_schemas 
from app.routers.auth import admin_only
from app.models.user import UserModel

router = APIRouter(prefix="/users", tags=["Utilisateurs"])

# --- CREATE (Public ou Admin selon ton choix, ici Public pour l'inscription) ---
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schemas.UserSchema)
def register_user(user_data: user_schemas.UserCreate, db: Session = Depends(get_db)):
    """Inscrire un nouvel utilisateur."""
    return user_controller.create_user(db, user_data)

# --- READ ALL (Admin uniquement) ---
@router.get("/", response_model=list[user_schemas.UserSchema])
def read_users(
    db: Session = Depends(get_db), 
    admin: UserModel = Depends(admin_only) # <--- Sécurisé
):
    """Liste tous les utilisateurs (Admin uniquement)."""
    return user_controller.get_all_users(db)

# --- READ ONE (Public/Staff pour voir un profil) ---
@router.get("/{user_id}", response_model=user_schemas.UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Récupérer un utilisateur par son ID."""
    db_user = user_controller.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_user

# --- UPDATE (Admin uniquement pour changer les rôles par exemple) ---
@router.put("/{user_id}", response_model=user_schemas.UserSchema)
def update_user(
    user_id: int, 
    user_data: user_schemas.UserUpdate, 
    db: Session = Depends(get_db),
    admin: UserModel = Depends(admin_only) # <--- Sécurisé
):
    """Modifier un utilisateur (Admin uniquement)."""
    # .dict(exclude_unset=True) permet de ne modifier que les champs envoyés
    updated_user = user_controller.update_user(
        db, 
        user_id, 
        user_data.dict(exclude_unset=True)
    )
    if not updated_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return updated_user

# --- DELETE (Admin uniquement) ---
@router.delete("/{user_id}")
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    admin: UserModel = Depends(admin_only) # <--- Sécurisé
):
    """Supprimer un utilisateur (Admin uniquement)."""
    success = user_controller.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"message": f"Utilisateur {user_id} supprimé avec succès"}