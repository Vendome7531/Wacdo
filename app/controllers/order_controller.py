from sqlalchemy.orm import Session
from app.models.order import OrderModel
from app.models.product import ProductModel
from app.schemas.order import OrderCreate
from fastapi import HTTPException

def create_new_order(db: Session, order_data: OrderCreate):
    total = 0
    # Logique de calcul du prix
    for p_id in order_data.product_ids:
        product = db.query(ProductModel).filter(ProductModel.id == p_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produit {p_id} non trouvé")
        total += product.price
    
    # Création de l'objet
    new_order = OrderModel(user_id=order_data.user_id, total_price=total)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order