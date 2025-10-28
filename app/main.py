from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db import init_db, SessionLocal
from app.routers import pizzas, stocks, orders, deliveries, sizes
from app.models.pizza import Pizza
from app.models.stock import StockItem
from app.models.size import Size, PizzaSize
from app.logging_config import logger


def seed_database():
    """Insère les données initiales dans la base de données."""
    db = SessionLocal()
    try:
        # Vérifier si les données existent déjà
        if db.query(Pizza).count() > 0:
            logger.info("Base de données déjà initialisée, skip seed")
            return
        
        # Pizzas par défaut
        pizzas = [
            Pizza(name="Margherita", description="Tomate, mozzarella, basilic", price=8.50, is_available=True),
            Pizza(name="Pepperoni", description="Tomate, mozzarella, pepperoni", price=10.00, is_available=True),
            Pizza(name="Reine", description="Tomate, mozzarella, jambon, champignons", price=11.50, is_available=True),
            Pizza(name="4 Fromages", description="Mozzarella, gorgonzola, parmesan, emmental", price=12.00, is_available=True),
        ]
        db.add_all(pizzas)
        
        # Stock initial
        stock_items = [
            StockItem(ingredient="dough", quantity=50),
            StockItem(ingredient="tomato", quantity=40),
            StockItem(ingredient="mozzarella", quantity=60),
            StockItem(ingredient="pepperoni", quantity=30),
            StockItem(ingredient="ham", quantity=25),
            StockItem(ingredient="mushrooms", quantity=20),
            StockItem(ingredient="gorgonzola", quantity=15),
            StockItem(ingredient="parmesan", quantity=15),
            StockItem(ingredient="emmental", quantity=15),
        ]
        db.add_all(stock_items)
        
        # Tailles par défaut
        sizes = [
            Size(name="Small", description="20cm", price_multiplier=0.8),
            Size(name="Medium", description="25cm", price_multiplier=1.0),
            Size(name="Large", description="30cm", price_multiplier=1.3),
            Size(name="XL", description="35cm", price_multiplier=1.6),
        ]
        db.add_all(sizes)
        db.commit()  # Commit pour récupérer les IDs
        
        # Créer des combinaisons pizza-taille pour toutes les pizzas
        for pizza in pizzas:
            for size in sizes:
                pizza_size = PizzaSize(
                    pizza_id=pizza.id,
                    size_id=size.id,
                    is_available=True
                )
                db.add(pizza_size)
        
        db.commit()
        logger.info("Base de données initialisée avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation de la base de données: {e}")
        db.rollback()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gère le cycle de vie de l'application."""
    # Startup
    logger.info("Démarrage de l'application Pizzeria API")
    init_db()
    seed_database()
    yield
    # Shutdown
    logger.info("Arrêt de l'application Pizzeria API")


app = FastAPI(
    title="Pizzeria API",
    description="API pour une application mobile de pizzeria",
    version="1.0.0",
    lifespan=lifespan
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "http://localhost:4201",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrer les routers
app.include_router(pizzas.router)
app.include_router(stocks.router)
app.include_router(orders.router)
app.include_router(deliveries.router)
app.include_router(sizes.router)
app.include_router(sizes.pizza_sizes_router)


@app.get("/")
def root():
    """Page d'accueil de l'API."""
    return {
        "message": "Bienvenue sur l'API Pizzeria",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "health": "/health",
            "pizzas": "/pizzas",
            "stocks": "/stocks",
            "orders": "/orders",
            "deliveries": "/deliveries",
            "sizes": "/sizes",
            "pizza-sizes": "/pizza-sizes"
        }
    }


@app.get("/health")
def health_check():
    """Endpoint de health check."""
    return {"status": "ok"}
