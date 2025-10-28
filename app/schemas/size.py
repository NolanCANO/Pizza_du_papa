from pydantic import BaseModel, Field
from typing import Optional


class SizeBase(BaseModel):
    """Schéma de base pour les tailles."""
    name: str = Field(..., description="Nom de la taille")
    description: Optional[str] = Field(None, description="Description de la taille")
    price_multiplier: float = Field(1.0, gt=0, description="Multiplicateur de prix")


class SizeCreate(SizeBase):
    """Schéma pour créer une taille."""
    pass


class SizeUpdate(BaseModel):
    """Schéma pour mettre à jour une taille."""
    name: Optional[str] = Field(None, description="Nom de la taille")
    description: Optional[str] = Field(None, description="Description de la taille")
    price_multiplier: Optional[float] = Field(None, gt=0, description="Multiplicateur de prix")


class Size(SizeBase):
    """Schéma pour retourner une taille."""
    id: int

    class Config:
        from_attributes = True


class PizzaSizeBase(BaseModel):
    """Schéma de base pour les combinaisons pizza-taille."""
    pizza_id: int = Field(..., description="ID de la pizza")
    size_id: int = Field(..., description="ID de la taille")
    specific_price: Optional[float] = Field(None, gt=0, description="Prix spécifique pour cette combinaison")
    is_available: bool = Field(True, description="Disponibilité de cette combinaison")


class PizzaSizeCreate(PizzaSizeBase):
    """Schéma pour créer une combinaison pizza-taille."""
    pass


class PizzaSizeUpdate(BaseModel):
    """Schéma pour mettre à jour une combinaison pizza-taille."""
    specific_price: Optional[float] = Field(None, gt=0, description="Prix spécifique pour cette combinaison")
    is_available: Optional[bool] = Field(None, description="Disponibilité de cette combinaison")


class PizzaSize(PizzaSizeBase):
    """Schéma pour retourner une combinaison pizza-taille."""
    id: int
    calculated_price: float = Field(..., description="Prix calculé pour cette combinaison")

    class Config:
        from_attributes = True


class PizzaSizeWithDetails(PizzaSize):
    """Schéma pour retourner une combinaison pizza-taille avec détails."""
    size: Size
    
    class Config:
        from_attributes = True