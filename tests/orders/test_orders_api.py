from app.models.pizza import Pizza
from app.models.stock import StockItem
from app.models.order import Order


def test_create_order_api(client, db):
    """Test création d'une commande via l'API."""
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
    order_data = {
        "customer_name": "Jean Dupont",
        "delivery_address": "123 Rue Test",
        "items": [
            {"pizza_id": pizza.id, "quantity": 2}
        ]
    }
    
    response = client.post("/orders/", json=order_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "Jean Dupont"
    assert data["total_price"] == 17.00
    assert data["status"] == "PENDING"
    assert len(data["items"]) == 1


def test_create_order_insufficient_stock_api(client, db):
    """Test création de commande avec stock insuffisant via l'API."""
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
    
    order_data = {
        "customer_name": "Jean Dupont",
        "delivery_address": "123 Rue Test",
        "items": [
            {"pizza_id": pizza.id, "quantity": 5}
        ]
    }
    
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 400
    assert "Stock insuffisant" in response.json()["detail"]


def test_get_order_api(client, db):
    """Test récupération d'une commande via l'API."""
    order = Order(
        customer_name="Jean Dupont",
        delivery_address="123 Rue Test",
        total_price=20.00,
        status="PENDING"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    response = client.get(f"/orders/{order.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order.id
    assert data["customer_name"] == "Jean Dupont"


def test_get_order_not_found_api(client):
    """Test récupération d'une commande inexistante."""
    response = client.get("/orders/999")
    assert response.status_code == 404


def test_list_orders_api(client, db):
    """Test liste de toutes les commandes via l'API."""
    orders = [
        Order(customer_name="Client 1", delivery_address="Addr 1", total_price=10.0, status="PENDING"),
        Order(customer_name="Client 2", delivery_address="Addr 2", total_price=15.0, status="PREPARING"),
    ]
    db.add_all(orders)
    db.commit()
    
    response = client.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_list_orders_by_status_api(client, db):
    """Test filtrage des commandes par statut via l'API."""
    orders = [
        Order(customer_name="Client 1", delivery_address="Addr 1", total_price=10.0, status="PENDING"),
        Order(customer_name="Client 2", delivery_address="Addr 2", total_price=15.0, status="PREPARING"),
        Order(customer_name="Client 3", delivery_address="Addr 3", total_price=20.0, status="PENDING"),
    ]
    db.add_all(orders)
    db.commit()
    
    response = client.get("/orders/?status=PENDING")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_update_order_status_api(client, db):
    """Test mise à jour du statut d'une commande via l'API."""
    order = Order(
        customer_name="Jean Dupont",
        delivery_address="123 Rue Test",
        total_price=20.00,
        status="PENDING"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    response = client.patch(f"/orders/{order.id}/status", json={"status": "PREPARING"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "PREPARING"


def test_cancel_order_api(client, db):
    """Test annulation d'une commande via l'API."""
    order = Order(
        customer_name="Jean Dupont",
        delivery_address="123 Rue Test",
        total_price=20.00,
        status="PENDING"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    response = client.post(f"/orders/{order.id}/cancel")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "CANCELLED"


def test_cancel_order_already_delivered_api(client, db):
    """Test annulation d'une commande déjà livrée via l'API."""
    order = Order(
        customer_name="Jean Dupont",
        delivery_address="123 Rue Test",
        total_price=20.00,
        status="DELIVERED"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    response = client.post(f"/orders/{order.id}/cancel")
    assert response.status_code == 400
