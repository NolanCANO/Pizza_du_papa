from sqlalchemy.orm import Session
from app.models.pizza import Pizza
from app.schemas.pizza import PizzaCreate, PizzaUpdate


def get_all_pizzas(db: Session) -> list[Pizza]:
    """Récupère toutes les pizzas."""
    return db.query(Pizza).all()


def get_pizza_by_id(db: Session, pizza_id: int) -> Pizza | None:
    """Récupère une pizza par son ID."""
    return db.query(Pizza).filter(Pizza.id == pizza_id).first()


def create_pizza(db: Session, pizza_data: PizzaCreate) -> Pizza:
    """Crée une nouvelle pizza."""
    pizza = Pizza(**pizza_data.model_dump())
    db.add(pizza)
    db.commit()
    db.refresh(pizza)
    return pizza


def update_pizza(db: Session, pizza_id: int, pizza_data: PizzaUpdate) -> Pizza | None:
    """Met à jour une pizza."""
    pizza = get_pizza_by_id(db, pizza_id)
    if not pizza:
        return None
    
    update_data = pizza_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(pizza, key, value)
    
    db.commit()
    db.refresh(pizza)
    return pizza


def delete_pizza(db: Session, pizza_id: int) -> bool:
    """Supprime une pizza."""
    pizza = get_pizza_by_id(db, pizza_id)
    if not pizza:
        return False
    
    db.delete(pizza)
    db.commit()
    return True
