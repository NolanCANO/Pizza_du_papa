from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.order import OrderCreate, OrderStatusUpdate, OrderResponse
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    """Crée une nouvelle commande."""
    try:
        return order_service.create_order(db, order_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Récupère une commande par son ID."""
    order = order_service.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    return order


@router.get("/", response_model=list[OrderResponse])
def list_orders(status: str | None = Query(None), db: Session = Depends(get_db)):
    """Liste les commandes, filtrables par statut."""
    return order_service.get_orders_by_status(db, status)


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: int, status_data: OrderStatusUpdate, db: Session = Depends(get_db)):
    """Met à jour le statut d'une commande."""
    order = order_service.update_order_status(db, order_id, status_data)
    if not order:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    return order


@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    """Annule une commande."""
    try:
        order = order_service.cancel_order(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Commande introuvable")
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
