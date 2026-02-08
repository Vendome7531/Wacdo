from pydantic import BaseModel
from typing import List, Optional
from app.schemas.product import ProductSchema 

class MenuBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True 

class MenuCreate(MenuBase):
    product_ids: List[int] = []

class MenuSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool 
    image: Optional[str] = None
    products: List[ProductSchema] = []

    class Config:
        from_attributes = True

class MenuDeleteResponse(BaseModel):
    message: str