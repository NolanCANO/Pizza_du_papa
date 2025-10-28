from sqlalchemy import Column, Integer, String
from app.db import Base


class StockItem(Base):
    """Modèle d'item de stock."""
    __tablename__ = "stock_items"
    
    id = Column(Integer, primary_key=True, index=True)
    ingredient = Column(String, unique=True, nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=0)
