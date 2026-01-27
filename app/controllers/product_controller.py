from sqlalchemy.orm import Session
from app.models.product import ProductModel
from app.schemas.product import ProductCreate

# Fonction pour lister (Read)
def get_all_products(db: Session):
    return db.query(ProductModel).all()

# Fonction pour créer (Create)
def create_new_product(db: Session, product_data: ProductCreate):
    new_product = ProductModel(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# Fonction pour supprimer (Delete)
def delete_product_by_id(db: Session, product_id: int):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return True
    return False

def update_product_info(db: Session, product_id: int, product_data: ProductCreate):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if product:
        product.name = product_data.name
        product.description = product_data.description
        product.price = product_data.price
        db.commit()
        db.refresh(product)
        return product
    return None