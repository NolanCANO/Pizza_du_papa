from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.schemas.size import (
    Size, SizeCreate, SizeUpdate,
    PizzaSize, PizzaSizeCreate, PizzaSizeUpdate, PizzaSizeWithDetails
)
from app.services.size_service import SizeService, PizzaSizeService

router = APIRouter(prefix="/sizes", tags=["sizes"])
pizza_sizes_router = APIRouter(prefix="/pizza-sizes", tags=["pizza-sizes"])


# Routes pour les tailles
@router.get("/", response_model=List[Size])
def get_sizes(db: Session = Depends(get_db)):
    """Récupère toutes les tailles disponibles."""
    return SizeService.get_all_sizes(db)


@router.get("/{size_id}", response_model=Size)
def get_size(size_id: int, db: Session = Depends(get_db)):
    """Récupère une taille par son ID."""
    size = SizeService.get_size_by_id(db, size_id)
    if not size:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Taille non trouvée"
        )
    return size


@router.post("/", response_model=Size, status_code=status.HTTP_201_CREATED)
def create_size(size_data: SizeCreate, db: Session = Depends(get_db)):
    """Crée une nouvelle taille."""
    return SizeService.create_size(db, size_data)


@router.put("/{size_id}", response_model=Size)
def update_size(size_id: int, size_data: SizeUpdate, db: Session = Depends(get_db)):
    """Met à jour une taille."""
    updated_size = SizeService.update_size(db, size_id, size_data)
    if not updated_size:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Taille non trouvée"
        )
    return updated_size


@router.delete("/{size_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_size(size_id: int, db: Session = Depends(get_db)):
    """Supprime une taille."""
    if not SizeService.delete_size(db, size_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Taille non trouvée"
        )


# Routes pour les combinaisons pizza-taille
@pizza_sizes_router.get("/pizza/{pizza_id}", response_model=List[PizzaSizeWithDetails])
def get_pizza_sizes(pizza_id: int, db: Session = Depends(get_db)):
    """Récupère toutes les tailles disponibles pour une pizza."""
    return PizzaSizeService.get_pizza_sizes_by_pizza(db, pizza_id)


@pizza_sizes_router.get("/{pizza_size_id}", response_model=PizzaSizeWithDetails)
def get_pizza_size(pizza_size_id: int, db: Session = Depends(get_db)):
    """Récupère une combinaison pizza-taille par son ID."""
    pizza_size = PizzaSizeService.get_pizza_size_by_id(db, pizza_size_id)
    if not pizza_size:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Combinaison pizza-taille non trouvée"
        )
    return pizza_size


@pizza_sizes_router.post("/", response_model=PizzaSizeWithDetails, status_code=status.HTTP_201_CREATED)
def create_pizza_size(pizza_size_data: PizzaSizeCreate, db: Session = Depends(get_db)):
    """Crée une nouvelle combinaison pizza-taille."""
    return PizzaSizeService.create_pizza_size(db, pizza_size_data)


@pizza_sizes_router.put("/{pizza_size_id}", response_model=PizzaSizeWithDetails)
def update_pizza_size(pizza_size_id: int, pizza_size_data: PizzaSizeUpdate, db: Session = Depends(get_db)):
    """Met à jour une combinaison pizza-taille."""
    updated_pizza_size = PizzaSizeService.update_pizza_size(db, pizza_size_id, pizza_size_data)
    if not updated_pizza_size:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Combinaison pizza-taille non trouvée"
        )
    return updated_pizza_size


@pizza_sizes_router.delete("/{pizza_size_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pizza_size(pizza_size_id: int, db: Session = Depends(get_db)):
    """Supprime une combinaison pizza-taille."""
    if not PizzaSizeService.delete_pizza_size(db, pizza_size_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Combinaison pizza-taille non trouvée"
        )


@pizza_sizes_router.get("/price/{pizza_id}/{size_id}")
def get_pizza_size_price(pizza_id: int, size_id: int, db: Session = Depends(get_db)):
    """Récupère le prix pour une combinaison pizza-taille."""
    price = PizzaSizeService.get_price_for_pizza_size(db, pizza_id, size_id)
    if price is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Combinaison pizza-taille non trouvée"
        )
    return {"pizza_id": pizza_id, "size_id": size_id, "price": price}