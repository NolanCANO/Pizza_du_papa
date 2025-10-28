# Pizzeria API

API backend pour une application mobile de pizzeria, développée avec FastAPI et suivant la méthodologie TDD.

## Prérequis

- Python 3.12+
- pip
- Docker et Docker Compose (optionnel)

## Installation

1. Cloner le dépôt
2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Démarrage de l'application

### En local

```bash
uvicorn app.main:app --reload
```

L'API sera accessible sur `http://localhost:8000`

Documentation OpenAPI : `http://localhost:8000/docs`

### Avec Docker

```bash
docker-compose up --build
```

## Exécution des tests

```bash
pytest
```

Pour voir la couverture des logs :

```bash
pytest -v
```

## Variables d'environnement

Aucune variable d'environnement critique n'est requise. Tout fonctionne avec des valeurs par défaut.

## Structure du projet

- `app/` : Code source de l'application
  - `models/` : Modèles SQLAlchemy
  - `schemas/` : Schémas Pydantic
  - `services/` : Logique métier
  - `routers/` : Endpoints FastAPI
- `tests/` : Tests unitaires et d'intégration
- `logs/` : Fichiers de logs (créé automatiquement)

## Endpoints principaux

- `GET /health` : Health check
- `GET /pizzas` : Liste des pizzas
- `POST /orders` : Créer une commande
- `GET /stocks` : Consulter les stocks
- `POST /deliveries` : Créer une livraison

Voir `/docs` pour la documentation complète.