from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base


class Size(Base):
    """Modèle de taille de pizza."""
    __tablename__ = "sizes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)  # e.g., "Small", "Medium", "Large"
    description = Column(String, nullable=True)  # e.g., "20cm", "25cm", "30cm"
    price_multiplier = Column(Float, nullable=False, default=1.0)  # Multiplier for base pizza price
    
    # Relationship to pizza-size specific prices
    pizza_sizes = relationship("PizzaSize", back_populates="size", cascade="all, delete-orphan")


class PizzaSize(Base):
    """Modèle de prix spécifique pour une combinaison pizza-taille."""
    __tablename__ = "pizza_sizes"
    
    id = Column(Integer, primary_key=True, index=True)
    pizza_id = Column(Integer, ForeignKey("pizzas.id"), nullable=False)
    size_id = Column(Integer, ForeignKey("sizes.id"), nullable=False)
    specific_price = Column(Float, nullable=True)  # If set, overrides base_price * multiplier
    is_available = Column(Boolean, default=True, nullable=False)
    
    # Ensure unique combination of pizza and size
    __table_args__ = (UniqueConstraint('pizza_id', 'size_id', name='unique_pizza_size'),)
    
    # Relationships
    pizza = relationship("Pizza", back_populates="pizza_sizes")
    size = relationship("Size", back_populates="pizza_sizes")
    
    @property
    def calculated_price(self):
        """Calculate the price for this pizza-size combination."""
        if self.specific_price is not None:
            return self.specific_price
        return self.pizza.price * self.size.price_multiplier