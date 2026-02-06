from fastapi import APIRouter, Depends, HTTPException, status, Path, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil

from app.database.database import get_db
from app.models.user import UserModel
from app.schemas.product import ProductSchema, ProductDeleteResponse, AvailabilityEnum
from app.controllers import product_controller
from app.dependencies import admin_only

router = APIRouter(prefix="/products", tags=["Produits"])

# --- LECTURE : Public ---
@router.get("/", response_model=List[ProductSchema])
def list_products(db: Session = Depends(get_db)):
    """**Liste tous les menus** : Récupère l'ensemble des menus disponibles dans l'établissement."""
    return product_controller.get_all_products(db)

@router.get("/{product_id}", response_model=ProductSchema)
def read_product(
    product_id: int = Path(..., description="L'identifiant unique du produit (ex: 1 pour le Big Mac)"),
    db: Session = Depends(get_db)
):
    """**Consulter un produit** : Affiche les détails, le prix et la disponibilité d'un article spécifique via son ID."""
    product = product_controller.get_product_by_id(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product

# --- CRÉATION : Admin uniquement ---
@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    is_available: AvailabilityEnum = Form(AvailabilityEnum.DISPO),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    admin: UserModel = Depends(admin_only)
):
    """**Ajouter un produit** : Crée une nouvelle référence dans la base de données avec son image (Admin seulement)."""
    image_url = None
    if image:
        os.makedirs("static/images", exist_ok=True)
        file_path = f"static/images/{image.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/{file_path}"

    return product_controller.create_new_product(
        db=db, 
        name=name, 
        description=description, 
        price=price, 
        image_url=image_url,
        is_available=is_available
    )

# --- MISE À JOUR : Admin uniquement ---
@router.put("/{product_id}", response_model=ProductSchema)
def update_product(
    product_id: int = Path(..., description="L'ID du produit à modifier"),
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    is_available: Optional[AvailabilityEnum] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    admin: UserModel = Depends(admin_only)
):
    """**Modifier un produit** : Met à jour les informations ou la disponibilité (rupture de stock) d'un article existant."""
    image_url = None
    if image:
        os.makedirs("static/images", exist_ok=True)
        file_path = f"static/images/{image.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/{file_path}"

    updated_product = product_controller.update_product(
        db=db,
        product_id=product_id,
        name=name,
        description=description,
        price=price,
        image_url=image_url,
        is_available=is_available
    )
    
    if not updated_product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return updated_product

# --- SUPPRESSION : Admin uniquement ---
@router.delete("/{product_id}", response_model=ProductDeleteResponse)
def delete_product(
    product_id: int = Path(..., description="L'ID du produit à retirer définitivement de la carte"),
    db: Session = Depends(get_db),
    admin: UserModel = Depends(admin_only)
):
    """**Supprimer un produit** : Efface définitivement un article du catalogue."""
    if not product_controller.delete_product_by_id(db, product_id):
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return {"message": "Produit supprimé avec succès"}