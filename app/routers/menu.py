from fastapi import APIRouter, Depends, HTTPException, status, Path, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil

from app.database.database import get_db
from app.models.user import UserModel
from app.schemas.menu import MenuSchema, MenuDeleteResponse  
from app.schemas.product import AvailabilityEnum
from app.controllers import menu_controller
from app.dependencies import admin_only

router = APIRouter(prefix="/menus", tags=["Menus"])

# --- LECTURE : Public ---
@router.get("/", response_model=List[MenuSchema])
def list_menus(db: Session = Depends(get_db)):
    """**Liste tous les menus** : Récupère l'ensemble des menus disponibles."""
    return menu_controller.get_all_menus(db)

# --- LECTURE D'UN MENU UNIQUE ---
@router.get("/{menu_id}", response_model=MenuSchema)
def read_menu(
    menu_id: int = Path(..., description="L'ID du menu"),
    db: Session = Depends(get_db)
):
    """**Consulter un menu** : Affiche les détails d'un menu spécifique."""
    menu = menu_controller.get_menu_by_id(db, menu_id=menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu non trouvé")
    return menu

# --- CRÉATION : Admin uniquement ---
@router.post("/", response_model=MenuSchema, status_code=status.HTTP_201_CREATED)
def create_menu(
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    is_available: AvailabilityEnum = Form(AvailabilityEnum.DISPO),
    # Saisie simplifiée par virgules
    product_ids: Optional[str] = Form(None, description="IDs des produits séparés par une virgule (ex: 1,2,3)"),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    admin: UserModel = Depends(admin_only)
):
    """**Créer un menu** : Regroupe toutes les infos en bas. Entrez les IDs produits séparés par des virgules."""
    image_url = None
    if image:
        os.makedirs("static/images", exist_ok=True)
        file_path = f"static/images/{image.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/{file_path}"

    return menu_controller.create_new_menu(
        db=db, 
        name=name, 
        description=description, 
        price=price, 
        image_url=image_url,
        is_available=is_available,
        product_ids=product_ids
    )

# --- MISE À JOUR : Admin uniquement ---
@router.put("/{menu_id}", response_model=MenuSchema)
def update_menu(
    menu_id: int = Path(..., description="L'ID du menu à modifier"),
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    is_available: Optional[AvailabilityEnum] = Form(None),
    # Saisie simplifiée par virgules regroupe avec le reste
    product_ids: Optional[str] = Form(None, description="Nouveaux IDs produits séparés par une virgule (ex: 4,5,6)"),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    admin: UserModel = Depends(admin_only)
):
    """**Modifier un menu** : L'ID est en haut, les modifications (dont les produits séparés par des virgules) sont en bas."""
    image_url = None
    if image:
        os.makedirs("static/images", exist_ok=True)
        file_path = f"static/images/{image.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/{file_path}"

    updated_menu = menu_controller.update_menu_in_db(
        db=db,
        menu_id=menu_id,
        name=name,
        description=description,
        price=price,
        image_url=image_url,
        is_available=is_available,
        product_ids=product_ids
    )
    
    if not updated_menu:
        raise HTTPException(status_code=404, detail="Menu non trouvé")
    return updated_menu

# --- SUPPRESSION ---
@router.delete("/{menu_id}", response_model=MenuDeleteResponse)
def delete_menu(
    menu_id: int = Path(..., description="L'ID du menu à supprimer"), 
    db: Session = Depends(get_db),
    admin: UserModel = Depends(admin_only)
):
    if not menu_controller.delete_menu_by_id(db, menu_id):
        raise HTTPException(status_code=404, detail="Menu non trouvé")
    return {"message": "Menu supprimé avec succès"}