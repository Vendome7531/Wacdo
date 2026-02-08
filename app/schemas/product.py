from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True 

class ProductCreate(ProductBase):
    pass

# On le garde pour la forme, même si on utilise Form(...) dans le router
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: bool

class ProductSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool
    image: Optional[str] = None

    class Config:
        from_attributes = True

class ProductDeleteResponse(BaseModel):
    message: str