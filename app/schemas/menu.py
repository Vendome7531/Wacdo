from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from app.schemas.product import ProductSchema 

class MenuBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Menu Best Of Big Mac"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "Le grand classique avec frites et boisson"})
    price: float = Field(..., json_schema_extra={"example": 10.50})
    is_available: bool = Field(True, json_schema_extra={"example": True})

class MenuCreate(MenuBase):
    product_ids: List[int] = Field([], json_schema_extra={"example": [1, 5, 12]})

class MenuSchema(BaseModel):
    id: int = Field(..., json_schema_extra={"example": 1})
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool 
    image: Optional[str] = Field(None, json_schema_extra={"example": "uploads/menus/bestof.jpg"})
    products: List[ProductSchema] = []

    # Le changement clé pour Pydantic V2
    model_config = ConfigDict(from_attributes=True)

class MenuDeleteResponse(BaseModel):
    message: str = Field(..., json_schema_extra={"example": "Menu supprimé avec succès"})