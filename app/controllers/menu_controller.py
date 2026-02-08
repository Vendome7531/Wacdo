from sqlalchemy.orm import Session
from app.models.menu import MenuModel
from app.models.product import ProductModel

def get_all_menus(db: Session):
    """Récupère tous les menus."""
    # On renvoie les objets tels quels, SQLAlchemy gère le booléen (0/1)
    return db.query(MenuModel).all()

def get_menu_by_id(db: Session, menu_id: int):
    """Récupère un menu spécifique par son identifiant."""
    return db.query(MenuModel).filter(MenuModel.id == menu_id).first()

def create_new_menu(db: Session, name, description, price, image_url, is_available, product_ids=None):
    """Crée un menu."""
    # is_available est déjà un booléen venant du router
    new_menu = MenuModel(
        name=name,
        description=description,
        price=price,
        image=image_url,
        is_available=is_available 
    )
    
    if product_ids and product_ids.strip():
        try:
            ids_list = [int(id.strip()) for id in product_ids.split(",") if id.strip()]
            products = db.query(ProductModel).filter(ProductModel.id.in_(ids_list)).all()
            new_menu.products = products
        except ValueError:
            pass
        
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu

def update_menu_in_db(db: Session, menu_id: int, name, description, price, image_url, is_available, product_ids):
    """Met à jour un menu."""
    db_menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()
    
    if db_menu:
        if name is not None: db_menu.name = name
        if description is not None: db_menu.description = description
        if price is not None: db_menu.price = price
        if image_url is not None: db_menu.image = image_url
        if is_available is not None: db_menu.is_available = is_available
        
        if product_ids is not None:
            if product_ids.strip() == "":
                db_menu.products = []
            else:
                try:
                    ids_list = [int(id.strip()) for id in product_ids.split(",") if id.strip()]
                    products = db.query(ProductModel).filter(ProductModel.id.in_(ids_list)).all()
                    db_menu.products = products
                except ValueError:
                    pass

        db.commit()
        db.refresh(db_menu)
        
    return db_menu

def delete_menu_by_id(db: Session, menu_id: int):
    db_menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()
    if db_menu:
        db.delete(db_menu)
        db.commit()
        return True
    return False