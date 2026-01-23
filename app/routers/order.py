from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.order import OrderModel
from app.models.product import ProductModel
from app.schemas.order import OrderSchema, OrderCreate

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderSchema)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    total = 0
    for p_id in order_data.product_ids:
        product = db.query(ProductModel).filter(ProductModel.id == p_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produit {p_id} non trouvé")
        total += product.price
    
    new_order = OrderModel(total_price=total)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.get("/", response_model=list[OrderSchema])
def get_orders(db: Session = Depends(get_db)):
    return db.query(OrderModel).all()