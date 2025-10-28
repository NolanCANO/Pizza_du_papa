# Pizzeria API

API backend pour une application mobile de pizzeria, développée avec **FastAPI** et suivant strictement la méthodologie **TDD (Test-Driven Development)**.

> **🚀 NOUVEAU SUR LE PROJET ?** → Consultez le **[Guide de Démarrage Rapide](DEMARRAGE.md)** pour lancer l'application en 5 minutes !

## 🎯 Fonctionnalités

### Gestion complète de pizzeria
- **Pizzas** : CRUD complet avec gestion de disponibilité
- **Stocks** : Suivi des ingrédients avec décrémentation automatique
- **Commandes** : Création avec calcul automatique du total et vérification des stocks
- **Livraisons** : Affectation de livreurs avec propagation de statut

### Points techniques
- ✅ **69 tests** (100% de réussite) couvrant API et services
- 🔄 **Gestion transactionnelle** avec rollback automatique
- 📝 **Logs structurés** avec rotation automatique
- 🗃️ **SQLite** avec SQLAlchemy (synchrone)
- 🔍 **Validation** complète via Pydantic
- 📚 **Documentation OpenAPI** interactive

## 📋 Prérequis

- **Python 3.12+**
- **pip** (gestionnaire de packages Python)
- **Docker & Docker Compose** (optionnel)

## 🚀 Installation

### 1. Cloner le dépôt
```bash
git clone <url-du-repo>
cd Pizza_du_papa
```

### 2. Créer un environnement virtuel (recommandé)
```bash
python -m venv .venv
```

**Activer l'environnement virtuel :**

- Windows (PowerShell) :
```powershell
.venv\Scripts\Activate.ps1
```

- Windows (CMD) :
```cmd
.venv\Scripts\activate.bat
```

- Linux/Mac :
```bash
source .venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

## ▶️ Démarrage de l'application

### En local (méthode recommandée)

**Important** : Si vous utilisez l'environnement virtuel, utilisez le chemin complet :

**Windows :**
```powershell
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

**Linux/Mac :**
```bash
python -m uvicorn app.main:app --reload
```

L'API sera accessible sur **http://localhost:8000**

**URLs importantes :**
- 🏠 **Page d'accueil** : http://localhost:8000/
- 📖 **Documentation Swagger** : http://localhost:8000/docs
- 📘 **Documentation ReDoc** : http://localhost:8000/redoc
- ❤️ **Health check** : http://localhost:8000/health

### Avec Docker

```bash
docker-compose up --build
```

L'API sera accessible sur **http://localhost:8000**

## 🧪 Exécution des tests

**Tous les tests (69 tests) :**
```bash
python -m pytest
```

**Avec détails :**
```bash
python -m pytest -v
```

**Avec logs :**
```bash
python -m pytest -v -s
```

**Tests spécifiques :**
```bash
# Tests d'une catégorie
python -m pytest tests/pizzas/

# Test d'un fichier
python -m pytest tests/orders/test_orders_api.py

# Test d'une fonction
python -m pytest tests/orders/test_orders_api.py::test_create_order_api
```

## 🗂️ Structure du projet

```
Pizza_du_papa/
├── app/                      # Code source de l'application Backend
│   ├── main.py              # Point d'entrée FastAPI
│   ├── db.py                # Configuration base de données
│   ├── logging_config.py    # Configuration des logs
│   ├── models/              # Modèles SQLAlchemy (tables DB)
│   │   ├── pizza.py
│   │   ├── stock.py
│   │   ├── order.py
│   │   └── delivery.py
│   ├── schemas/             # Schémas Pydantic (validation)
│   │   ├── pizza.py
│   │   ├── stock.py
│   │   ├── order.py
│   │   └── delivery.py
│   ├── services/            # Logique métier
│   │   ├── pizza_service.py
│   │   ├── stock_service.py
│   │   ├── order_service.py
│   │   └── delivery_service.py
│   └── routers/             # Endpoints FastAPI (routes)
│       ├── pizzas.py
│       ├── stocks.py
│       ├── orders.py
│       └── deliveries.py
├── tests/                   # Tests TDD Backend (69 tests)
│   ├── conftest.py         # Configuration pytest
│   ├── test_health.py
│   ├── pizzas/
│   ├── stocks/
│   ├── orders/
│   └── deliveries/
├── pizzeria-front/          # Frontend Angular 17+ (Standalone)
│   ├── src/                # Code source Angular
│   │   ├── app/
│   │   │   ├── core/      # Services, intercepteurs, modèles
│   │   │   └── features/  # Pages (menu, cart, checkout, etc.)
│   │   └── environments/  # Configuration par environnement
│   ├── package.json       # Dépendances npm
│   └── README.md          # Documentation frontend
├── logs/                    # Fichiers de logs (créé auto)
├── requirements.txt         # Dépendances Python
├── Dockerfile              # Image Docker Backend
├── docker-compose.yml      # Orchestration Docker
├── DEMARRAGE.md            # 🚀 Guide de démarrage rapide
└── README.md               # Ce fichier
```

## 📡 Endpoints de l'API

### Page d'accueil
- `GET /` - Informations générales de l'API

### Health Check
- `GET /health` - Vérification du statut de l'API

### Pizzas
- `GET /pizzas` - Liste toutes les pizzas
- `GET /pizzas/{id}` - Détails d'une pizza
- `POST /pizzas` - Créer une pizza
- `PATCH /pizzas/{id}` - Mettre à jour une pizza
- `DELETE /pizzas/{id}` - Supprimer une pizza

