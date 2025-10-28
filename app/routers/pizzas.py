from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.pizza import PizzaCreate, PizzaUpdate, PizzaResponse
from app.services import pizza_service

router = APIRouter(prefix="/pizzas", tags=["pizzas"])


@router.get("/", response_model=list[PizzaResponse])
def list_pizzas(db: Session = Depends(get_db)):
    """Liste toutes les pizzas."""
    return pizza_service.get_all_pizzas(db)


@router.get("/{pizza_id}", response_model=PizzaResponse)
def get_pizza(pizza_id: int, db: Session = Depends(get_db)):
    """Récupère une pizza par son ID."""
    pizza = pizza_service.get_pizza_by_id(db, pizza_id)
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza introuvable")
    return pizza


@router.post("/", response_model=PizzaResponse, status_code=201)
def create_pizza(pizza_data: PizzaCreate, db: Session = Depends(get_db)):
    """Crée une nouvelle pizza."""
    try:
        return pizza_service.create_pizza(db, pizza_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{pizza_id}", response_model=PizzaResponse)
def update_pizza(pizza_id: int, pizza_data: PizzaUpdate, db: Session = Depends(get_db)):
    """Met à jour une pizza."""
    pizza = pizza_service.update_pizza(db, pizza_id, pizza_data)
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza introuvable")
    return pizza


@router.delete("/{pizza_id}", status_code=204)
def delete_pizza(pizza_id: int, db: Session = Depends(get_db)):
    """Supprime une pizza."""
    success = pizza_service.delete_pizza(db, pizza_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pizza introuvable")
