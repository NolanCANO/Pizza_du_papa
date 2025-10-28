import pytest
from app.models.order import Order
from app.models.delivery import Delivery
from app.services import delivery_service
from app.schemas.delivery import DeliveryCreate, DeliveryStatusUpdate


def test_get_delivery_by_id(db):
    """Test récupération d'une livraison par ID."""
    order = Order(customer_name="Client", delivery_address="Addr", total_price=20.0, status="PENDING")
    db.add(order)
    db.commit()
    db.refresh(order)
    
    delivery = Delivery(order_id=order.id, assigned_driver="Pierre", eta_minutes=30, status="ASSIGNED")
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    
    found_delivery = delivery_service.get_delivery_by_id(db, delivery.id)
    assert found_delivery is not None
    assert found_delivery.assigned_driver == "Pierre"


def test_get_delivery_by_order_id(db):
    """Test récupération d'une livraison par ID de commande."""
    order = Order(customer_name="Client", delivery_address="Addr", total_price=20.0, status="PENDING")
    db.add(order)
    db.commit()
    db.refresh(order)
    
    delivery = Delivery(order_id=order.id, assigned_driver="Marie", eta_minutes=25, status="ASSIGNED")
    db.add(delivery)
    db.commit()
    
    found_delivery = delivery_service.get_delivery_by_order_id(db, order.id)
    assert found_delivery is not None
    assert found_delivery.assigned_driver == "Marie"


def test_create_delivery(db):
    """Test création d'une livraison."""
    order = Order(customer_name="Client", delivery_address="Addr", total_price=20.0, status="PENDING")
    db.add(order)
    db.commit()
    db.refresh(order)
    
    delivery_data = DeliveryCreate(
        order_id=order.id,
        assigned_driver="Jean",
        eta_minutes=30
    )
    
    delivery = delivery_service.create_delivery(db, delivery_data)
    
    assert delivery.id is not None
    assert delivery.order_id == order.id
    assert delivery.assigned_driver == "Jean"
    assert delivery.eta_minutes == 30
    assert delivery.status == "ASSIGNED"


def test_create_delivery_order_not_found(db):
    """Test création d'une livraison pour une commande inexistante."""
    delivery_data = DeliveryCreate(
        order_id=999,
        assigned_driver="Jean",
        eta_minutes=30
    )
    
    with pytest.raises(ValueError, match="introuvable"):
        delivery_service.create_delivery(db, delivery_data)


def test_create_delivery_already_exists(db):
    """Test création d'une livraison quand une existe déjà."""
    order = Order(customer_name="Client", delivery_address="Addr", total_price=20.0, status="PENDING")
    db.add(order)
    db.commit()
    db.refresh(order)
    
    delivery1 = Delivery(order_id=order.id, assigned_driver="Pierre", eta_minutes=30, status="ASSIGNED")
    db.add(delivery1)
    db.commit()
    
    delivery_data = DeliveryCreate(
        order_id=order.id,
        assigned_driver="Marie",
        eta_minutes=25
    )
    
    with pytest.raises(ValueError, match="existe déjà"):
        delivery_service.create_delivery(db, delivery_data)


def test_update_delivery_status_to_picked_up(db):
    """Test mise à jour du statut de livraison à PICKED_UP."""
    order = Order(customer_name="Client", delivery_address="Addr", total_price=20.0, status="PREPARING")
    db.add(order)
    db.commit()
    db.refresh(order)
    
    delivery = Delivery(order_id=order.id, assigned_driver="Pierre", eta_minutes=30, status="ASSIGNED")
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    
    status_update = DeliveryStatusUpdate(status="PICKED_UP")
    updated_delivery = delivery_service.update_delivery_status(db, delivery.id, status_update)
    
    assert updated_delivery.status == "PICKED_UP"
    
    # Vérifier que le statut de la commande a été mis à jour
    db.refresh(order)
    assert order.status == "OUT_FOR_DELIVERY"


def test_update_delivery_status_to_delivered(db):
    """Test mise à jour du statut de livraison à DELIVERED."""
    order = Order(customer_name="Client", delivery_address="Addr", total_price=20.0, status="OUT_FOR_DELIVERY")
    db.add(order)
    db.commit()
    db.refresh(order)
    
    delivery = Delivery(order_id=order.id, assigned_driver="Marie", eta_minutes=15, status="PICKED_UP")
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    
    status_update = DeliveryStatusUpdate(status="DELIVERED")
    updated_delivery = delivery_service.update_delivery_status(db, delivery.id, status_update)
    
    assert updated_delivery.status == "DELIVERED"
    
    # Vérifier que le statut de la commande a été mis à jour
    db.refresh(order)
    assert order.status == "DELIVERED"


def test_update_delivery_status_with_eta(db):
    """Test mise à jour du statut avec changement d'ETA."""
    order = Order(customer_name="Client", delivery_address="Addr", total_price=20.0, status="PENDING")
    db.add(order)
    db.commit()
    db.refresh(order)
    
    delivery = Delivery(order_id=order.id, assigned_driver="Jean", eta_minutes=30, status="ASSIGNED")
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    
    status_update = DeliveryStatusUpdate(status="PICKED_UP", eta_minutes=20)
    updated_delivery = delivery_service.update_delivery_status(db, delivery.id, status_update)
    
    assert updated_delivery.eta_minutes == 20


def test_delivery_logging(db, caplog):
    """Test que les logs sont émis lors des opérations de livraison."""
    order = Order(customer_name="Client", delivery_address="Addr", total_price=20.0, status="PENDING")
    db.add(order)
    db.commit()
    db.refresh(order)
    
    delivery_data = DeliveryCreate(
        order_id=order.id,
        assigned_driver="Jean",
        eta_minutes=30
    )
    
    delivery = delivery_service.create_delivery(db, delivery_data)
    
    # Vérifier les logs de création
    assert "Livraison créée" in caplog.text
    assert "Jean" in caplog.text
    
    # Mise à jour du statut
    status_update = DeliveryStatusUpdate(status="PICKED_UP")
    delivery_service.update_delivery_status(db, delivery.id, status_update)
    
    # Vérifier les logs de transition
    assert "OUT_FOR_DELIVERY" in caplog.text
