from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.controllers import user_controller
from app.schemas import user as user_schemas
from app.dependencies import admin_only
# J'ai nettoyé les imports pour qu'ils correspondent à l'usage
from app.schemas.user import UserCreate, UserResponse, UserDeleteResponse, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Utilisateurs"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    """
    **Créer un nouvel employé** : Enregistre un utilisateur dans la base avec un rôle spécifique (admin, agent, préparateur).
    
    *Accessible uniquement par un Administrateur.*
    """
    return user_controller.create_user(db=db, user_data=user)

@router.get("/", response_model=List[UserResponse])
def read_users(
    skip: int = Query(0, description="Nombre d'utilisateurs à ignorer pour la pagination"),
    limit: int = Query(100, description="Nombre maximum d'utilisateurs à afficher"),
    db: Session = Depends(get_db)
):
    """
    **Récupérer la liste des employés** : Affiche tous les utilisateurs enregistrés dans le système.
    """
    return user_controller.get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int = Path(..., description="L'identifiant unique (ID) de l'utilisateur à consulter"),
    db: Session = Depends(get_db)
):
    """
    **Détails d'un utilisateur** : Affiche les informations complètes d'un employé spécifique via son ID.
    """
    return user_controller.get_user_by_id(db, user_id=user_id)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_data: UserUpdate, # <--- Corrigé : on utilise la classe importée
    user_id: int = Path(..., description="L'ID de l'utilisateur que vous souhaitez modifier"),
    db: Session = Depends(get_db),
    current_user = Depends(admin_only) # <--- Corrigé : pas besoin de UserModel ici
):
    """
    **Modifier un utilisateur** : Permet de mettre à jour les informations d'un employé existant.
    
    *Nécessite des droits Administrateur.*
    """
    return user_controller.update_existing_user(db, user_id, user_data)

@router.delete("/{user_id}", response_model=UserDeleteResponse)
def delete_user(
    user_id: int = Path(..., description="ID de l'utilisateur à supprimer"), # Ajout de la description
    db: Session = Depends(get_db), 
    current_user = Depends(admin_only)
):
    """
    **Supprimer un utilisateur** : Retire un employé de la base. (Admin uniquement)
    """
    if not user_controller.delete_user(db, user_id=user_id):
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    return {"message": "Les accès de cet employé ont été révoqués avec succès"}