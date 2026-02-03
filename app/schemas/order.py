from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.order import OrderStatus

# Ce qui est nécessaire pour CRÉER une commande
class OrderCreate(BaseModel):
    menu_ids: Optional[List[int]] = None
    product_ids: Optional[List[int]] = None
    notes: Optional[str] = None

# Ce qui est renvoyé par l'API (Lecture)
class OrderResponse(BaseModel):
    id: int
    created_at: datetime
    notes: Optional[str]
    final_price: float
    status: OrderStatus
    user_id: Optional[int]

    class Config:
        from_attributes = True # Permet à Pydantic de lire les modèles SQLAlchemy