# Pizzeria Front

Application mobile Angular pour pizzeria, développée avec **Angular 17+** (standalone components) et suivant strictement la méthodologie **TDD (Test-Driven Development)**.

## 🎯 Fonctionnalités

### Interface utilisateur complète
- **Menu** : Liste des pizzas avec prix et disponibilité
- **Panier** : Gestion des quantités et calcul du total
- **Commande** : Formulaire de checkout avec validation
- **Suivi** : Tracking en temps réel du statut de livraison
- **Stocks** : Consultation des ingrédients (lecture seule)

### Points techniques
- ✅ **Angular 17+** avec standalone components
- ✅ **TailwindCSS** pour le styling
- ✅ **Tests complets** (Jasmine/Karma) sur services et composants
- ✅ **HttpClient** avec interceptors pour API calls
- ✅ **Reactive Forms** pour validation
- ✅ **Signals/BehaviorSubject** pour state management léger
- ✅ **Docker** ready avec nginx

## 📋 Prérequis

- **Node.js 18+** et **npm 9+**
- **Angular CLI 17+** : `npm install -g @angular/cli`
- **Docker & Docker Compose** (optionnel)

## 🚀 Installation

### 1. Cloner et installer les dépendances

```bash
cd pizzeria-front
npm ci
```

### 2. Configuration de l'API Backend

Assurez-vous que l'API backend est lancée sur `http://localhost:8000`.

Pour modifier l'URL de l'API, éditez `src/environments/environment.development.ts`.

## ▶️ Démarrage de l'application

### En mode développement

```bash
npm start
```

L'application sera accessible sur **http://localhost:4200**

### Build de production

```bash
npm run build
```

Les fichiers compilés seront dans `dist/pizzeria-front/`.

## 🧪 Exécution des tests

### Tests unitaires (Karma)

```bash
# Tous les tests
npm test

# Tests en mode watch
npm run test:watch

# Tests avec couverture
npm run test:coverage
```

### Tests spécifiques

```bash
# Test d'un fichier
ng test --include='**/cart.service.spec.ts'

# Test d'une suite
ng test --grep='CartService'
```

## 🐳 Docker

### Build et lancement avec Docker

```bash
docker compose up --build
```

L'application sera accessible sur **http://localhost:4200**

### Build de l'image Docker uniquement

```bash
docker build -t pizzeria-front .
```

## 🗂️ Structure du projet

```
pizzeria-front/
├── src/
│   ├── app/
│   │   ├── core/                    # Services et utilitaires centraux
│   │   │   ├── services/
│   │   │   │   ├── api/            # Services API (HTTP)
│   │   │   │   │   ├── pizzas.api.ts
│   │   │   │   │   ├── orders.api.ts
│   │   │   │   │   ├── deliveries.api.ts
│   │   │   │   │   ├── stocks.api.ts
│   │   │   │   │   └── health.api.ts
│   │   │   │   ├── cart.service.ts      # Gestion panier
│   │   │   │   └── logger.service.ts    # Logs
│   │   │   ├── models/             # Modèles TypeScript
│   │   │   │   ├── pizza.model.ts
│   │   │   │   ├── order.model.ts
│   │   │   │   ├── delivery.model.ts
│   │   │   │   └── stock.model.ts
│   │   │   └── interceptors/       # HTTP Interceptors
│   │   │       ├── api-base.interceptor.ts
│   │   │       └── error-logger.interceptor.ts
│   │   ├── features/               # Pages/Features
│   │   │   ├── menu/              # Liste des pizzas
│   │   │   ├── cart/              # Panier
│   │   │   ├── checkout/          # Commande
│   │   │   ├── order-tracking/    # Suivi livraison
│   │   │   └── stocks/            # Stocks (lecture seule)
│   │   ├── shared/                # Composants réutilisables
│   │   │   └── components/
│   │   │       └── pizza-card/
│   │   ├── app.routes.ts          # Configuration routing
│   │   ├── app.config.ts          # Configuration app
│   │   ├── app.component.ts       # Root component
│   │   └── app.component.html     # Template principal
│   ├── environments/              # Variables d'environnement
│   │   ├── environment.ts
│   │   └── environment.development.ts
│   └── styles.css                 # Styles globaux (Tailwind)
├── docker/
│   └── nginx.conf                 # Configuration nginx
├── Dockerfile                      # Image Docker
├── docker-compose.yml             # Orchestration Docker
├── tailwind.config.js             # Configuration Tailwind
├── package.json                   # Dépendances npm
└── README.md                      # Ce fichier
```

## 🛣️ Routes de l'application

