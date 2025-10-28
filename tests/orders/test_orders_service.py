import pytest
from app.models.pizza import Pizza
from app.models.stock import StockItem
from app.models.order import Order
from app.services import order_service
from app.schemas.order import OrderCreate, OrderItemCreate, OrderStatusUpdate


def test_get_order_by_id(db):
    """Test récupération d'une commande par ID."""
    order = Order(
        customer_name="Jean Dupont",
        delivery_address="123 Rue Test",
        total_price=20.00,
        status="PENDING"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    found_order = order_service.get_order_by_id(db, order.id)
    assert found_order is not None
    assert found_order.customer_name == "Jean Dupont"


def test_get_orders_by_status(db):
    """Test récupération des commandes par statut."""
    orders = [
        Order(customer_name="Client 1", delivery_address="Addr 1", total_price=10.0, status="PENDING"),
        Order(customer_name="Client 2", delivery_address="Addr 2", total_price=15.0, status="PREPARING"),
        Order(customer_name="Client 3", delivery_address="Addr 3", total_price=20.0, status="PENDING"),
    ]
    db.add_all(orders)
    db.commit()
    
    pending_orders = order_service.get_orders_by_status(db, "PENDING")
    assert len(pending_orders) == 2
    
    all_orders = order_service.get_orders_by_status(db, None)
    assert len(all_orders) == 3


def test_create_order_success(db):
    """Test création d'une commande avec décrémentation du stock."""
    # Préparer la base
    pizza = Pizza(name="Margherita", description="Base", price=8.50, is_available=True)
    db.add(pizza)
    db.commit()
    db.refresh(pizza)
    
    stock_items = [
        StockItem(ingredient="dough", quantity=10),
        StockItem(ingredient="tomato", quantity=10),
        StockItem(ingredient="mozzarella", quantity=10),
    ]
    db.add_all(stock_items)
    db.commit()
    
    # Créer la commande
    order_data = OrderCreate(
        customer_name="Jean Dupont",
        delivery_address="123 Rue Test",
        items=[OrderItemCreate(pizza_id=pizza.id, quantity=2)]
    )
    
    order = order_service.create_order(db, order_data)
    
    assert order.id is not None
    assert order.total_price == 17.00  # 8.50 * 2
    assert order.status == "PENDING"
    assert len(order.items) == 1
    
    # Vérifier le stock décrémenté
    dough_stock = db.query(StockItem).filter(StockItem.ingredient == "dough").first()
    assert dough_stock.quantity == 8  # 10 - (1*2)


def test_create_order_insufficient_stock(db):
    """Test création de commande avec stock insuffisant."""
    pizza = Pizza(name="Pepperoni", description="Base", price=10.00, is_available=True)
    db.add(pizza)
    db.commit()
    db.refresh(pizza)
    
    stock_items = [
        StockItem(ingredient="dough", quantity=1),
        StockItem(ingredient="tomato", quantity=10),
        StockItem(ingredient="mozzarella", quantity=10),
        StockItem(ingredient="pepperoni", quantity=10),
    ]
    db.add_all(stock_items)
    db.commit()
    
    order_data = OrderCreate(
        customer_name="Jean Dupont",
        delivery_address="123 Rue Test",
        items=[OrderItemCreate(pizza_id=pizza.id, quantity=5)]
    )
    
    with pytest.raises(ValueError, match="Stock insuffisant"):
        order_service.create_order(db, order_data)


def test_create_order_pizza_not_found(db):
    """Test création de commande avec pizza inexistante."""
    order_data = OrderCreate(
        customer_name="Jean Dupont",
        delivery_address="123 Rue Test",
        items=[OrderItemCreate(pizza_id=999, quantity=1)]
    )
    
    with pytest.raises(ValueError, match="introuvable"):
        order_service.create_order(db, order_data)


def test_create_order_pizza_not_available(db):
    """Test création de commande avec pizza indisponible."""
    pizza = Pizza(name="Reine", description="Base", price=11.50, is_available=False)
    db.add(pizza)
    db.commit()
    db.refresh(pizza)
    
    order_data = OrderCreate(
        customer_name="Jean Dupont",
        delivery_address="123 Rue Test",
        items=[OrderItemCreate(pizza_id=pizza.id, quantity=1)]
    )
    
    with pytest.raises(ValueError, match="non disponible"):
        order_service.create_order(db, order_data)


def test_create_order_calculates_total(db):
    """Test que le total est correctement calculé."""
    pizzas = [
        Pizza(name="Margherita", description="Base", price=8.50, is_available=True),
        Pizza(name="Pepperoni", description="Base", price=10.00, is_available=True),
    ]
    db.add_all(pizzas)
    db.commit()
    
    # Ajouter du stock
    stock_items = [
        StockItem(ingredient="dough", quantity=50),
        StockItem(ingredient="tomato", quantity=50),
        StockItem(ingredient="mozzarella", quantity=50),
        StockItem(ingredient="pepperoni", quantity=50),
    ]
    db.add_all(stock_items)
    db.commit()
    
    order_data = OrderCreate(
        customer_name="Jean Dupont",
        delivery_address="123 Rue Test",
        items=[
            OrderItemCreate(pizza_id=pizzas[0].id, quantity=2),
            OrderItemCreate(pizza_id=pizzas[1].id, quantity=1),
        ]
    )
    
    order = order_service.create_order(db, order_data)
    assert order.total_price == 27.00  # (8.50*2) + (10.00*1)


def test_update_order_status(db):
    """Test mise à jour du statut d'une commande."""
    order = Order(
        customer_name="Jean Dupont",
        delivery_address="123 Rue Test",
        total_price=20.00,
        status="PENDING"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    status_update = OrderStatusUpdate(status="PREPARING")
    updated_order = order_service.update_order_status(db, order.id, status_update)
    
    assert updated_order.status == "PREPARING"


def test_cancel_order_success(db):
    """Test annulation d'une commande."""
    order = Order(
        customer_name="Jean Dupont",
        delivery_address="123 Rue Test",
        total_price=20.00,
        status="PENDING"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    cancelled_order = order_service.cancel_order(db, order.id)
    assert cancelled_order.status == "CANCELLED"


def test_cancel_order_already_delivered(db):
    """Test annulation d'une commande déjà livrée."""
    order = Order(
        customer_name="Jean Dupont",
        delivery_address="123 Rue Test",
        total_price=20.00,
        status="DELIVERED"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    with pytest.raises(ValueError, match="déjà livrée"):
        order_service.cancel_order(db, order.id)


def test_order_logging(db, caplog):
    """Test que les logs sont émis lors de la création de commande."""
    pizza = Pizza(name="Margherita", description="Base", price=8.50, is_available=True)
    db.add(pizza)
    db.commit()
    db.refresh(pizza)
    
    stock_items = [
        StockItem(ingredient="dough", quantity=10),
        StockItem(ingredient="tomato", quantity=10),
        StockItem(ingredient="mozzarella", quantity=10),
    ]
    db.add_all(stock_items)
    db.commit()
    
    order_data = OrderCreate(
        customer_name="Jean Dupont",
        delivery_address="123 Rue Test",
        items=[OrderItemCreate(pizza_id=pizza.id, quantity=1)]
    )
    
    order = order_service.create_order(db, order_data)
    
    # Vérifier les logs
    assert "Commande créée" in caplog.text
    assert "Jean Dupont" in caplog.text
