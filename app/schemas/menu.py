from pydantic import BaseModel
from typing import List, Optional
from app.schemas.product import ProductSchema, AvailabilityEnum

class MenuBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    # On utilise l'Enum pour que le POST propose le menu déroulant
    is_available: AvailabilityEnum = AvailabilityEnum.DISPO

class MenuCreate(MenuBase):
    product_ids: List[int] = []

class MenuSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    # On met 'str' ici car le controller renvoie "disponible" ou "non disponible"
    is_available: str 
    image: Optional[str] = None
    products: List[ProductSchema] = []

    class Config:
        from_attributes = True

class MenuDeleteResponse(BaseModel):
    message: str