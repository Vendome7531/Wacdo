from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderSchema(BaseModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    total_price: float
    status: str = "En cours"

    class Config:
        from_attributes = True

# Ce schéma servira pour la création d'une commande
class OrderCreate(BaseModel):
    product_ids: List[int]