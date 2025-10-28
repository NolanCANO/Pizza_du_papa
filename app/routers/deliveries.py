from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.delivery import DeliveryCreate, DeliveryStatusUpdate, DeliveryResponse
from app.services import delivery_service

router = APIRouter(prefix="/deliveries", tags=["deliveries"])


@router.post("/", response_model=DeliveryResponse, status_code=201)
def create_delivery(delivery_data: DeliveryCreate, db: Session = Depends(get_db)):
    """Crée une nouvelle livraison."""
    try:
        return delivery_service.create_delivery(db, delivery_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{delivery_id}", response_model=DeliveryResponse)
def get_delivery(delivery_id: int, db: Session = Depends(get_db)):
    """Récupère une livraison par son ID."""
    delivery = delivery_service.get_delivery_by_id(db, delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Livraison introuvable")
    return delivery


@router.patch("/{delivery_id}/status", response_model=DeliveryResponse)
def update_delivery_status(delivery_id: int, status_data: DeliveryStatusUpdate, db: Session = Depends(get_db)):
    """Met à jour le statut d'une livraison."""
    delivery = delivery_service.update_delivery_status(db, delivery_id, status_data)
    if not delivery:
        raise HTTPException(status_code=404, detail="Livraison introuvable")
    return delivery
