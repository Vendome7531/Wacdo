from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.product import ProductModel
from app.schemas.product import ProductSchema

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[ProductSchema])
def read_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()

@router.post("/", response_model=ProductSchema)
def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    db_product = ProductModel(**product.dict(exclude={"id"}))
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, product_data: ProductSchema, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    
    for key, value in product_data.dict(exclude={"id"}).items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    
    db.delete(db_product)
    db.commit()
    return {"message": f"Produit {product_id} supprimé avec succès"}

