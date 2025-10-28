from app.models.order import Order
from app.models.delivery import Delivery


def test_create_delivery_api(client, db):
    """Test création d'une livraison via l'API."""
    order = Order(customer_name="Client", delivery_address="Addr", total_price=20.0, status="PENDING")
    db.add(order)
    db.commit()
    db.refresh(order)
    
    delivery_data = {
        "order_id": order.id,
        "assigned_driver": "Pierre",
        "eta_minutes": 30
    }
    
    response = client.post("/deliveries/", json=delivery_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["order_id"] == order.id
    assert data["assigned_driver"] == "Pierre"
    assert data["eta_minutes"] == 30
    assert data["status"] == "ASSIGNED"


def test_create_delivery_order_not_found_api(client):
    """Test création d'une livraison pour une commande inexistante."""
    delivery_data = {
        "order_id": 999,
        "assigned_driver": "Pierre",
        "eta_minutes": 30
    }
    
    response = client.post("/deliveries/", json=delivery_data)
    assert response.status_code == 400
    assert "introuvable" in response.json()["detail"]


def test_create_delivery_already_exists_api(client, db):
    """Test création d'une livraison quand une existe déjà."""
    order = Order(customer_name="Client", delivery_address="Addr", total_price=20.0, status="PENDING")
    db.add(order)
    db.commit()
    db.refresh(order)
    
    delivery = Delivery(order_id=order.id, assigned_driver="Pierre", eta_minutes=30, status="ASSIGNED")
    db.add(delivery)
    db.commit()
    
    delivery_data = {
        "order_id": order.id,
        "assigned_driver": "Marie",
        "eta_minutes": 25
    }
    
    response = client.post("/deliveries/", json=delivery_data)
    assert response.status_code == 400
    assert "existe déjà" in response.json()["detail"]


def test_get_delivery_api(client, db):
    """Test récupération d'une livraison via l'API."""
    order = Order(customer_name="Client", delivery_address="Addr", total_price=20.0, status="PENDING")
    db.add(order)
    db.commit()
    db.refresh(order)
    
    delivery = Delivery(order_id=order.id, assigned_driver="Marie", eta_minutes=25, status="ASSIGNED")
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    
    response = client.get(f"/deliveries/{delivery.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == delivery.id
    assert data["assigned_driver"] == "Marie"


def test_get_delivery_not_found_api(client):
    """Test récupération d'une livraison inexistante."""
    response = client.get("/deliveries/999")
    assert response.status_code == 404


def test_update_delivery_status_api(client, db):
    """Test mise à jour du statut d'une livraison via l'API."""
    order = Order(customer_name="Client", delivery_address="Addr", total_price=20.0, status="PREPARING")
    db.add(order)
    db.commit()
    db.refresh(order)
    
    delivery = Delivery(order_id=order.id, assigned_driver="Jean", eta_minutes=30, status="ASSIGNED")
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    
    response = client.patch(f"/deliveries/{delivery.id}/status", json={"status": "PICKED_UP"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "PICKED_UP"
    
    # Vérifier que la commande a été mise à jour
    db.refresh(order)
    assert order.status == "OUT_FOR_DELIVERY"


def test_update_delivery_status_with_eta_api(client, db):
    """Test mise à jour du statut avec ETA via l'API."""
    order = Order(customer_name="Client", delivery_address="Addr", total_price=20.0, status="PENDING")
    db.add(order)
    db.commit()
    db.refresh(order)
    
    delivery = Delivery(order_id=order.id, assigned_driver="Pierre", eta_minutes=30, status="ASSIGNED")
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    
    response = client.patch(f"/deliveries/{delivery.id}/status", json={"status": "PICKED_UP", "eta_minutes": 20})
    assert response.status_code == 200
    data = response.json()
    assert data["eta_minutes"] == 20


def test_delivery_full_cycle_api(client, db):
    """Test cycle complet de livraison avec propagation des statuts."""
    # Créer une commande
    order = Order(customer_name="Client", delivery_address="Addr", total_price=20.0, status="PREPARING")
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # Créer une livraison
    delivery_data = {
        "order_id": order.id,
        "assigned_driver": "Jean",
        "eta_minutes": 30
    }
    response = client.post("/deliveries/", json=delivery_data)
    assert response.status_code == 201
    delivery_id = response.json()["id"]
    
    # Passer à PICKED_UP
    response = client.patch(f"/deliveries/{delivery_id}/status", json={"status": "PICKED_UP"})
    assert response.status_code == 200
    db.refresh(order)
    assert order.status == "OUT_FOR_DELIVERY"
    
    # Passer à DELIVERED
    response = client.patch(f"/deliveries/{delivery_id}/status", json={"status": "DELIVERED"})
    assert response.status_code == 200
    db.refresh(order)
    assert order.status == "DELIVERED"
