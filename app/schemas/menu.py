from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.product import ProductSchema

class MenuBase(BaseModel):
    name: str = Field(..., example="Menu Maxi Best-Wac", description="Nom du menu complet")
    description: Optional[str] = Field(None, example="Un burger, une grande frite et une boisson au choix", description="Détails du menu")
    price: float = Field(..., example=12.50, description="Prix du menu")
    image: Optional[str] = Field(None, example="menu_maxi.jpg", description="Lien vers l'image du menu")
    
class MenuCreate(MenuBase):
    product_ids: List[int] = Field(..., example=[1, 5, 8], description="IDs des produits à inclure dans le menu")

class MenuSchema(MenuBase):
    id: int = Field(..., example=1)
    products: List[ProductSchema] = Field(..., description="Liste des objets produits complets")

    class Config:
        from_attributes = True
        # Ce bloc écrase l'exemple par défaut dans Swagger
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Menu Maxi Best-Wac",
                "description": "Un burger, une grande frite et une boisson au choix",
                "price": 12.50,
                "image": "menu_maxi.jpg",
                "products": [
                    {
                        "id": 12,
                        "name": "Big Wac",
                        "description": "Double steak, fromage fondant",
                        "price": 5.90,
                        "category": "burgers",
                        "image": "big_wac.jpg",
                        "is_available": True
                    }
                ]
            }
        }

class MenuDeleteResponse(BaseModel):
    message: str = Field(..., example="Le menu a été supprimé avec succès")