from sqlalchemy.orm import Session
from app.models.product import ProductModel

def get_all_products(db: Session):
    """Récupère tous les produits (le booléen reste un booléen)."""
    return db.query(ProductModel).all()

def get_product_by_id(db: Session, product_id: int):
    """Récupère un produit par son ID."""
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()

def create_new_product(db: Session, name, description, price, image_url, is_available):
    """Crée un produit. is_available arrive déjà en booléen du router."""
    new_product = ProductModel(
        name=name,
        description=description,
        price=price,
        image=image_url,
        is_available=is_available
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def update_product(db: Session, product_id: int, name, description, price, image_url, is_available):
    """Met à jour un produit existant."""
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    
    if db_product:
        if name is not None: db_product.name = name
        if description is not None: db_product.description = description
        if price is not None: db_product.price = price
        if image_url is not None: db_product.image = image_url
        if is_available is not None:
            db_product.is_available = is_available

        db.commit()
        db.refresh(db_product)
        
    return db_product

def delete_product_by_id(db: Session, product_id: int):
    """Supprime définitivement un produit."""
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False