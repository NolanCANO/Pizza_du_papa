from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from .size import Size


class OrderItemCreate(BaseModel):
    """Schéma pour créer un item de commande."""
    pizza_id: int = Field(..., gt=0)
    size_id: Optional[int] = Field(None, gt=0, description="ID de la taille (optionnel)")
    quantity: int = Field(..., gt=0)


class OrderItemResponse(BaseModel):
    """Schéma de réponse pour un item de commande."""
    id: int
    pizza_id: int
    size_id: Optional[int]
    quantity: int
    unit_price: float
    
    model_config = ConfigDict(from_attributes=True)


class OrderItemWithDetails(OrderItemResponse):
    """Schéma de réponse pour un item de commande avec détails."""
    size: Optional[Size] = None
    
    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    """Schéma pour créer une commande."""
    customer_name: str = Field(..., min_length=1)
    delivery_address: str = Field(..., min_length=1)
    items: list[OrderItemCreate] = Field(..., min_length=1)


class OrderStatusUpdate(BaseModel):
    """Schéma pour mettre à jour le statut d'une commande."""
    status: str = Field(..., pattern="^(PENDING|PREPARING|OUT_FOR_DELIVERY|DELIVERED|CANCELLED)$")


class OrderResponse(BaseModel):
    """Schéma de réponse pour une commande."""
    id: int
    customer_name: str
    delivery_address: str
    total_price: float
    status: str
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemWithDetails]
    
    model_config = ConfigDict(from_attributes=True)
