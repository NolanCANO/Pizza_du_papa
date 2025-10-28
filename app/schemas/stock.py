from pydantic import BaseModel, Field, ConfigDict


class StockItemBase(BaseModel):
    """Schéma de base pour un item de stock."""
    ingredient: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=0)


class StockItemCreate(StockItemBase):
    """Schéma pour créer un item de stock."""
    pass


class StockItemAdjust(BaseModel):
    """Schéma pour ajuster un item de stock."""
    quantity: int


class StockItemResponse(StockItemBase):
    """Schéma de réponse pour un item de stock."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)
