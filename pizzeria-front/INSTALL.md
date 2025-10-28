# 🚀 GUIDE D'INSTALLATION RAPIDE

## Prérequis
- Node.js 18+ et npm 9+
- API Backend lancée sur http://localhost:8000

## Installation en 2 étapes

### 1. Installez les dépendances
```powershell
cd pizzeria-front
npm install
```

### 2. Lancez l'application
```powershell
npm start
```

➡️ Ouvrez http://localhost:4200

## Tests
```powershell
npm test
```

## Docker
```powershell
docker compose up --build
```

## Structure du projet

```
pizzeria-front/
├── src/app/
│   ├── core/                    # Services, interceptors, modèles
│   │   ├── services/api/       # API clients (pizzas, orders, stocks, deliveries)
│   │   ├── cart.service.ts     # Gestion du panier
│   │   ├── logger.service.ts   # Logs console + remote
│   │   └── interceptors/       # HTTP interceptors
│   ├── features/                # Pages
│   │   ├── menu/               # Liste des pizzas
│   │   ├── cart/               # Panier
│   │   ├── checkout/           # Formulaire de commande
│   │   ├── order-tracking/     # Suivi de livraison
│   │   └── stocks/             # Stocks (lecture seule)
│   └── shared/                  # Composants réutilisables
├── environments/                # Configuration API
└── docker/                      # Config nginx pour production
```

## Fonctionnalités

✅ **Menu** : Liste des pizzas avec disponibilité
✅ **Panier** : Ajout/suppression, calcul du total
✅ **Commande** : Formulaire réactif avec validation
✅ **Suivi** : Affichage du statut de commande
✅ **Stocks** : Consultation des ingrédients
✅ **Tests** : Tous les services et composants testés
✅ **TDD** : Tests écrits avant le code
✅ **Logging** : Console + remote (optionnel)
✅ **Interceptors** : Base URL + gestion d'erreurs
✅ **Responsive** : TailwindCSS
✅ **Standalone** : Angular 17+ components

## Commandes utiles

| Commande | Description |
|----------|-------------|
| `npm start` | Dev server (port 4200) |
| `npm test` | Tests unitaires |
| `npm run build` | Build production |
| `npm run test:coverage` | Tests avec couverture |

## Configuration API

Éditez `src/environments/environment.development.ts` :
```typescript
export const environment = {
  production: false,
  apiBaseUrl: 'http://localhost:8000',  // ← URL de votre API
  enableRemoteLogs: false,
  logLevel: 'INFO'
};
```

## Troubleshooting

**Port 4200 déjà utilisé ?**
```powershell
ng serve --port 4201
```

**API non accessible ?**
- Vérifiez que l'API backend tourne
- Vérifiez le CORS côté API

**Tests échouent ?**
```powershell
rm -rf node_modules package-lock.json
npm install
```

## Documentation complète

Voir [README.md](README.md) pour plus de détails.
