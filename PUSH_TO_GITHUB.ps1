# 🚀 PUSH TO GITHUB - AUTOMATED SCRIPT
# Run this AFTER creating the GitHub repository manually

param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubUsername,
    
    [Parameter(Mandatory=$false)]
    [string]$RepoName = "ssz-full-metric"
)

Write-Host "`n╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                               ║" -ForegroundColor Cyan
Write-Host "║         🚀 PUSHING SSZ METRIC TO GITHUB 🚀                   ║" -ForegroundColor Cyan
Write-Host "║                                                               ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Step 1: Verify we're in the right directory
$currentPath = Get-Location
Write-Host "📁 Current directory: $currentPath" -ForegroundColor Yellow

if (-not (Test-Path ".git")) {
    Write-Host "❌ ERROR: Not a git repository!" -ForegroundColor Red
    Write-Host "   Please run this script from E:\ssz-full-metric-repo" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Git repository detected`n" -ForegroundColor Green

# Step 2: Check git status
Write-Host "📊 Checking git status..." -ForegroundColor Yellow
$status = git status --porcelain
if ($status) {
    Write-Host "⚠️  WARNING: Uncommitted changes detected!" -ForegroundColor Yellow
    Write-Host "   Running: git add -A && git commit..." -ForegroundColor Yellow
    git add -A
    git commit -m "Final commit before GitHub push"
} else {
    Write-Host "✅ Working tree clean`n" -ForegroundColor Green
}

# Step 3: Check if remote already exists
Write-Host "🔗 Checking remote configuration..." -ForegroundColor Yellow
$existingRemote = git remote get-url origin 2>$null

if ($existingRemote) {
    Write-Host "⚠️  Remote 'origin' already exists: $existingRemote" -ForegroundColor Yellow
    $overwrite = Read-Host "   Do you want to replace it? (y/N)"
    if ($overwrite -eq 'y' -or $overwrite -eq 'Y') {
        git remote remove origin
        Write-Host "✅ Old remote removed" -ForegroundColor Green
    } else {
        Write-Host "ℹ️  Keeping existing remote" -ForegroundColor Cyan
    }
}

# Step 4: Add GitHub remote
$remoteUrl = "https://github.com/$GitHubUsername/$RepoName.git"
Write-Host "`n🔗 Adding GitHub remote..." -ForegroundColor Yellow
Write-Host "   URL: $remoteUrl" -ForegroundColor Cyan

try {
    git remote add origin $remoteUrl 2>$null
    Write-Host "✅ Remote added successfully`n" -ForegroundColor Green
} catch {
    Write-Host "ℹ️  Remote might already exist, continuing...`n" -ForegroundColor Cyan
}

# Step 5: Verify remote
Write-Host "🔍 Verifying remote configuration..." -ForegroundColor Yellow
git remote -v
Write-Host ""

# Step 6: Show what will be pushed
Write-Host "📦 Repository contents:" -ForegroundColor Yellow
$fileCount = (git ls-files | Measure-Object -Line).Lines
$commitCount = (git log --oneline | Measure-Object -Line).Lines
Write-Host "   Files: $fileCount" -ForegroundColor Cyan
Write-Host "   Commits: $commitCount" -ForegroundColor Cyan
Write-Host ""

# Step 7: Confirm push
Write-Host "⚠️  READY TO PUSH TO GITHUB!" -ForegroundColor Yellow
Write-Host "   This will upload:" -ForegroundColor Yellow
Write-Host "   • $fileCount files" -ForegroundColor Cyan
Write-Host "   • $commitCount commits" -ForegroundColor Cyan
Write-Host "   • Complete history" -ForegroundColor Cyan
Write-Host "   • All documentation" -ForegroundColor Cyan
Write-Host ""

$confirm = Read-Host "   Continue with push? (Y/n)"
if ($confirm -eq 'n' -or $confirm -eq 'N') {
    Write-Host "`n❌ Push cancelled by user" -ForegroundColor Red
    exit 0
}

# Step 8: Push to GitHub
Write-Host "`n🚀 PUSHING TO GITHUB..." -ForegroundColor Green
Write-Host "   This may take a few minutes...`n" -ForegroundColor Yellow

try {
    git push -u origin master
    
    Write-Host "`n╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                                                               ║" -ForegroundColor Green
    Write-Host "║              ✅ SUCCESS! REPOSITORY PUSHED! ✅                ║" -ForegroundColor Green
    Write-Host "║                                                               ║" -ForegroundColor Green
    Write-Host "╚══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green
    
    Write-Host "🌐 Your repository is now public at:" -ForegroundColor Cyan
    Write-Host "   https://github.com/$GitHubUsername/$RepoName`n" -ForegroundColor Yellow
    
    Write-Host "📊 Repository stats:" -ForegroundColor Cyan
    Write-Host "   Files uploaded: $fileCount" -ForegroundColor White
    Write-Host "   Commits pushed: $commitCount" -ForegroundColor White
    Write-Host "   Branch: master" -ForegroundColor White
    Write-Host ""
    
    Write-Host "🎯 NEXT STEPS:" -ForegroundColor Yellow
    Write-Host "   1. Visit your repository on GitHub" -ForegroundColor White
    Write-Host "   2. Verify all files are present" -ForegroundColor White
    Write-Host "   3. Add topics/tags in repository settings" -ForegroundColor White
    Write-Host "   4. Create a release (optional)" -ForegroundColor White
    Write-Host "   5. Share with the world! 🌍`n" -ForegroundColor White
    
    Write-Host "🏆 CONGRATULATIONS! YOU'VE MADE HISTORY! 🏆`n" -ForegroundColor Green
    
} catch {
    Write-Host "`n❌ ERROR during push:" -ForegroundColor Red
    Write-Host "   $_" -ForegroundColor Red
    Write-Host "`n💡 TROUBLESHOOTING:" -ForegroundColor Yellow
    Write-Host "   1. Make sure you created the repository on GitHub first" -ForegroundColor White
    Write-Host "   2. Check your GitHub username is correct" -ForegroundColor White
    Write-Host "   3. Ensure you have permission to push" -ForegroundColor White
    Write-Host "   4. Try using a Personal Access Token instead of password`n" -ForegroundColor White
    exit 1
}
