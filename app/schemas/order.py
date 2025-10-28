from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class OrderItemCreate(BaseModel):
    """Schéma pour créer un item de commande."""
    pizza_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class OrderItemResponse(BaseModel):
    """Schéma de réponse pour un item de commande."""
    id: int
    pizza_id: int
    quantity: int
    
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
    items: list[OrderItemResponse]
    
    model_config = ConfigDict(from_attributes=True)
