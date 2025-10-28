from app.models.stock import StockItem


def test_list_stock_items_empty(client):
    """Test liste des items de stock quand vide."""
    response = client.get("/stocks/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_stock_item_api(client, db):
    """Test création d'un item de stock via l'API."""
    stock_data = {
        "ingredient": "dough",
        "quantity": 50
    }
    response = client.post("/stocks/", json=stock_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["ingredient"] == "dough"
    assert data["quantity"] == 50
    assert "id" in data


def test_list_stock_items_api(client, db):
    """Test liste de tous les items de stock via l'API."""
    items = [
        StockItem(ingredient="tomato", quantity=40),
        StockItem(ingredient="mozzarella", quantity=60),
    ]
    db.add_all(items)
    db.commit()
    
    response = client.get("/stocks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_adjust_stock_quantity_api(client, db):
    """Test ajustement de quantité via l'API."""
    stock_item = StockItem(ingredient="pepperoni", quantity=30)
    db.add(stock_item)
    db.commit()
    db.refresh(stock_item)
    
    # Augmenter
    response = client.patch(f"/stocks/{stock_item.id}", json={"quantity": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 40
    
    # Diminuer
    response = client.patch(f"/stocks/{stock_item.id}", json={"quantity": -5})
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 35


def test_adjust_stock_negative_error_api(client, db):
    """Test ajustement menant à une quantité négative."""
    stock_item = StockItem(ingredient="ham", quantity=10)
    db.add(stock_item)
    db.commit()
    db.refresh(stock_item)
    
    response = client.patch(f"/stocks/{stock_item.id}", json={"quantity": -15})
    assert response.status_code == 400
    assert "négative" in response.json()["detail"]


def test_adjust_stock_not_found_api(client):
    """Test ajustement d'un item inexistant."""
    response = client.patch("/stocks/999", json={"quantity": 5})
    assert response.status_code == 404
