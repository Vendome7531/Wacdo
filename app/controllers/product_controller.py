from sqlalchemy.orm import Session
from app.models.product import ProductModel
from app.schemas.product import ProductCreate

# 1. LIRE TOUT
def get_all_products(db: Session):
    return db.query(ProductModel).all()

# 2. LIRE UN SEUL
def get_product_by_id(db: Session, product_id: int):
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()

# 3. CRÉER
def create_new_product(db: Session, product_data: ProductCreate):
    new_product = ProductModel(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        category=product_data.category,
        is_available=product_data.is_available
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# 4. MODIFIER
def update_product_info(db: Session, product_id: int, product_data: ProductCreate):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product:
        db_product.name = product_data.name
        db_product.description = product_data.description
        db_product.price = product_data.price
        db_product.category = product_data.category
        db_product.image = product_data.image
        db_product.is_available = product_data.is_available
        db.commit()
        db.refresh(db_product)
    return db_product

# 5. SUPPRIMER
def delete_product_by_id(db: Session, product_id: int):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product