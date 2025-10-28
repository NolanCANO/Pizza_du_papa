from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.models.pizza import Pizza
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.services import stock_service
from app.logging_config import logger


# Mapping pizza → ingrédients
PIZZA_INGREDIENTS = {
    "Margherita": {"dough": 1, "tomato": 1, "mozzarella": 1},
    "Pepperoni": {"dough": 1, "tomato": 1, "mozzarella": 1, "pepperoni": 1},
    "Reine": {"dough": 1, "tomato": 1, "mozzarella": 1, "ham": 1, "mushrooms": 1},
    "4 Fromages": {"dough": 1, "mozzarella": 1, "gorgonzola": 1, "parmesan": 1, "emmental": 1}
}


def get_order_by_id(db: Session, order_id: int) -> Order | None:
    """Récupère une commande par son ID."""
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders_by_status(db: Session, status: str | None = None) -> list[Order]:
    """Récupère les commandes filtrées par statut."""
    query = db.query(Order)
    if status:
        query = query.filter(Order.status == status)
    return query.all()


def create_order(db: Session, order_data: OrderCreate) -> Order:
    """Crée une nouvelle commande avec gestion des stocks."""
    # Calculer le total et vérifier les stocks
    total_price = 0.0
    ingredients_needed = {}
    
    for item in order_data.items:
        pizza = db.query(Pizza).filter(Pizza.id == item.pizza_id).first()
        if not pizza:
            raise ValueError(f"Pizza avec ID {item.pizza_id} introuvable")
        
        if not pizza.is_available:
            raise ValueError(f"Pizza '{pizza.name}' non disponible")
        
        total_price += pizza.price * item.quantity
        
        # Calculer les ingrédients nécessaires
        if pizza.name in PIZZA_INGREDIENTS:
            for ingredient, qty_per_pizza in PIZZA_INGREDIENTS[pizza.name].items():
                ingredients_needed[ingredient] = ingredients_needed.get(ingredient, 0) + (qty_per_pizza * item.quantity)
    
    # Vérifier la disponibilité des stocks
    for ingredient, quantity_needed in ingredients_needed.items():
        stock_item = stock_service.get_stock_item_by_ingredient(db, ingredient)
        if not stock_item or stock_item.quantity < quantity_needed:
            available = stock_item.quantity if stock_item else 0
            raise ValueError(f"Stock insuffisant pour {ingredient}: disponible={available}, requis={quantity_needed}")
    
    # Décrémenter les stocks
    for ingredient, quantity_needed in ingredients_needed.items():
        stock_service.decrement_stock(db, ingredient, quantity_needed)
    
    # Créer la commande
    order = Order(
        customer_name=order_data.customer_name,
        delivery_address=order_data.delivery_address,
        total_price=total_price,
        status="PENDING"
    )
    db.add(order)
    db.flush()
    
    # Créer les items de commande
    for item_data in order_data.items:
        order_item = OrderItem(
            order_id=order.id,
            pizza_id=item_data.pizza_id,
            quantity=item_data.quantity
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(order)
    
    logger.info(f"Commande créée: ID={order.id}, client={order.customer_name}, total={order.total_price}€")
    
    return order


def update_order_status(db: Session, order_id: int, status_data: OrderStatusUpdate) -> Order | None:
    """Met à jour le statut d'une commande."""
    order = get_order_by_id(db, order_id)
    if not order:
        return None
    
    old_status = order.status
    order.status = status_data.status
    db.commit()
    db.refresh(order)
    
    logger.info(f"Commande {order_id}: statut {old_status} → {status_data.status}")
    
    return order


def cancel_order(db: Session, order_id: int) -> Order | None:
    """Annule une commande si elle n'est pas encore livrée."""
    order = get_order_by_id(db, order_id)
    if not order:
        return None
    
    if order.status == "DELIVERED":
        raise ValueError("Impossible d'annuler une commande déjà livrée")
    
    order.status = "CANCELLED"
    db.commit()
    db.refresh(order)
    
    logger.info(f"Commande {order_id} annulée")
    
    return order
