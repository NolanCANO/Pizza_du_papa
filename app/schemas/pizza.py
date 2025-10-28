from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from .size import PizzaSizeWithDetails


class PizzaBase(BaseModel):
    """Schéma de base pour une pizza."""
    name: str = Field(..., min_length=1)
    description: str
    price: float = Field(..., gt=0, description="Prix de base de la pizza")
    is_available: bool = True


class PizzaCreate(PizzaBase):
    """Schéma pour créer une pizza."""
    pass


class PizzaUpdate(BaseModel):
    """Schéma pour mettre à jour une pizza."""
    name: str | None = None
    description: str | None = None
    price: float | None = Field(None, gt=0)
    is_available: bool | None = None


class PizzaResponse(PizzaBase):
    """Schéma de réponse pour une pizza."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class PizzaWithSizes(PizzaResponse):
    """Schéma de réponse pour une pizza avec ses tailles disponibles."""
    pizza_sizes: List[PizzaSizeWithDetails] = []
    
    model_config = ConfigDict(from_attributes=True)