- `/` → Redirige vers `/menu`
- `/menu` → Liste des pizzas disponibles
- `/cart` → Panier d'achat
- `/checkout` → Formulaire de commande
- `/orders/:id` → Détail et suivi de commande
- `/stocks` → Liste des stocks (démo admin)
- `/health` → Status de l'API

## 🔧 Configuration

### Environnements

**Development** (`src/environments/environment.development.ts`) :
```typescript
{
  apiBaseUrl: 'http://localhost:8000',
  enableRemoteLogs: false,
  logLevel: 'INFO'
}
```

**Production** (`src/environments/environment.ts`) :
```typescript
{
  apiBaseUrl: 'https://api.pizzeria.com',
  enableRemoteLogs: true,
  logLevel: 'ERROR'
}
```

### Tailwind CSS

Configuré dans `tailwind.config.js` avec purge automatique pour optimiser le build.

Classes utilitaires disponibles pour tous les composants.

## 📡 API Contract (Backend attendu)

L'application s'attend à ce que le backend expose ces endpoints :

- `GET /pizzas` - Liste des pizzas
- `GET /pizzas/:id` - Détail d'une pizza
- `POST /orders` - Créer une commande
- `GET /orders/:id` - Détail d'une commande
- `GET /deliveries/:id` - Détail d'une livraison
- `GET /stocks` - Liste des stocks
- `GET /health` - Health check

## 🎨 Guide de style

### TailwindCSS classes principales utilisées

- **Layout** : `container`, `mx-auto`, `flex`, `grid`
- **Spacing** : `p-4`, `m-2`, `space-y-4`
- **Colors** : `bg-orange-500`, `text-white`, `border-gray-300`
- **Typography** : `text-lg`, `font-bold`, `text-center`
- **Buttons** : `px-4 py-2 rounded hover:bg-orange-600`

### Composants maison

Tous les composants UI sont créés en interne (pas de librairie externe) :
- `pizza-card` : Carte pizza avec image, prix, badge disponibilité
- Formulaires réactifs avec validation
- Alerts simples avec `window.alert`

## 🐛 Dépannage

### Problème : API non accessible

**Solution** : Vérifiez que l'API backend tourne sur `http://localhost:8000` et que le CORS est configuré.

```bash
# Dans le projet backend
python -m uvicorn app.main:app --reload
```

### Problème : Tests échouent

**Solution** : 
```bash
# Réinstallez les dépendances
rm -rf node_modules package-lock.json
npm install

# Nettoyez le cache Angular
ng cache clean
```

### Problème : Port 4200 déjà utilisé

**Solution** : Changez le port
```bash
ng serve --port 4201
```

### Problème : Tailwind ne fonctionne pas

**Solution** : Vérifiez que `styles.css` contient les directives Tailwind :
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## 📊 Scripts disponibles

```json
{
  "start": "ng serve",
  "build": "ng build",
  "test": "ng test",
  "test:watch": "ng test --watch=true",
  "test:coverage": "ng test --code-coverage",
  "lint": "ng lint"
}
```

## 🔐 Sécurité

- ✅ **Pas d'authentification** pour l'instant (ajoutez JWT plus tard)
- ✅ **Validation côté client** via Reactive Forms
- ✅ **Sanitization** automatique par Angular
- ✅ **HttpOnly** headers gérés par interceptors

## 🚀 Prochaines étapes (suggestions)

- [ ] Ajouter l'authentification JWT
- [ ] Implémenter la persistence du panier (localStorage)
- [ ] Ajouter des animations (Angular Animations)
- [ ] Lazy loading des modules features
- [ ] Progressive Web App (PWA)
- [ ] Internationalisation (i18n)
- [ ] Tests E2E avec Cypress
- [ ] State management avec NgRx (si l'app grossit)

## 👨‍💻 Développement TDD

Ce projet suit les principes **TDD** :

1. ✅ **Red** : Écrire le test (qui échoue)
2. ✅ **Green** : Écrire le code minimum pour passer
3. ✅ **Refactor** : Améliorer le code

**Tests couverts** :
- Services API (HTTP mocking avec `HttpTestingController`)
- CartService (ajout, suppression, calcul total)
- LoggerService (logs locaux et remote)
- Composants (render, interactions, navigation)
- Interceptors (base URL, error handling)

## 📄 Licence

Ce projet est un exemple éducatif développé avec la méthodologie TDD.

## 🔗 Liens utiles

- [Angular Documentation](https://angular.io/docs)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Jasmine Testing Framework](https://jasmine.github.io/)
- [API Backend Repository](../Pizza_du_papa/)
