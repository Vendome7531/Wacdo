from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.order import OrderModel, OrderStatus
from app.models.product import ProductModel
from app.models.menu import MenuModel
from typing import Optional, List

# --- 1. FONCTION UTILITAIRE : Parsing des IDs ---
def parse_string_to_ids(id_str: Optional[str]) -> List[int]:
    """Transforme '1, 2, 3' en [1, 2, 3] en ignorant les erreurs de saisie."""
    if not id_str or id_str.strip() == "":
        return []
    return [int(x.strip()) for x in id_str.split(",") if x.strip().isdigit()]

# --- 2. CRÉATION (Saisie par l'Accueil via Formulaire) ---
def create_order_from_form(
    db: Session, 
    menu_ids_str: Optional[str], 
    product_ids_str: Optional[str], 
    notes: Optional[str], 
    user_id: Optional[int] = None
):
    """Crée une commande à partir des chaînes de caractères du formulaire."""
    
    # Conversion des strings en listes d'entiers
    menu_ids = parse_string_to_ids(menu_ids_str)
    product_ids = parse_string_to_ids(product_ids_str)

    final_price = 0.0
    db_menus = []
    db_products = []

    # Récupération et calcul des Menus
    if menu_ids:
        db_menus = db.query(MenuModel).filter(MenuModel.id.in_(menu_ids)).all()
        final_price += sum(menu.price for menu in db_menus)

    # Récupération et calcul des Produits
    if product_ids:
        db_products = db.query(ProductModel).filter(ProductModel.id.in_(product_ids)).all()
        final_price += sum(product.price for product in db_products)

    # Création en base
    new_order = OrderModel(
        user_id=user_id,
        notes=notes,
        final_price=round(final_price, 2),
        status=OrderStatus.EN_ATTENTE,
        menus=db_menus,
        products=db_products
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

# --- 3. MISE À JOUR DU STATUT ---
def update_order_status(db: Session, order_id: int, new_status: OrderStatus):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not db_order:
        return None
    
    db_order.status = new_status
    db.commit()
    db.refresh(db_order)
    return db_order

# --- 4. LECTURE : COMMANDES À PRÉPARER (Cuisine) ---
def get_orders_to_prepare(db: Session):
    return db.query(OrderModel)\
        .filter(OrderModel.status.in_([OrderStatus.EN_ATTENTE, OrderStatus.EN_PREPARATION]))\
        .order_by(OrderModel.created_at.asc())\
        .all()

# --- 5. TOUTES LES COMMANDES (Historique/Admin) ---
def get_all_orders(db: Session):
    return db.query(OrderModel).order_by(OrderModel.created_at.desc()).all()