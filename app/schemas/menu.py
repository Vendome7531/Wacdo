from pydantic import BaseModel
from typing import List, Optional
from app.schemas.product import ProductSchema

class MenuBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class MenuCreate(MenuBase):
    # C'est ici qu'on demande les IDs des produits pour la création
    product_ids: List[int]

class MenuSchema(MenuBase):
    id: int
    # Quand on récupère le menu, on veut voir le détail des produits, pas juste les IDs
    products: List[ProductSchema]

    class Config:
        from_attributes = True