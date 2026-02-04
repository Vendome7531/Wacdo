from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.controllers import order_controller
from app.schemas.order import OrderCreate, OrderResponse
from app.models.order import OrderModel, OrderStatus  # <--- Ajout de OrderModel ici
from app.dependencies import get_current_user, admin_only, accueil_only, preparation_only

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# --- 1. SAISIE DE COMMANDE (Rôle : Accueil ou Admin) ---
@router.post("/", response_model=OrderResponse)
def create_new_order(
    order_data: OrderCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(accueil_only)
):
    """Saisie d'une nouvelle commande par l'accueil."""
    return order_controller.create_order(db, order_data, user_id=current_user.id)

# --- 2. LISTE DES COMMANDES À PRÉPARER (Rôle : Préparation) ---
@router.get("/to-prepare", response_model=List[OrderResponse])
def list_orders_to_prepare(
    db: Session = Depends(get_db),
    current_user = Depends(preparation_only)
):
    """Affiche les commandes qui attendent d'être préparées."""
    return order_controller.get_orders_to_prepare(db)

# --- 3. LECTURE D'UNE COMMANDE UNIQUE (ID) ---
@router.get("/{order_id}", response_model=OrderResponse)
def get_one_order(order_id: int, db: Session = Depends(get_db)):
    """Récupère les détails d'une commande spécifique par son ID."""
    # On cherche dans la table OrderModel via SQLAlchemy
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return order

# --- 4. VALIDER UNE PRÉPARATION (Rôle : Préparation) ---
@router.patch("/{order_id}/ready", response_model=OrderResponse)
def mark_order_as_ready(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(preparation_only)
):
    """Le préparateur marque la commande comme prête."""
    order = order_controller.update_order_status(db, order_id, OrderStatus.TERMINE)
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return order

# --- 5. REMETTRE UNE COMMANDE AU CLIENT (Rôle : Accueil) ---
@router.patch("/{order_id}/deliver", response_model=OrderResponse)
def deliver_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(accueil_only)
):
    """L'accueil marque la commande comme livrée au client."""
    order = order_controller.update_order_status(db, order_id, OrderStatus.TERMINE)
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return order