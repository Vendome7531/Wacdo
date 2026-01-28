from pydantic import BaseModel
from app.models.product import CategoryEnum


# Ce qui est commun à la création et à l'affichage
class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float

# Ce qu'on utilise pour la CREATION (POST)
class ProductCreate(ProductBase):
    name : str
    description : str
    price : float
    category : CategoryEnum
    image : str
    is_available : bool
    

# Ce qu'on utilise pour l'AFFICHAGE (GET)
class ProductSchema(ProductBase):
    id: int

    class Config:
        from_attributes = True # Permet de convertir les objets SQLAlchemy en JSON