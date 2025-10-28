from sqlalchemy import Column, Integer, String, ForeignKey
from app.db import Base


class Delivery(Base):
    """Modèle de livraison."""
    __tablename__ = "deliveries"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True)
    assigned_driver = Column(String, nullable=False)
    eta_minutes = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="ASSIGNED")
