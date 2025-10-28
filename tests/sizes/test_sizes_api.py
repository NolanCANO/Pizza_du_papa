import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import get_db, Base


# Base de données de test en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_size():
    """Test de création d'une taille."""
    response = client.post("/sizes/", json={
        "name": "Test Size",
        "description": "40cm",
        "price_multiplier": 1.5
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Size"
    assert data["description"] == "40cm"
    assert data["price_multiplier"] == 1.5


def test_get_sizes():
    """Test de récupération des tailles."""
    response = client.get("/sizes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_size_by_id():
    """Test de récupération d'une taille par ID."""
    # Créer une taille
    create_response = client.post("/sizes/", json={
        "name": "Test Size 2",
        "description": "45cm",
        "price_multiplier": 1.8
    })
    size_id = create_response.json()["id"]
    
    # Récupérer la taille
    response = client.get(f"/sizes/{size_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == size_id
    assert data["name"] == "Test Size 2"


def test_update_size():
    """Test de mise à jour d'une taille."""
    # Créer une taille
    create_response = client.post("/sizes/", json={
        "name": "Test Size 3",
        "description": "50cm",
        "price_multiplier": 2.0
    })
    size_id = create_response.json()["id"]
    
    # Mettre à jour la taille
    response = client.put(f"/sizes/{size_id}", json={
        "price_multiplier": 2.2
    })
    assert response.status_code == 200
    data = response.json()
    assert data["price_multiplier"] == 2.2


def test_delete_size():
    """Test de suppression d'une taille."""
    # Créer une taille
    create_response = client.post("/sizes/", json={
        "name": "Test Size 4",
        "description": "55cm",
        "price_multiplier": 2.5
    })
    size_id = create_response.json()["id"]
    
    # Supprimer la taille
    response = client.delete(f"/sizes/{size_id}")
    assert response.status_code == 204
    
    # Vérifier qu'elle n'existe plus
    get_response = client.get(f"/sizes/{size_id}")
    assert get_response.status_code == 404


def test_create_pizza_size():
    """Test de création d'une combinaison pizza-taille."""
    # Créer une pizza
    pizza_response = client.post("/pizzas/", json={
        "name": "Test Pizza Size",
        "description": "Pizza pour test de taille",
        "price": 10.0
    })
    pizza_id = pizza_response.json()["id"]
    
    # Créer une taille
    size_response = client.post("/sizes/", json={
        "name": "Test Size for Pizza",
        "description": "Test size",
        "price_multiplier": 1.3
    })
    size_id = size_response.json()["id"]
    
    # Créer la combinaison pizza-taille
    response = client.post("/pizza-sizes/", json={
        "pizza_id": pizza_id,
        "size_id": size_id,
        "specific_price": 15.0,
        "is_available": True
    })
    assert response.status_code == 201
    data = response.json()
    assert data["pizza_id"] == pizza_id
    assert data["size_id"] == size_id
    assert data["specific_price"] == 15.0
    assert data["calculated_price"] == 15.0  # Should use specific price


def test_pizza_size_price_calculation():
    """Test du calcul de prix pour une combinaison pizza-taille."""
    # Créer une pizza
    pizza_response = client.post("/pizzas/", json={
        "name": "Test Pizza Price Calc",
        "description": "Pizza pour test de calcul",
        "price": 12.0
    })
    pizza_id = pizza_response.json()["id"]
    
    # Créer une taille
    size_response = client.post("/sizes/", json={
        "name": "Medium Test",
        "description": "Medium size",
        "price_multiplier": 1.2
    })
    size_id = size_response.json()["id"]
    
    # Créer la combinaison pizza-taille sans prix spécifique
    response = client.post("/pizza-sizes/", json={
        "pizza_id": pizza_id,
        "size_id": size_id,
        "is_available": True
    })
    assert response.status_code == 201
    data = response.json()
    # Prix calculé = prix de base (12.0) * multiplicateur (1.2) = 14.4
    assert data["calculated_price"] == 14.4


def test_get_pizza_with_sizes():
    """Test de récupération d'une pizza avec ses tailles."""
    # Créer une pizza
    pizza_response = client.post("/pizzas/", json={
        "name": "Test Pizza with Sizes",
        "description": "Pizza avec tailles",
        "price": 8.0
    })
    pizza_id = pizza_response.json()["id"]
    
    # Récupérer la pizza avec ses tailles
    response = client.get(f"/pizzas/{pizza_id}/with-sizes")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == pizza_id
    assert "pizza_sizes" in data
    assert isinstance(data["pizza_sizes"], list)