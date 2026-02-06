from sqlalchemy.orm import Session
from app.models.product import ProductModel

def get_all_products(db: Session):
    """Récupère tous les produits et convertit le booléen en texte pour l'affichage."""
    products = db.query(ProductModel).all()
    for p in products:
        p.is_available = "disponible" if p.is_available else "non disponible"
    return products

def get_product_by_id(db: Session, product_id: int):
    """Récupère un produit par son ID et formate sa disponibilité."""
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if product:
        product.is_available = "disponible" if product.is_available else "non disponible"
    return product

def create_new_product(db: Session, name, description, price, image_url, is_available):
    """Crée un produit en convertissant le choix du menu déroulant en booléen."""
    bool_available = True if is_available == "disponible" else False
    
    new_product = ProductModel(
        name=name,
        description=description,
        price=price,
        image=image_url,
        is_available=bool_available
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    # On reformate pour la réponse JSON
    new_product.is_available = "disponible" if new_product.is_available else "non disponible"
    return new_product

def update_product(db: Session, product_id: int, name, description, price, image_url, is_available):
    """Met à jour un produit existant (gestion des ruptures de stock)."""
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    
    if db_product:
        # Mise à jour seulement si les champs sont fournis (non None)
        if name is not None: db_product.name = name
        if description is not None: db_product.description = description
        if price is not None: db_product.price = price
        if image_url is not None: db_product.image = image_url
        
        # Conversion du menu déroulant pour la BDD
        if is_available is not None:
            db_product.is_available = True if is_available == "disponible" else False

        db.commit()
        db.refresh(db_product)
        
        # On reformate pour que l'admin voie le résultat en texte
        db_product.is_available = "disponible" if db_product.is_available else "non disponible"
        
    return db_product

def delete_product_by_id(db: Session, product_id: int):
    """Supprime définitivement un produit."""
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False