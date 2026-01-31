from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas import order as order_schemas
from app.controllers import order_controller
from app.routers.auth import get_current_user
from app.models.user import UserModel
from app.models.order import OrderModel # On l'importe proprement ici

router = APIRouter(prefix="/orders", tags=["Commandes"])

# --- CREATE ---
@router.post("/", response_model=order_schemas.OrderSchema, status_code=status.HTTP_201_CREATED)
def place_order(
    order_data: order_schemas.OrderCreate, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    try:
        return order_controller.create_order(
            db=db, 
            order_data=order_data, 
            user_id=current_user.id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erreur lors de la création : {str(e)}"
        )

# --- READ MY ORDERS ---
@router.get("/my-orders", response_model=list[order_schemas.OrderSchema])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return db.query(OrderModel).filter(OrderModel.user_id == current_user.id).all()

# --- UPDATE STATUS (PATCH) ---
@router.patch("/{order_id}/status", response_model=order_schemas.OrderSchema)
def change_order_status(
    order_id: int, 
    new_status: str, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # On appelle le controller pour la logique
    updated_order = order_controller.update_order_status(db, order_id, new_status)
    
    if not updated_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Commande non trouvée"
        )
    return updated_order