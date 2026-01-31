from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.product import ProductSchema, ProductCreate, ProductUpdate
from app.controllers import product_controller
from app.routers.auth import admin_only
from app.models.user import UserModel

router = APIRouter(prefix="/products", tags=["Produits"])

# --- LECTURE : Accessible à tous (Agent, Préparateur, Admin) ---
@router.get("/", response_model=list[ProductSchema])
def list_products(db: Session = Depends(get_db)):
    """Récupère la liste de tous les produits."""
    return product_controller.get_all_products(db)

# --- CRÉATION : Admin seulement ---
@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
def add_product(
    product: ProductCreate, 
    db: Session = Depends(get_db),
    admin: UserModel = Depends(admin_only)
):
    """Ajoute un nouveau produit (Admin uniquement)."""
    return product_controller.create_new_product(db, product)

# --- MODIFICATION : Admin seulement ---
@router.put("/{product_id}", response_model=ProductSchema)
def update_product(
    product_id: int, 
    product_data: ProductUpdate, 
    db: Session = Depends(get_db),
    admin: UserModel = Depends(admin_only)
):
    """Met à jour un produit existant (Admin uniquement)."""
    updated_product = product_controller.update_product_info(db, product_id, product_data)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return updated_product

# --- SUPPRESSION : Admin seulement ---
@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def remove_product(
    product_id: int, 
    db: Session = Depends(get_db),
    admin: UserModel = Depends(admin_only)
):
    """Supprime un produit de la base (Admin uniquement)."""
    success = product_controller.delete_product_by_id(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return {"message": f"Le produit {product_id} a été supprimé avec succès"}