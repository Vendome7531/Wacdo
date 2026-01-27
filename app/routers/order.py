from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order import OrderCreate, OrderSchema
from app.controllers.order_controller import create_new_order # On importe le controller

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderSchema)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    # Le router délègue le travail au controller
    return create_new_order(db, order_data)