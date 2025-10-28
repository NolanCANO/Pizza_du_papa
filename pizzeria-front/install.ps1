# 🍕 Installation complète de Pizzeria Front

Write-Host "`n🍕 Installation du projet Pizzeria Front..." -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Gray

# 1. Vérifications préliminaires
Write-Host "`n📋 Vérification des prérequis..." -ForegroundColor Yellow

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Node.js n'est pas installé. Téléchargez-le sur https://nodejs.org/" -ForegroundColor Red
    exit 1
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "❌ npm n'est pas installé." -ForegroundColor Red
    exit 1
}

$nodeVersion = node --version
$npmVersion = npm --version
Write-Host "✅ Node.js version: $nodeVersion" -ForegroundColor Green
Write-Host "✅ npm version: $npmVersion" -ForegroundColor Green

# 2. Installation des dépendances
Write-Host "`n📦 Installation des dépendances npm..." -ForegroundColor Yellow
Write-Host "   (Cela peut prendre quelques minutes)" -ForegroundColor Gray

npm install

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Échec de l'installation des dépendances" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Dépendances installées avec succès" -ForegroundColor Green

# 3. Vérification de l'installation d'Angular CLI
Write-Host "`n🔧 Vérification d'Angular CLI..." -ForegroundColor Yellow

if (-not (Get-Command ng -ErrorAction SilentlyContinue)) {
    Write-Host "⚠️  Angular CLI n'est pas installé globalement" -ForegroundColor Yellow
    Write-Host "   Utilisez: npm install -g @angular/cli" -ForegroundColor Gray
    Write-Host "   Ou utilisez: npx ng pour les commandes" -ForegroundColor Gray
} else {
    $ngVersion = ng version --help 2>$null
    Write-Host "✅ Angular CLI installé" -ForegroundColor Green
}

# 4. Résumé
Write-Host "`n" -NoNewline
Write-Host "=" * 60 -ForegroundColor Gray
Write-Host "`n✨ Installation terminée avec succès ! ✨`n" -ForegroundColor Green

Write-Host "📚 Commandes disponibles:" -ForegroundColor Cyan
Write-Host "   npm start           " -NoNewline; Write-Host "→ Démarre le serveur de développement (http://localhost:4200)" -ForegroundColor Gray
Write-Host "   npm test            " -NoNewline; Write-Host "→ Lance les tests unitaires" -ForegroundColor Gray
Write-Host "   npm run build       " -NoNewline; Write-Host "→ Build de production" -ForegroundColor Gray
Write-Host "   docker compose up   " -NoNewline; Write-Host "→ Lance l'app avec Docker" -ForegroundColor Gray

Write-Host "`n🎯 Prochaines étapes:" -ForegroundColor Cyan
Write-Host "   1. Assurez-vous que l'API backend tourne sur http://localhost:8000" -ForegroundColor White
Write-Host "   2. Lancez: " -NoNewline; Write-Host "npm start" -ForegroundColor Yellow
Write-Host "   3. Ouvrez votre navigateur sur: " -NoNewline; Write-Host "http://localhost:4200" -ForegroundColor Yellow

Write-Host "`n📖 Documentation complète dans README.md`n" -ForegroundColor Gray
