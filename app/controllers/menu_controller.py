from sqlalchemy.orm import Session
from app.models.menu import MenuModel
from app.models.product import ProductModel
from app.schemas.menu import MenuCreate

# CREATE
def create_new_menu(db: Session, menu_data: MenuCreate):
    new_menu = MenuModel(
        name=menu_data.name,
        description=menu_data.description,
        image=menu_data.image,
        price=menu_data.price
    )
    if menu_data.product_ids:
        products = db.query(ProductModel).filter(ProductModel.id.in_(menu_data.product_ids)).all()
        new_menu.products = products
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu

# READ (All)
def get_all_menus(db: Session):
    return db.query(MenuModel).all()

# READ (One)
def get_menu_by_id(db: Session, menu_id: int):
    return db.query(MenuModel).filter(MenuModel.id == menu_id).first()

# UPDATE
def update_menu_info(db: Session, menu_id: int, menu_data: MenuCreate):
    db_menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()
    if db_menu:
        db_menu.name = menu_data.name
        db_menu.description = menu_data.description
        db_menu.image = menu_data.image
        db_menu.price = menu_data.price
        
        # On met à jour l'association des produits
        if menu_data.product_ids:
            products = db.query(ProductModel).filter(ProductModel.id.in_(menu_data.product_ids)).all()
            db_menu.products = products
            
        db.commit()
        db.refresh(db_menu)
    return db_menu

# DELETE
def delete_menu_by_id(db: Session, menu_id: int):
    db_menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()
    if db_menu:
        db.delete(db_menu)
        db.commit()
    return db_menu