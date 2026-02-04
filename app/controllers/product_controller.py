from sqlalchemy.orm import Session
from app.models.product import ProductModel

def get_all_products(db: Session):
    return db.query(ProductModel).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()

# --- CRÉATION : Synchronisée avec ton modèle ---
def create_new_product(db: Session, name, description, price, category, image_url):
    new_product = ProductModel(
        name=name,
        description=description,
        price=price,
        category=category,
        image=image_url,  # <--- On utilise 'image' car c'est le nom dans ton modèle
        is_available=True
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def update_product_info(db: Session, product_id: int, product_data):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product:
        # On utilise une boucle pour mettre à jour les champs proprement
        for key, value in product_data.dict(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product_by_id(db: Session, product_id: int):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False