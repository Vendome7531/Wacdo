from pydantic import BaseModel
from typing import List

class OrderCreate(BaseModel):
    product_ids: list[int]
    user_id: int  

class OrderSchema(BaseModel):
    id: int
    total_price: float
    user_id: int 

    class Config:
        from_attributes = True