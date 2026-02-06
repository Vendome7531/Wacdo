from sqlalchemy.orm import Session
from app.models.menu import MenuModel
from app.models.product import ProductModel

def get_all_menus(db: Session):
    """Récupère tous les menus et formate la disponibilité pour l'affichage."""
    menus = db.query(MenuModel).all()
    for m in menus:
        m.is_available = "disponible" if m.is_available else "non disponible"
    return menus

def get_menu_by_id(db: Session, menu_id: int):
    """Récupère un menu spécifique par son identifiant."""
    menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()
    if menu:
        menu.is_available = "disponible" if menu.is_available else "non disponible"
    return menu

def create_new_menu(db: Session, name, description, price, image_url, is_available, product_ids=None):
    """Crée un menu et transforme la chaîne d'IDs (ex: '1,2') en relation SQL."""
    bool_available = True if is_available == "disponible" else False

    new_menu = MenuModel(
        name=name,
        description=description,
        price=price,
        image=image_url,
        is_available=bool_available
    )
    
    if product_ids and product_ids.strip():
        # Transformation de la chaîne "1, 2, 3" en liste d'entiers [1, 2, 3]
        try:
            ids_list = [int(id.strip()) for id in product_ids.split(",") if id.strip()]
            products = db.query(ProductModel).filter(ProductModel.id.in_(ids_list)).all()
            new_menu.products = products
        except ValueError:
            # Si l'utilisateur saisit autre chose que des chiffres, on ignore ou on pourrait lever une erreur
            pass
        
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    
    new_menu.is_available = "disponible" if new_menu.is_available else "non disponible"
    return new_menu

def update_menu_in_db(db: Session, menu_id: int, name, description, price, image_url, is_available, product_ids):
    """Met à jour un menu et sa composition via une liste d'IDs séparés par des virgules."""
    db_menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()
    
    if db_menu:
        if name is not None: db_menu.name = name
        if description is not None: db_menu.description = description
        if price is not None: db_menu.price = price
        if image_url is not None: db_menu.image = image_url
        
        if is_available is not None:
            db_menu.is_available = True if is_available == "disponible" else False
        
        # Mise à jour de la composition du menu (Many-to-Many)
        if product_ids is not None:
            if product_ids.strip() == "":
                db_menu.products = [] # On vide le menu si le champ est vide
            else:
                try:
                    # Conversion de la saisie texte en liste d'entiers
                    ids_list = [int(id.strip()) for id in product_ids.split(",") if id.strip()]
                    products = db.query(ProductModel).filter(ProductModel.id.in_(ids_list)).all()
                    db_menu.products = products
                except ValueError:
                    pass

        db.commit()
        db.refresh(db_menu)
        db_menu.is_available = "disponible" if db_menu.is_available else "non disponible"
        
    return db_menu

def delete_menu_by_id(db: Session, menu_id: int):
    """Supprime un menu après avoir vérifié son existence."""
    db_menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()
    if db_menu:
        db.delete(db_menu)
        db.commit()
        return True
    return False