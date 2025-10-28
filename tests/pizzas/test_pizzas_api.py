from app.models.pizza import Pizza


def test_list_pizzas_empty(client):
    """Test liste des pizzas quand vide."""
    response = client.get("/pizzas/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_pizza_api(client, db):
    """Test création d'une pizza via l'API."""
    pizza_data = {
        "name": "Margherita",
        "description": "Tomate, mozzarella, basilic",
        "price": 8.50,
        "is_available": True
    }
    response = client.post("/pizzas/", json=pizza_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Margherita"
    assert data["price"] == 8.50
    assert "id" in data


def test_get_pizza_api(client, db):
    """Test récupération d'une pizza via l'API."""
    # Créer une pizza
    pizza = Pizza(name="Pepperoni", description="Tomate, mozzarella, pepperoni", price=10.00)
    db.add(pizza)
    db.commit()
    db.refresh(pizza)
    
    # Récupérer via l'API
    response = client.get(f"/pizzas/{pizza.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == pizza.id
    assert data["name"] == "Pepperoni"


def test_get_pizza_not_found_api(client):
    """Test récupération d'une pizza inexistante."""
    response = client.get("/pizzas/999")
    assert response.status_code == 404


def test_update_pizza_api(client, db):
    """Test mise à jour d'une pizza via l'API."""
    # Créer une pizza
    pizza = Pizza(name="Reine", description="Base", price=11.00, is_available=True)
    db.add(pizza)
    db.commit()
    db.refresh(pizza)
    
    # Mettre à jour
    update_data = {"price": 11.50, "is_available": False}
    response = client.patch(f"/pizzas/{pizza.id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 11.50
    assert data["is_available"] is False


def test_delete_pizza_api(client, db):
    """Test suppression d'une pizza via l'API."""
    # Créer une pizza
    pizza = Pizza(name="4 Fromages", description="Fromages", price=12.00)
    db.add(pizza)
    db.commit()
    db.refresh(pizza)
    
    # Supprimer
    response = client.delete(f"/pizzas/{pizza.id}")
    assert response.status_code == 204
    
    # Vérifier que la pizza n'existe plus
    get_response = client.get(f"/pizzas/{pizza.id}")
    assert get_response.status_code == 404


def test_list_pizzas_api(client, db):
    """Test liste de toutes les pizzas via l'API."""
    # Créer quelques pizzas
    pizzas = [
        Pizza(name="Margherita", description="Base", price=8.50),
        Pizza(name="Pepperoni", description="Base", price=10.00),
    ]
    db.add_all(pizzas)
    db.commit()
    
    # Lister
    response = client.get("/pizzas/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Margherita"
    assert data[1]["name"] == "Pepperoni"
