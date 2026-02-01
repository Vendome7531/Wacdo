from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.order import OrderModel, OrderStatus
from app.models.product import ProductModel
from app.models.menu import MenuModel
from app.schemas.order import OrderCreate
from typing import Optional

# --- CRÉATION ---
def create_order(db: Session, order_data: OrderCreate, user_id: Optional[int] = None):
    """
    Crée une commande en calculant le prix dynamiquement.
    Le user_id est optionnel pour permettre les ventes au comptoir (anonymes).
    """
    final_price = 0.0
    db_menus = []
    db_products = []

    # 1. Récupérer et calculer le prix des menus
    if order_data.menu_ids:
        db_menus = db.query(MenuModel).filter(MenuModel.id.in_(order_data.menu_ids)).all()
        for menu in db_menus:
            final_price += menu.price

    # 2. Récupérer et calculer le prix des produits seuls
    if order_data.product_ids:
        db_products = db.query(ProductModel).filter(ProductModel.id.in_(order_data.product_ids)).all()
        for product in db_products:
            final_price += product.price

    # 3. Création de l'objet Commande (Statut initial : EN_ATTENTE)
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

# --- LECTURE : PRÉPARATION (Contrainte Exercice) ---
def get_orders_to_prepare(db: Session):
    """
    Récupère les commandes à préparer triées par heure de création.
    Répond au critère : 'triées par heure de livraison croissante'.
    """
    return db.query(OrderModel)\
        .filter(OrderModel.status == OrderStatus.EN_ATTENTE)\
        .order_by(OrderModel.created_at.asc())\
        .all()

# --- LECTURE : ACCUEIL ---
def get_ready_orders(db: Session):
    """Récupère les commandes prêtes à être remises au client."""
    return db.query(OrderModel)\
        .filter(OrderModel.status == OrderStatus.TERMINE)\
        .all()

# --- MISE À JOUR DU STATUT ---
def update_order_status(db: Session, order_id: int, new_status: OrderStatus):
    """
    Met à jour le statut d'une commande (ex: passer de 'en_attente' à 'termine').
    L'utilisation de l'Enum OrderStatus garantit l'intégrité des données.
    """
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    
    if not db_order:
        return None
    
    db_order.status = new_status
    db.commit()
    db.refresh(db_order)
    return db_order

# --- LECTURE : HISTORIQUE ---
def get_user_orders(db: Session, user_id: int):
    """Récupère l'historique des commandes d'un utilisateur spécifique."""
    return db.query(OrderModel).filter(OrderModel.user_id == user_id).all()