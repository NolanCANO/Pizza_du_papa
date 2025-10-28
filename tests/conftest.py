import pytest
import os
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.db import Base, get_db
from app.routers import pizzas, stocks, orders, deliveries


@pytest.fixture(scope="function")
def test_db_file():
    """Crée un fichier de base de données temporaire."""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    yield db_path
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="function")
def test_engine(test_db_file):
    """Fixture pour créer un engine de test."""
    engine = create_engine(
        f"sqlite:///{test_db_file}",
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db(test_engine):
    """Fixture de session de base de données pour les tests."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db):
    """Fixture de client de test FastAPI."""
    # Créer une app de test sans lifespan
    test_app = FastAPI()
    test_app.include_router(pizzas.router)
    test_app.include_router(stocks.router)
    test_app.include_router(orders.router)
    test_app.include_router(deliveries.router)
    
    @test_app.get("/health")
    def health_check():
        return {"status": "ok"}
    
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    test_app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(test_app, raise_server_exceptions=True) as test_client:
        yield test_client
    test_app.dependency_overrides.clear()
