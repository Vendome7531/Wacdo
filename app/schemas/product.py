from pydantic import BaseModel, Field
from typing import Optional
from app.models.product import CategoryEnum

# Ce qui est commun à la création et à l'affichage
class ProductBase(BaseModel):
    name: str = Field(..., example="Big Wac", description="Nom du produit")
    description: Optional[str] = Field(None, example="Double steak, fromage fondant et sauce secrète", description="Ingrédients et détails")
    price: float = Field(..., example=5.90, description="Prix de vente unitaire")

# Ce qu'on utilise pour la CREATION (POST)
class ProductCreate(ProductBase):
    category: CategoryEnum = Field(..., example="burgers", description="Catégorie du menu")
    image: str = Field(..., example="big_wac.jpg", description="Nom du fichier image ou URL")
    is_available: bool = Field(True, example=True, description="Disponibilité en stock")

# Ce qu'on utilise pour l'AFFICHAGE (GET)
class ProductSchema(ProductBase):
    id: int = Field(..., example=12)
    # On rajoute les champs de ProductCreate pour qu'ils soient visibles au GET
    category: CategoryEnum
    image: str
    is_available: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 12,
                "name": "Big Wac",
                "description": "Double steak, fromage fondant et sauce secrète",
                "price": 5.90,
                "category": "burgers",
                "image": "big_wac.jpg",
                "is_available": True
            }
        }

class ProductUpdate(ProductCreate):
    # Les champs sont hérités de ProductCreate
    pass

class ProductDeleteResponse(BaseModel):
    message: str = Field(..., example="Produit supprimé avec succès")