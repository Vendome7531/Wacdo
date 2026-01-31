from pydantic import BaseModel
from typing import List, Optional
from app.schemas.product import ProductSchema

class MenuBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image: Optional[str] = None
    
class MenuCreate(MenuBase):
    product_ids: List[int]

class MenuSchema(MenuBase):
    id: int
    products: List[ProductSchema]

    class Config:
        from_attributes = True