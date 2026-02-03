from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.controllers import user_controller
from app.schemas import user as user_schemas 
from app.routers.auth import admin_only, get_current_user
from app.models.user import UserModel

router = APIRouter(prefix="/users", tags=["Utilisateurs"])

# --- CREATE (Admin uniquement) ---
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schemas.UserSchema)
def register_user(user_data: user_schemas.UserCreate, db: Session = Depends(get_db), current_admin: UserModel = Depends(admin_only)):
    return user_controller.create_user(db, user_data)

# --- READ ALL (Admin uniquement) ---
@router.get("/", response_model=list[user_schemas.UserSchema])
def read_users(db: Session = Depends(get_db), current_admin: UserModel = Depends(admin_only)):
    return user_controller.get_all_users(db)

# --- READ ONE (Admin ou Soi-même) ---
@router.get("/{user_id}", response_model=user_schemas.UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    if current_user.role != "administrateur" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès interdit")
    db_user = user_controller.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_user

# --- UPDATE (Admin ou Soi-même) ---
@router.put("/{user_id}", response_model=user_schemas.UserSchema)
def update_user(user_id: int, user_data: user_schemas.UserUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    is_admin = current_user.role == "administrateur"
    if not is_admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Vous ne pouvez modifier que votre profil")
    
    update_dict = user_data.dict(exclude_unset=True)
    if not is_admin and "role" in update_dict:
        del update_dict["role"]
        
    return user_controller.update_user(db, user_id, update_dict)

# --- DELETE (Admin uniquement - Soft Delete) ---
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_admin: UserModel = Depends(admin_only)):
    success = user_controller.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"message": "Utilisateur désactivé avec succès"}

# --- REACTIVATE (Admin uniquement) ---
@router.patch("/{user_id}/activate", response_model=user_schemas.UserSchema)
def reactivate_user(user_id: int, db: Session = Depends(get_db), current_admin: UserModel = Depends(admin_only)):
    """Réactive un compte utilisateur (Admin uniquement)."""
    updated_user = user_controller.update_user(db, user_id, {"is_active": True})
    if not updated_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return updated_user