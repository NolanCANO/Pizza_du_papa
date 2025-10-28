import pytest
from app.models.stock import StockItem
from app.services import stock_service
from app.schemas.stock import StockItemCreate


def test_get_all_stock_items_empty(db):
    """Test récupération de tous les items de stock quand vide."""
    items = stock_service.get_all_stock_items(db)
    assert items == []


def test_create_stock_item(db):
    """Test création d'un item de stock."""
    stock_data = StockItemCreate(ingredient="dough", quantity=50)
    stock_item = stock_service.create_stock_item(db, stock_data)
    
    assert stock_item.id is not None
    assert stock_item.ingredient == "dough"
    assert stock_item.quantity == 50


def test_get_stock_item_by_id(db):
    """Test récupération d'un item de stock par ID."""
    stock_item = StockItem(ingredient="tomato", quantity=40)
    db.add(stock_item)
    db.commit()
    db.refresh(stock_item)
    
    found_item = stock_service.get_stock_item_by_id(db, stock_item.id)
    assert found_item is not None
    assert found_item.ingredient == "tomato"


def test_get_stock_item_by_ingredient(db):
    """Test récupération d'un item de stock par ingrédient."""
    stock_item = StockItem(ingredient="mozzarella", quantity=60)
    db.add(stock_item)
    db.commit()
    
    found_item = stock_service.get_stock_item_by_ingredient(db, "mozzarella")
    assert found_item is not None
    assert found_item.quantity == 60


def test_adjust_stock_quantity_increase(db):
    """Test ajustement de quantité en augmentation."""
    stock_item = StockItem(ingredient="pepperoni", quantity=30)
    db.add(stock_item)
    db.commit()
    db.refresh(stock_item)
    
    adjusted_item = stock_service.adjust_stock_quantity(db, stock_item.id, 10)
    assert adjusted_item.quantity == 40


def test_adjust_stock_quantity_decrease(db):
    """Test ajustement de quantité en diminution."""
    stock_item = StockItem(ingredient="ham", quantity=25)
    db.add(stock_item)
    db.commit()
    db.refresh(stock_item)
    
    adjusted_item = stock_service.adjust_stock_quantity(db, stock_item.id, -5)
    assert adjusted_item.quantity == 20


def test_adjust_stock_quantity_negative_error(db):
    """Test ajustement qui mènerait à une quantité négative."""
    stock_item = StockItem(ingredient="mushrooms", quantity=10)
    db.add(stock_item)
    db.commit()
    db.refresh(stock_item)
    
    with pytest.raises(ValueError, match="La quantité ne peut pas être négative"):
        stock_service.adjust_stock_quantity(db, stock_item.id, -15)


def test_decrement_stock(db):
    """Test décrémentation de stock."""
    stock_item = StockItem(ingredient="gorgonzola", quantity=20)
    db.add(stock_item)
    db.commit()
    
    stock_service.decrement_stock(db, "gorgonzola", 5)
    
    # Vérifier la nouvelle quantité
    updated_item = stock_service.get_stock_item_by_ingredient(db, "gorgonzola")
    assert updated_item.quantity == 15


def test_decrement_stock_insufficient(db):
    """Test décrémentation avec stock insuffisant."""
    stock_item = StockItem(ingredient="parmesan", quantity=5)
    db.add(stock_item)
    db.commit()
    
    with pytest.raises(ValueError, match="Stock insuffisant"):
        stock_service.decrement_stock(db, "parmesan", 10)


def test_decrement_stock_ingredient_not_found(db):
    """Test décrémentation d'un ingrédient inexistant."""
    with pytest.raises(ValueError, match="introuvable"):
        stock_service.decrement_stock(db, "nonexistent", 5)


def test_stock_logging(db, caplog):
    """Test que les logs sont émis lors des opérations sur le stock."""
    stock_item = StockItem(ingredient="emmental", quantity=20)
    db.add(stock_item)
    db.commit()
    db.refresh(stock_item)
    
    # Ajuster le stock
    stock_service.adjust_stock_quantity(db, stock_item.id, 5)
    
    # Vérifier les logs
    assert "Stock ajusté: emmental" in caplog.text
    assert "+5" in caplog.text
