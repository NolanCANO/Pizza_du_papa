from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from app.db import Base


class Pizza(Base):
    """Modèle de pizza."""
    __tablename__ = "pizzas"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)  # Base price
    is_available = Column(Boolean, default=True, nullable=False)
    
    # Relationship to pizza-size combinations
    pizza_sizes = relationship("PizzaSize", back_populates="pizza", cascade="all, delete-orphan")
