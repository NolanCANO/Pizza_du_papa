from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.stock import StockItemCreate, StockItemAdjust, StockItemResponse
from app.services import stock_service

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("/", response_model=list[StockItemResponse])
def list_stock_items(db: Session = Depends(get_db)):
    """Liste tous les items de stock."""
    return stock_service.get_all_stock_items(db)


@router.post("/", response_model=StockItemResponse, status_code=201)
def create_stock_item(stock_data: StockItemCreate, db: Session = Depends(get_db)):
    """Crée un nouvel item de stock."""
    try:
        return stock_service.create_stock_item(db, stock_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{stock_id}", response_model=StockItemResponse)
def adjust_stock(stock_id: int, adjust_data: StockItemAdjust, db: Session = Depends(get_db)):
    """Ajuste la quantité d'un item de stock."""
    try:
        stock_item = stock_service.adjust_stock_quantity(db, stock_id, adjust_data.quantity)
        if not stock_item:
            raise HTTPException(status_code=404, detail="Item de stock introuvable")
        return stock_item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
