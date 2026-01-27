from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.product import ProductSchema, ProductCreate
# On importe nos fonctions du controller
from app.controllers.product_controller import get_all_products, create_new_product, delete_product_by_id

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[ProductSchema])
def list_products(db: Session = Depends(get_db)):
    return get_all_products(db)

@router.post("/", response_model=ProductSchema)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_new_product(db, product)

@router.delete("/{product_id}")
def remove_product(product_id: int, db: Session = Depends(get_db)):
    if not delete_product_by_id(db, product_id):
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return {"message": "Produit supprimé avec succès"}

