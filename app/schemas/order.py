from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderCreate(BaseModel):
    menu_ids: List[int] = []
    product_ids: List[int] = []
    notes: Optional[str] = None

class OrderSchema(BaseModel):
    id: int
    created_at: datetime
    notes: Optional[str]
    final_price: float
    status: str
    user_id: Optional[int] = None

    class Config:
        from_attributes = True