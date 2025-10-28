from sqlalchemy import Column, Integer, String, Float, Boolean
from app.db import Base


class Pizza(Base):
    """Modèle de pizza."""
    __tablename__ = "pizzas"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
