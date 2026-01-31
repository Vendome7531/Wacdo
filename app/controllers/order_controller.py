from sqlalchemy.orm import Session
from app.models.order import OrderModel, OrderStatus
from app.models.product import ProductModel
from app.models.menu import MenuModel
from app.schemas.order import OrderCreate

def create_order(db: Session, order_data: OrderCreate, user_id: int):
    # 1. Initialiser le prix final
    final_price = 0.0
    db_menus = []
    db_products = []

    # 2. Calculer le prix des menus et les récupérer
    if order_data.menu_ids:
        db_menus = db.query(MenuModel).filter(MenuModel.id.in_(order_data.menu_ids)).all()
        for menu in db_menus:
            final_price += menu.price

    # 3. Calculer le prix des produits seuls et les récupérer
    if order_data.product_ids:
        db_products = db.query(ProductModel).filter(ProductModel.id.in_(order_data.product_ids)).all()
        for product in db_products:
            final_price += product.price

    # 4. Créer l'objet Commande
    new_order = OrderModel(
        user_id=user_id,
        notes=order_data.notes,
        final_price=round(final_price, 2), # On arrondit à 2 décimales
        status=OrderStatus.EN_ATTENTE,
        menus=db_menus,
        products=db_products
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

def update_order_status(db: Session, order_id: int, new_status: str):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not db_order:
        return None
    
    db_order.status = new_status
    db.commit()
    db.refresh(db_order)
    return db_order