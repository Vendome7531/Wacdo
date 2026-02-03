from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.controllers import user_controller
from app.schemas import user as user_schemas
from app.routers.auth import admin_only

router = APIRouter(
    prefix="/users",
    tags=["Utilisateurs"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schemas.UserResponse)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return user_controller.create_user(db=db, user_data=user)

@router.get("/", response_model=List[user_schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return user_controller.get_all_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=user_schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    db_user = user_controller.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_user

@router.put("/{user_id}", response_model=user_schemas.UserResponse)
def update_user(user_id: int, user_update: user_schemas.UserCreate, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    db_user = user_controller.update_user(db, user_id=user_id, user_update_data=user_update)
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    if not user_controller.delete_user(db, user_id=user_id):
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return None