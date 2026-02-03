from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.order import OrderModel, OrderStatus
from app.models.product import ProductModel
from app.models.menu import MenuModel
from app.schemas.order import OrderCreate
from typing import Optional

# --- 1. CRÉATION (Saisie par l'Accueil) ---
def create_order(db: Session, order_data: OrderCreate, user_id: Optional[int] = None):
    """
    Crée une commande en calculant le prix dynamiquement depuis la base de données.
    """
    final_price = 0.0
    db_menus = []
    db_products = []

    # Calcul du prix des menus
    if order_data.menu_ids:
        db_menus = db.query(MenuModel).filter(MenuModel.id.in_(order_data.menu_ids)).all()
        for menu in db_menus:
            final_price += menu.price

    # Calcul du prix des produits seuls
    if order_data.product_ids:
        db_products = db.query(ProductModel).filter(ProductModel.id.in_(order_data.product_ids)).all()
        for product in db_products:
            final_price += product.price

    # Création de l'objet Commande (Statut initial par défaut : EN_ATTENTE)
    new_order = OrderModel(
        user_id=user_id,
        notes=order_data.notes,
        final_price=round(final_price, 2),
        status=OrderStatus.EN_ATTENTE,
        menus=db_menus,
        products=db_products
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

# --- 2. MISE À JOUR DU STATUT (Préparateur ou Accueil) ---
def update_order_status(db: Session, order_id: int, new_status: OrderStatus):
    """
    Met à jour le statut d'une commande.
    Le préparateur passera à TERMINE quand c'est prêt.
    """
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    
    if not db_order:
        return None
    
    db_order.status = new_status
    db.commit()
    db.refresh(db_order)
    return db_order

# --- 3. LECTURE : COMMANDES À PRÉPARER (Pour les Préparateurs) ---
def get_orders_to_prepare(db: Session):
    """
    Récupère les commandes 'en_attente' triées par heure (croissant).
    """
    return db.query(OrderModel)\
        .filter(OrderModel.status == OrderStatus.EN_ATTENTE)\
        .order_by(OrderModel.created_at.asc())\
        .all()

# --- 4. LECTURE : HISTORIQUE D'UN UTILISATEUR ---
def get_user_orders(db: Session, user_id: int):
    return db.query(OrderModel).filter(OrderModel.user_id == user_id).all()