### Stocks
- `GET /stocks` - Liste tous les items de stock
- `POST /stocks` - Créer un item de stock
- `PATCH /stocks/{id}` - Ajuster la quantité (+/-)

### Commandes
- `POST /orders` - Créer une commande (avec vérification stock)
- `GET /orders/{id}` - Détails d'une commande
- `GET /orders?status=PENDING` - Filtrer par statut
- `PATCH /orders/{id}/status` - Changer le statut
- `POST /orders/{id}/cancel` - Annuler une commande

### Livraisons
- `POST /deliveries` - Créer une livraison
- `GET /deliveries/{id}` - Détails d'une livraison
- `PATCH /deliveries/{id}/status` - Mettre à jour le statut

**👉 Voir `/docs` pour tester l'API interactivement**

## 🎲 Données de démonstration

Au démarrage, l'application crée automatiquement :

**4 pizzas :**
- Margherita (8,50€)
- Pepperoni (10,00€)
- Reine (11,50€)
- 4 Fromages (12,00€)

**9 ingrédients en stock :**
- dough (pâte) : 50
- tomato (tomate) : 40
- mozzarella : 60
- pepperoni : 30
- ham (jambon) : 25
- mushrooms (champignons) : 20
- gorgonzola : 15
- parmesan : 15
- emmental : 15

## 🔧 Configuration

### Base de données
- **Type** : SQLite (fichier `pizzeria.db`)
- **Création automatique** : Les tables sont créées au démarrage
- **Seed automatique** : Données de démo insérées si la DB est vide

### Logs
- **Emplacement** : `logs/app.log`
- **Rotation** : Quotidienne (minuit)
- **Rétention** : 7 jours
- **Format** : `%(asctime)s %(levelname)s %(name)s - %(message)s`
- **Niveau** : INFO

### Mapping Pizzas → Ingrédients
Les pizzas utilisent les ingrédients suivants (défini dans `order_service.py`) :

```python
Margherita : dough, tomato, mozzarella
Pepperoni : dough, tomato, mozzarella, pepperoni
Reine : dough, tomato, mozzarella, ham, mushrooms
4 Fromages : dough, mozzarella, gorgonzola, parmesan, emmental
```

## 📊 Exemples d'utilisation

### Créer une commande
```bash
curl -X POST "http://localhost:8000/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jean Dupont",
    "delivery_address": "123 Rue de la Paix, Paris",
    "items": [
      {"pizza_id": 1, "quantity": 2},
      {"pizza_id": 2, "quantity": 1}
    ]
  }'
```

### Consulter les stocks
```bash
curl http://localhost:8000/stocks/
```

### Créer une livraison
```bash
curl -X POST "http://localhost:8000/deliveries/" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "assigned_driver": "Pierre Martin",
    "eta_minutes": 30
  }'
```

## 🐛 Dépannage

### Problème : "uvicorn not found"
**Solution** : Utilisez `python -m uvicorn` au lieu de `uvicorn` directement

### Problème : Port déjà utilisé
**Solution** : Changez le port avec `--port 8001`
```bash
python -m uvicorn app.main:app --reload --port 8001
```

### Problème : Imports non trouvés
**Solution** : Vérifiez que vous êtes dans le bon répertoire et que l'environnement virtuel est activé

### Problème : Tests échouent
**Solution** : 
```bash
# Réinstallez les dépendances
pip install -r requirements.txt

# Supprimez les fichiers cache
rm -rf .pytest_cache __pycache__ app/__pycache__
```

## 📝 Variables d'environnement

Aucune variable d'environnement n'est requise. Tout fonctionne avec les valeurs par défaut.

Pour personnaliser :
- Base de données : Modifiez `DATABASE_URL` dans `app/db.py`
- Port du serveur : Utilisez l'argument `--port` avec uvicorn

## 🔐 Avant de pusher sur Git

Le fichier `.gitignore` est déjà configuré et exclut :
- ✅ L'environnement virtuel (`.venv/`)
- ✅ Les fichiers compilés Python (`__pycache__/`, `*.pyc`)
- ✅ La base de données (`*.db`)
- ✅ Les logs (`logs/`, `*.log`)
- ✅ Les fichiers IDE (`.vscode/`, `.idea/`)
- ✅ Les fichiers de cache de tests (`.pytest_cache/`)

**Vous pouvez pusher en toute sécurité !**

## 🚀 Prochaines étapes (suggestions)

- [ ] Ajouter l'authentification JWT
- [ ] Implémenter la pagination sur les listes
- [ ] Ajouter des filtres avancés (prix, ingrédients)
- [ ] Mettre en place un système de cache (Redis)
- [ ] Ajouter des webhooks pour les notifications
- [ ] Créer des rapports de vente
- [ ] Implémenter un système de promotions

## 📄 Licence

Ce projet est un exemple éducatif développé avec la méthodologie TDD.

## 👨‍💻 Développement

Ce projet suit les principes **TDD** :
1. ✅ **Red** : Écrire le test (qui échoue)
2. ✅ **Green** : Écrire le code minimum pour passer
3. ✅ **Refactor** : Améliorer le code

**Tests** : 69 tests couvrent l'ensemble des fonctionnalités
**Couverture** : Services + API + Logs + Gestion d'erreurs