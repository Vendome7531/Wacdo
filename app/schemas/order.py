from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from app.models.order import OrderStatus

# --- Schéma pour CRÉER une commande ---
class OrderCreate(BaseModel):
    menu_ids: Optional[List[int]] = Field(None, description="Liste des IDs des menus (optionnel)", json_schema_extra={"examples": [[1]]})
    product_ids: Optional[List[int]] = Field(None, description="Liste des IDs des produits à la carte", json_schema_extra={"examples": [[5, 12]]})
    notes: Optional[str] = Field(None, description="Instructions pour la cuisine", json_schema_extra={"examples": ["Pas de sel sur les frites, merci !"]})

# --- Schéma pour la RÉPONSE (Lecture) ---
class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "example": {
            "id": 101,
            "created_at": "2026-02-04T10:00:00",
            "notes": "Pas de sel sur les frites",
            "final_price": 15.50,
            "status": "en_attente",
            "user_id": 2
        }
    })

    id: int = Field(..., description="ID de la commande", json_schema_extra={"examples": [101]})
    created_at: datetime = Field(default_factory=datetime.now, description="Date et heure de création")
    notes: Optional[str] = Field(None, description="Notes client", json_schema_extra={"examples": ["Pas de sel sur les frites"]})
    final_price: float = Field(..., description="Prix total calculé", json_schema_extra={"examples": [15.50]})
    status: OrderStatus = Field(..., description="Statut : en_attente, preparation, pret, livre", json_schema_extra={"examples": ["en_attente"]})
    user_id: Optional[int] = Field(None, description="ID de l'employé qui a saisi la commande", json_schema_extra={"examples": [2]})