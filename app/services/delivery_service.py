from sqlalchemy.orm import Session
from app.models.delivery import Delivery
from app.models.order import Order
from app.schemas.delivery import DeliveryCreate, DeliveryStatusUpdate
from app.logging_config import logger


def get_delivery_by_id(db: Session, delivery_id: int) -> Delivery | None:
    """Récupère une livraison par son ID."""
    return db.query(Delivery).filter(Delivery.id == delivery_id).first()


def get_delivery_by_order_id(db: Session, order_id: int) -> Delivery | None:
    """Récupère une livraison par l'ID de commande."""
    return db.query(Delivery).filter(Delivery.order_id == order_id).first()


def create_delivery(db: Session, delivery_data: DeliveryCreate) -> Delivery:
    """Crée une nouvelle livraison."""
    # Vérifier que la commande existe
    order = db.query(Order).filter(Order.id == delivery_data.order_id).first()
    if not order:
        raise ValueError(f"Commande avec ID {delivery_data.order_id} introuvable")
    
    # Vérifier qu'il n'y a pas déjà une livraison pour cette commande
    existing_delivery = get_delivery_by_order_id(db, delivery_data.order_id)
    if existing_delivery:
        raise ValueError(f"Une livraison existe déjà pour la commande {delivery_data.order_id}")
    
    # Créer la livraison
    delivery = Delivery(**delivery_data.model_dump())
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    
    logger.info(f"Livraison créée: ID={delivery.id}, commande={delivery.order_id}, livreur={delivery.assigned_driver}")
    
    return delivery


def update_delivery_status(db: Session, delivery_id: int, status_data: DeliveryStatusUpdate) -> Delivery | None:
    """Met à jour le statut d'une livraison et propage à la commande."""
    delivery = get_delivery_by_id(db, delivery_id)
    if not delivery:
        return None
    
    old_status = delivery.status
    delivery.status = status_data.status
    
    if status_data.eta_minutes is not None:
        delivery.eta_minutes = status_data.eta_minutes
    
    # Propager le statut à la commande
    order = db.query(Order).filter(Order.id == delivery.order_id).first()
    if order:
        if delivery.status == "PICKED_UP":
            order.status = "OUT_FOR_DELIVERY"
            logger.info(f"Commande {order.id}: statut → OUT_FOR_DELIVERY (livraison récupérée)")
        elif delivery.status == "DELIVERED":
            order.status = "DELIVERED"
            logger.info(f"Commande {order.id}: statut → DELIVERED (livraison terminée)")
    
    db.commit()
    db.refresh(delivery)
    
    logger.info(f"Livraison {delivery_id}: statut {old_status} → {delivery.status}")
    
    return delivery
