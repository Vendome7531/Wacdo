from pydantic import BaseModel
from typing import Optional

class ProductSchema(BaseModel):
    id: Optional[int] = None  # Crucial : permet l'affichage sans forcer la saisie
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    image: Optional[str] = None
    is_available: bool = True

    class Config:
        from_attributes = True