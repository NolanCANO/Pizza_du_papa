from app.models.pizza import Pizza
from app.services import pizza_service
from app.schemas.pizza import PizzaCreate, PizzaUpdate


def test_get_all_pizzas_empty(db):
    """Test récupération de toutes les pizzas quand la DB est vide."""
    pizzas = pizza_service.get_all_pizzas(db)
    assert pizzas == []


def test_create_pizza(db):
    """Test création d'une pizza."""
    pizza_data = PizzaCreate(
        name="Margherita",
        description="Tomate, mozzarella, basilic",
        price=8.50,
        is_available=True
    )
    pizza = pizza_service.create_pizza(db, pizza_data)
    
    assert pizza.id is not None
    assert pizza.name == "Margherita"
    assert pizza.description == "Tomate, mozzarella, basilic"
    assert pizza.price == 8.50
    assert pizza.is_available is True


def test_get_pizza_by_id(db):
    """Test récupération d'une pizza par ID."""
    # Créer une pizza
    pizza = Pizza(name="Pepperoni", description="Tomate, mozzarella, pepperoni", price=10.00)
    db.add(pizza)
    db.commit()
    db.refresh(pizza)
    
    # Récupérer la pizza
    found_pizza = pizza_service.get_pizza_by_id(db, pizza.id)
    assert found_pizza is not None
    assert found_pizza.id == pizza.id
    assert found_pizza.name == "Pepperoni"


def test_get_pizza_by_id_not_found(db):
    """Test récupération d'une pizza inexistante."""
    pizza = pizza_service.get_pizza_by_id(db, 999)
    assert pizza is None


def test_update_pizza(db):
    """Test mise à jour d'une pizza."""
    # Créer une pizza
    pizza = Pizza(name="Reine", description="Base", price=11.00, is_available=True)
    db.add(pizza)
    db.commit()
    db.refresh(pizza)
    
    # Mettre à jour
    update_data = PizzaUpdate(price=11.50, is_available=False)
    updated_pizza = pizza_service.update_pizza(db, pizza.id, update_data)
    
    assert updated_pizza is not None
    assert updated_pizza.price == 11.50
    assert updated_pizza.is_available is False
    assert updated_pizza.name == "Reine"  # Inchangé


def test_delete_pizza(db):
    """Test suppression d'une pizza."""
    # Créer une pizza
    pizza = Pizza(name="4 Fromages", description="Fromages", price=12.00)
    db.add(pizza)
    db.commit()
    db.refresh(pizza)
    pizza_id = pizza.id
    
    # Supprimer
    success = pizza_service.delete_pizza(db, pizza_id)
    assert success is True
    
    # Vérifier que la pizza n'existe plus
    deleted_pizza = pizza_service.get_pizza_by_id(db, pizza_id)
    assert deleted_pizza is None


def test_delete_pizza_not_found(db):
    """Test suppression d'une pizza inexistante."""
    success = pizza_service.delete_pizza(db, 999)
    assert success is False
