# Script d'installation et de génération des composants
# Ce script crée automatiquement tous les composants manquants

Write-Host "🍕 Installation du projet Pizzeria Front..." -ForegroundColor Green

# Vérifier que npm est installé
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "❌ npm n'est pas installé. Installez Node.js d'abord." -ForegroundColor Red
    exit 1
}

Write-Host "`n📦 Installation des dépendances..." -ForegroundColor Yellow
npm install

Write-Host "`n🏗️  Génération des composants features..." -ForegroundColor Yellow

# Menu Page
Write-Host "Création de Menu Page..." -ForegroundColor Cyan
ng generate component features/menu/menu --flat --skip-tests
Remove-Item "src\app\features\menu\menu.component.css" -ErrorAction SilentlyContinue
Rename-Item "src\app\features\menu\menu.component.ts" "menu.page.ts"
Rename-Item "src\app\features\menu\menu.component.html" "menu.page.html"

# Cart Page  
Write-Host "Création de Cart Page..." -ForegroundColor Cyan
ng generate component features/cart/cart --flat --skip-tests
Remove-Item "src\app\features\cart\cart.component.css" -ErrorAction SilentlyContinue
Rename-Item "src\app\features\cart\cart.component.ts" "cart.page.ts"
Rename-Item "src\app\features\cart\cart.component.html" "cart.page.html"

# Checkout Page
Write-Host "Création de Checkout Page..." -ForegroundColor Cyan
ng generate component features/checkout/checkout --flat --skip-tests
Remove-Item "src\app\features\checkout\checkout.component.css" -ErrorAction SilentlyContinue
Rename-Item "src\app\features\checkout\checkout.component.ts" "checkout.page.ts"
Rename-Item "src\app\features\checkout\checkout.component.html" "checkout.page.html"

# Order Tracking Page
Write-Host "Création de Order Tracking Page..." -ForegroundColor Cyan
ng generate component features/order-tracking/order-tracking --flat --skip-tests
Remove-Item "src\app\features\order-tracking\order-tracking.component.css" -ErrorAction SilentlyContinue
Rename-Item "src\app\features\order-tracking\order-tracking.component.ts" "order-tracking.page.ts"
Rename-Item "src\app\features\order-tracking\order-tracking.component.html" "order-tracking.page.html"

# Stocks Page
Write-Host "Création de Stocks Page..." -ForegroundColor Cyan
ng generate component features/stocks/stocks --flat --skip-tests
Remove-Item "src\app\features\stocks\stocks.component.css" -ErrorAction SilentlyContinue
Rename-Item "src\app\features\stocks\stocks.component.ts" "stocks.page.ts"
Rename-Item "src\app\features\stocks\stocks.component.html" "stocks.page.html"

# Pizza Card Component
Write-Host "Création de Pizza Card Component..." -ForegroundColor Cyan
ng generate component shared/components/pizza-card/pizza-card --flat --skip-tests

Write-Host "`n✅ Installation terminée !" -ForegroundColor Green
Write-Host "`nPour démarrer l'application :" -ForegroundColor Yellow
Write-Host "  npm start" -ForegroundColor Cyan
Write-Host "`nPour exécuter les tests :" -ForegroundColor Yellow
Write-Host "  npm test" -ForegroundColor Cyan
