# 🚀 Guide de Démarrage Rapide

Guide pour démarrer le projet après un `git clone`.

## 📦 Prérequis à installer

Avant de commencer, assurez-vous d'avoir installé :

1. **Python 3.12+** : https://www.python.org/downloads/
   - ⚠️ Cochez "Add Python to PATH" lors de l'installation
   - Vérifiez : `python --version`

2. **Node.js 18+** : https://nodejs.org/
   - Vérifiez : `node --version` et `npm --version`

3. **Git** : https://git-scm.com/

## 📥 1. Cloner le projet

```powershell
git clone https://github.com/NolanCANO/Pizza_du_papa.git
cd Pizza_du_papa
```

## 🔧 2. Configuration du Backend

### a) Créer l'environnement virtuel Python

```powershell
python -m venv .venv
```

### b) Activer l'environnement virtuel

**Windows (PowerShell) :**
```powershell
.venv\Scripts\Activate.ps1
```

Si vous avez une erreur de sécurité, exécutez ceci une fois :
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows (CMD) :**
```cmd
.venv\Scripts\activate.bat
```

**Linux/Mac :**
```bash
source .venv/bin/activate
```

### c) Installer les dépendances Python

```powershell
pip install -r requirements.txt
```

⏱️ **Temps estimé** : 30 secondes - 1 minute

## ▶️ 3. Lancer le Backend

Dans le dossier `Pizza_du_papa`, avec l'environnement virtuel activé :

```powershell
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

✅ **Backend lancé sur** : http://localhost:8000
- Documentation API : http://localhost:8000/docs
- Health check : http://localhost:8000/health

**La base de données et les données de test sont créées automatiquement au démarrage !**

---

## 🎨 4. Configuration du Frontend (Optionnel)

Si vous voulez aussi lancer le frontend Angular :

### a) Aller dans le dossier frontend

```powershell
cd ..\pizzeria-front
```

### b) Installer les dépendances npm

```powershell
npm install
```

⏱️ **Temps estimé** : 2-3 minutes (première fois seulement)

### c) Lancer le frontend

```powershell
npm start
```

✅ **Frontend lancé sur** : http://localhost:4200

---

## 🚀 Méthode Rapide (Tout-en-un)

Si vous avez un script PowerShell de lancement (`LANCER.ps1`) :

```powershell
.\LANCER.ps1
```

Ce script :
- ✅ Lance le backend sur le port 8000
- ✅ Lance le frontend sur le port 4200
- ✅ Installe automatiquement les dépendances npm si nécessaire
- ✅ Ouvre deux fenêtres PowerShell séparées

---

## 🧪 5. Tester que tout fonctionne

### Tester le Backend

```powershell
# Dans le dossier Pizza_du_papa avec l'environnement virtuel activé
python -m pytest
```

✅ Résultat attendu : **69 tests passés**

### Tester le Frontend

Ouvrez votre navigateur sur http://localhost:4200 et vous devriez voir :
- 🏠 Page d'accueil
- 📋 Menu des pizzas
- 📦 Gestion des stocks
- 📝 Commandes
- 🚚 Livraisons

---

## 📂 Résumé de la Structure

```
Pizza_du_papa/           # ← BACKEND
├── app/                 # Code source API
├── tests/               # 69 tests TDD
├── .venv/               # Environnement virtuel Python (à créer)
└── requirements.txt     # Dépendances Python

pizzeria-front/          # ← FRONTEND (dans le dossier parent)
├── src/                 # Code source Angular
└── node_modules/        # Dépendances npm (créé par npm install)
```

---

## ❓ Problèmes courants

### ❌ "python n'est pas reconnu"
**Solution** : Python n'est pas dans le PATH. Réinstallez Python en cochant "Add to PATH".

### ❌ "Impossible d'exécuter Activate.ps1"
**Solution** : Erreur de sécurité PowerShell. Exécutez :
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### ❌ "Port 8000 already in use"
**Solution** : Un autre processus utilise le port. Tuez le processus ou utilisez un autre port :
```powershell
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8001
```

### ❌ "npm not found"
**Solution** : Node.js n'est pas installé. Téléchargez-le depuis https://nodejs.org/

### ❌ Frontend affiche "Impossible de charger les pizzas"
**Solution** : Le backend n'est pas lancé ou CORS mal configuré. Vérifiez que :
1. Le backend tourne sur http://localhost:8000
2. Le fichier `app/main.py` contient la configuration CORS

---

## 🎯 Workflow de développement

### Backend (FastAPI)

1. Activer l'environnement virtuel
2. Lancer le serveur : `.venv\Scripts\python.exe -m uvicorn app.main:app --reload`
3. Modifier le code (rechargement automatique avec `--reload`)
4. Lancer les tests : `python -m pytest`

### Frontend (Angular)

1. Lancer le serveur : `npm start`
2. Modifier le code (rechargement automatique)
3. Lancer les tests : `npm test`

---

## 📝 Commandes utiles

### Backend
```powershell
# Lancer le serveur
.venv\Scripts\python.exe -m uvicorn app.main:app --reload

# Lancer tous les tests
python -m pytest

# Lancer les tests avec détails
python -m pytest -v

# Tester un module spécifique
python -m pytest tests/pizzas/

# Voir les logs en temps réel
# Les logs sont dans logs/app.log
```

### Frontend
```powershell
# Lancer le serveur de développement
npm start

# Lancer les tests
npm test

# Builder pour la production
npm run build

# Lancer le linter
npm run lint
```

---

## 🔐 Données de test

Au premier démarrage, le backend crée automatiquement :

**4 Pizzas :**
- 🍕 Margherita (8,50€)
- 🍕 Pepperoni (10,00€)
- 🍕 Reine (11,50€)
- 🍕 4 Fromages (12,00€)

**9 Ingrédients :**
- dough (pâte) : 50
- tomato (tomate) : 40
- mozzarella : 60
- pepperoni : 30
- ham (jambon) : 25
- mushrooms (champignons) : 20
- gorgonzola : 15
- parmesan : 15
- emmental : 15

---

## 📚 Documentation

- **API Backend** : http://localhost:8000/docs
- **README complet** : [README.md](README.md)

---

## 🎉 C'est parti !

Vous êtes prêt à développer ! 🚀

**Besoin d'aide ?** Consultez le README.md ou la documentation interactive sur `/docs`.
