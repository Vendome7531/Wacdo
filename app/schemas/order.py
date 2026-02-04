from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.models.order import OrderStatus

# --- Schéma pour CRÉER une commande ---
class OrderCreate(BaseModel):
    menu_ids: Optional[List[int]] = Field(None, description="Liste des IDs des menus (optionnel)", example=[1])
    product_ids: Optional[List[int]] = Field(None, description="Liste des IDs des produits à la carte", example=[5, 12])
    notes: Optional[str] = Field(None, description="Instructions pour la cuisine", example="Pas de sel sur les frites, merci !")

# --- Schéma pour la RÉPONSE (Lecture) ---
class OrderResponse(BaseModel):
    id: int = Field(..., example=101)
    created_at: datetime = Field(default_factory=datetime.now, description="Date et heure de création")
    notes: Optional[str] = Field(None, example="Pas de sel sur les frites", description="Notes client")
    final_price: float = Field(..., example=15.50, description="Prix total calculé")
    status: OrderStatus = Field(..., example="en_attente", description="Statut : en_attente, preparation, pret, livre")
    user_id: Optional[int] = Field(None, example=2, description="ID de l'employé qui a saisi la commande")

    class Config:
        from_attributes = True
        # Ce bloc garantit que Swagger affiche l'exemple complet au lieu de "string"
        json_schema_extra = {
            "example": {
                "id": 101,
                "created_at": "2026-02-04T10:00:00",
                "notes": "Pas de sel sur les frites",
                "final_price": 15.50,
                "status": "en_attente",
                "user_id": 2
            }
        }