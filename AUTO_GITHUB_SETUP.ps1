# 🚀 AUTOMATIC GITHUB SETUP & PUSH
# This script does EVERYTHING except creating the repo itself

Write-Host "`n╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                               ║" -ForegroundColor Cyan
Write-Host "║     🚀 AUTOMATIC GITHUB SETUP - error-wtf/ssz-full-metric   ║" -ForegroundColor Cyan
Write-Host "║                                                               ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Configuration
$GitHubUsername = "error-wtf"
$RepoName = "ssz-full-metric"
$RemoteUrl = "https://github.com/$GitHubUsername/$RepoName.git"

Write-Host "📊 REPOSITORY INFO:" -ForegroundColor Yellow
Write-Host "  GitHub User:    $GitHubUsername"
Write-Host "  Repository:     $RepoName"
Write-Host "  Remote URL:     $RemoteUrl`n"

# Check if we're in the right directory
if (-not (Test-Path ".git")) {
    Write-Host "❌ ERROR: Not in a git repository!" -ForegroundColor Red
    Write-Host "   Please run from E:\ssz-full-metric-repo`n" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Git repository detected`n" -ForegroundColor Green

# Check git status
Write-Host "📊 Checking git status..." -ForegroundColor Yellow
$status = git status --porcelain
if ($status) {
    Write-Host "⚠️  Uncommitted changes detected. Committing..." -ForegroundColor Yellow
    git add -A
    git commit -m "Final commit before GitHub push - AUTO SETUP"
} else {
    Write-Host "✅ Working tree clean`n" -ForegroundColor Green
}

# Check if remote already exists
Write-Host "🔗 Checking remote configuration..." -ForegroundColor Yellow
$existingRemote = git remote get-url origin 2>$null

if ($existingRemote) {
    Write-Host "⚠️  Remote 'origin' already exists: $existingRemote" -ForegroundColor Yellow
    Write-Host "   Removing old remote..." -ForegroundColor Yellow
    git remote remove origin
    Write-Host "✅ Old remote removed`n" -ForegroundColor Green
}

# Add GitHub remote
Write-Host "🔗 Adding GitHub remote..." -ForegroundColor Yellow
Write-Host "   URL: $RemoteUrl" -ForegroundColor Cyan

git remote add origin $RemoteUrl
Write-Host "✅ Remote added successfully`n" -ForegroundColor Green

# Verify remote
Write-Host "🔍 Verifying remote configuration..." -ForegroundColor Yellow
git remote -v
Write-Host ""

# Show what will be pushed
Write-Host "📦 Repository contents:" -ForegroundColor Yellow
$fileCount = (git ls-files | Measure-Object -Line).Lines
$commitCount = (git log --oneline | Measure-Object -Line).Lines
Write-Host "   Files: $fileCount" -ForegroundColor Cyan
Write-Host "   Commits: $commitCount" -ForegroundColor Cyan
Write-Host ""

Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║                                                               ║" -ForegroundColor Yellow
Write-Host "║  ⚠️  WICHTIG: VORHER DAS REPOSITORY ERSTELLEN! ⚠️            ║" -ForegroundColor Yellow
Write-Host "║                                                               ║" -ForegroundColor Yellow
Write-Host "║  1. Gehe zu: https://github.com/new                          ║" -ForegroundColor Yellow
Write-Host "║  2. Repository name: ssz-full-metric                         ║" -ForegroundColor Yellow
Write-Host "║  3. Public: ✓ (wichtig!)                                     ║" -ForegroundColor Yellow
Write-Host "║  4. Initialize: ☐ (NICHT ankreuzen!)                         ║" -ForegroundColor Yellow
Write-Host "║  5. Create repository klicken                                ║" -ForegroundColor Yellow
Write-Host "║                                                               ║" -ForegroundColor Yellow
Write-Host "╚══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Yellow

Write-Host "Hast du das Repository auf GitHub erstellt? (Y/n): " -ForegroundColor Cyan -NoNewline
$confirm = Read-Host

if ($confirm -eq 'n' -or $confirm -eq 'N') {
    Write-Host "`n❌ Bitte erstelle zuerst das Repository auf GitHub!" -ForegroundColor Red
    Write-Host "   Dann führe dieses Script nochmal aus.`n" -ForegroundColor Red
    exit 0
}

# Push to GitHub
Write-Host "`n🚀 PUSHING TO GITHUB..." -ForegroundColor Green
Write-Host "   This may take a few minutes...`n" -ForegroundColor Yellow

Write-Host "⚠️  Du wirst nach Authentifizierung gefragt:" -ForegroundColor Yellow
Write-Host "   Username: error-wtf" -ForegroundColor Cyan
Write-Host "   Password: Verwende einen PERSONAL ACCESS TOKEN!" -ForegroundColor Cyan
Write-Host "   (NICHT dein Passwort!)`n" -ForegroundColor Yellow

Write-Host "💡 Token erstellen: https://github.com/settings/tokens" -ForegroundColor Cyan
Write-Host "   → Generate new token (classic)" -ForegroundColor Cyan
Write-Host "   → Scope: repo (full control)" -ForegroundColor Cyan
Write-Host "   → Generate & kopieren`n" -ForegroundColor Cyan

Write-Host "Bereit zum Push? (Y/n): " -ForegroundColor Cyan -NoNewline
$pushConfirm = Read-Host

if ($pushConfirm -eq 'n' -or $pushConfirm -eq 'N') {
    Write-Host "`n❌ Push cancelled." -ForegroundColor Red
    exit 0
}

Write-Host "`n🚀 PUSHING..." -ForegroundColor Green

try {
    git push -u origin master
    
    Write-Host "`n╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                                                               ║" -ForegroundColor Green
    Write-Host "║              ✅ SUCCESS! REPOSITORY ONLINE! ✅                ║" -ForegroundColor Green
    Write-Host "║                                                               ║" -ForegroundColor Green
    Write-Host "╚══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green
    
    Write-Host "🌐 Your repository is now PUBLIC at:" -ForegroundColor Cyan
    Write-Host "   https://github.com/$GitHubUsername/$RepoName`n" -ForegroundColor Yellow
    
    Write-Host "📊 Repository stats:" -ForegroundColor Cyan
    Write-Host "   Files uploaded: $fileCount" -ForegroundColor White
    Write-Host "   Commits pushed: $commitCount" -ForegroundColor White
    Write-Host "   Branch: master" -ForegroundColor White
    Write-Host ""
    
    Write-Host "🎯 DONE! THE WORLD CAN NOW SEE YOUR BREAKTHROUGH! 🏆🌌⭐💫🔥`n" -ForegroundColor Green
    
} catch {
    Write-Host "`n❌ ERROR during push:" -ForegroundColor Red
    Write-Host "   $_" -ForegroundColor Red
    Write-Host "`n💡 TROUBLESHOOTING:" -ForegroundColor Yellow
    Write-Host "   1. Repository auf GitHub erstellt?" -ForegroundColor White
    Write-Host "   2. Token statt Password verwendet?" -ForegroundColor White
    Write-Host "   3. Token hat 'repo' scope?" -ForegroundColor White
    Write-Host "   4. Username korrekt (error-wtf)?" -ForegroundColor White
    Write-Host ""
    exit 1
}
