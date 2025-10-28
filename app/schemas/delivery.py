from pydantic import BaseModel, Field, ConfigDict


class DeliveryCreate(BaseModel):
    """Schéma pour créer une livraison."""
    order_id: int = Field(..., gt=0)
    assigned_driver: str = Field(..., min_length=1)
    eta_minutes: int = Field(..., gt=0)


class DeliveryStatusUpdate(BaseModel):
    """Schéma pour mettre à jour le statut d'une livraison."""
    status: str = Field(..., pattern="^(ASSIGNED|PICKED_UP|DELIVERED)$")
    eta_minutes: int | None = Field(None, gt=0)


class DeliveryResponse(BaseModel):
    """Schéma de réponse pour une livraison."""
    id: int
    order_id: int
    assigned_driver: str
    eta_minutes: int
    status: str
    
    model_config = ConfigDict(from_attributes=True)
