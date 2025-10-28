from sqlalchemy.orm import Session
from app.models.stock import StockItem
from app.schemas.stock import StockItemCreate
from app.logging_config import logger


def get_all_stock_items(db: Session) -> list[StockItem]:
    """Récupère tous les items de stock."""
    return db.query(StockItem).all()


def get_stock_item_by_id(db: Session, stock_id: int) -> StockItem | None:
    """Récupère un item de stock par son ID."""
    return db.query(StockItem).filter(StockItem.id == stock_id).first()


def get_stock_item_by_ingredient(db: Session, ingredient: str) -> StockItem | None:
    """Récupère un item de stock par son ingrédient."""
    return db.query(StockItem).filter(StockItem.ingredient == ingredient).first()


def create_stock_item(db: Session, stock_data: StockItemCreate) -> StockItem:
    """Crée un nouvel item de stock."""
    stock_item = StockItem(**stock_data.model_dump())
    db.add(stock_item)
    db.commit()
    db.refresh(stock_item)
    return stock_item


def adjust_stock_quantity(db: Session, stock_id: int, quantity_change: int) -> StockItem | None:
    """Ajuste la quantité d'un item de stock."""
    stock_item = get_stock_item_by_id(db, stock_id)
    if not stock_item:
        return None
    
    new_quantity = stock_item.quantity + quantity_change
    if new_quantity < 0:
        raise ValueError(f"La quantité ne peut pas être négative (actuelle: {stock_item.quantity}, changement: {quantity_change})")
    
    stock_item.quantity = new_quantity
    db.commit()
    db.refresh(stock_item)
    
    logger.info(f"Stock ajusté: {stock_item.ingredient} - {quantity_change:+d} (nouveau: {stock_item.quantity})")
    
    return stock_item


def decrement_stock(db: Session, ingredient: str, quantity: int) -> None:
    """Décrémente le stock d'un ingrédient."""
    stock_item = get_stock_item_by_ingredient(db, ingredient)
    if not stock_item:
        raise ValueError(f"Ingrédient '{ingredient}' introuvable dans le stock")
    
    if stock_item.quantity < quantity:
        raise ValueError(f"Stock insuffisant pour {ingredient}: disponible={stock_item.quantity}, requis={quantity}")
    
    stock_item.quantity -= quantity
    logger.info(f"Stock décrémenté: {ingredient} - {quantity} (reste: {stock_item.quantity})")
