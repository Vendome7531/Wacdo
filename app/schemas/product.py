from pydantic import BaseModel
from typing import Optional
from enum import Enum

# L'Enum qui crée le menu déroulant
class AvailabilityEnum(str, Enum):
    DISPO = "disponible"
    NON_DISPO = "non disponible"

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: AvailabilityEnum = AvailabilityEnum.DISPO

class ProductCreate(ProductBase):
    pass

# On le garde pour la forme, même si on utilise Form(...) dans le router
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[AvailabilityEnum] = None

class ProductSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    is_available: str  # On renvoie le texte ("disponible") pour le front/Swagger
    image: Optional[str] = None

    class Config:
        from_attributes = True

class ProductDeleteResponse(BaseModel):
    message: str