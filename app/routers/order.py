from fastapi import APIRouter, Depends, HTTPException, status, Path, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.database import get_db
from app.controllers import order_controller
from app.schemas.order import OrderCreate, OrderResponse
from app.models.order import OrderModel, OrderStatus 
from app.dependencies import get_current_user, admin_only, accueil_only, preparation_only

router = APIRouter(
    prefix="/orders",
    tags=["Commandes"]
)

# --- 1. SAISIE DE COMMANDE (Rôle : Accueil ou Admin) ---
@router.post("/", status_code=201)
def create_new_order(
    # On reçoit les IDs sous forme de texte : "1,2,5"
    menu_ids: Optional[str] = Form(None, description="IDs des menus séparés par une virgule (ex: 1,2)"),
    product_ids: Optional[str] = Form(None, description="IDs des produits séparés par une virgule (ex: 10,11,12)"),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user = Depends(accueil_only)
):
    """**Saisie Ultra-Rapide** : Tapez les IDs séparés par des virgules."""
    return order_controller.create_order_from_form(
        db=db,
        menu_ids_str=menu_ids,
        product_ids_str=product_ids,
        notes=notes,
        user_id=current_user.id
    )

# --- 2. LISTE DES COMMANDES (Visible par tous le staff connecté) ---
@router.get("/", response_model=List[OrderResponse])
def list_all_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """**Tout le personnel** : Liste complète des commandes pour le suivi général."""
    return order_controller.get_all_orders(db)

# --- 3. COMMANDES À PRÉPARER (Rôle : Préparation) ---
@router.get("/to-prepare", response_model=List[OrderResponse])
def list_orders_to_prepare(
    db: Session = Depends(get_db),
    current_user = Depends(preparation_only)
):
    """**Cuisine / Admin** : Affiche uniquement les commandes dont le statut est 'EN_ATTENTE'."""
    return order_controller.get_orders_to_prepare(db)

# --- 4. VALIDER UNE PRÉPARATION (Rôle : Préparation) ---
@router.patch("/{order_id}/ready", response_model=OrderResponse)
def mark_order_as_ready(
    order_id: int = Path(..., description="ID de la commande à passer en 'PRÊTE'"),
    db: Session = Depends(get_db),
    current_user = Depends(preparation_only)
):
    """**Cuisine / Admin** : Le préparateur signale que le plateau/sac est prêt."""
    # Note : Utilise un statut intermédiaire comme OrderStatus.PRETE si tu l'as
    order = order_controller.update_order_status(db, order_id, "prete") 
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return order

# --- 5. REMETTRE UNE COMMANDE AU CLIENT (Rôle : Accueil) ---
@router.patch("/{order_id}/deliver", response_model=OrderResponse)
def deliver_order(
    order_id: int = Path(..., description="ID de la commande remise au client"),
    db: Session = Depends(get_db),
    current_user = Depends(accueil_only)
):
    """**Accueil / Admin** : L'agent d'accueil confirme la remise au client (Statut 'TERMINE')."""
    order = order_controller.update_order_status(db, order_id, OrderStatus.TERMINE)
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return order