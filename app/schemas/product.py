from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Big Mac"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "Deux étages de bœuf haché..."})
    price: float = Field(..., json_schema_extra={"example": 5.99})
    is_available: bool = Field(True, json_schema_extra={"example": True})

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: bool = Field(..., json_schema_extra={"example": True})

class ProductSchema(BaseModel):
    id: int = Field(..., json_schema_extra={"example": 1})
    name: str = Field(..., json_schema_extra={"example": "Big Mac"})
    description: Optional[str] = None
    price: float = Field(..., json_schema_extra={"example": 5.99})
    is_available: bool
    image: Optional[str] = Field(None, json_schema_extra={"example": "uploads/bigmac.jpg"})

    # CHANGEMENT ICI : Adieu class Config, bonjour model_config
    model_config = ConfigDict(from_attributes=True)

class ProductDeleteResponse(BaseModel):
    message: str = Field(..., json_schema_extra={"example": "Produit supprimé avec succès"})