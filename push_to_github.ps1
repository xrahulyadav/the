# PowerShell Git Initialization & Remote Push Script for xrahulyadav/the
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Instagram Threads Auto-Poster // Deployment to GitHub" -ForegroundColor Cyan
Write-Host " Target Repository: https://github.com/xrahulyadav/the.git" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Initialize Git if not initialized
if (-not (Test-Path ".git")) {
    Write-Host "[1/5] Initializing Git repository..." -ForegroundColor Yellow
    git init
} else {
    Write-Host "[1/5] Git repository already initialized." -ForegroundColor Green
}

# 2. Rename branch to main
Write-Host "[2/5] Switching branch to 'main'..." -ForegroundColor Yellow
git branch -M main

# 3. Configure Remote URL
Write-Host "[3/5] Setting remote origin to https://github.com/xrahulyadav/the.git..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin https://github.com/xrahulyadav/the.git

# 4. Stage and commit files
Write-Host "[4/5] Staging files and creating commit..." -ForegroundColor Yellow
git add .github/ script.py index.html posts_log.json upcoming_queue.json requirements.txt README.md .gitignore .env.example
git commit -m "feat: complete instagram threads auto-posting & monitoring system for github actions and pages"

# 5. Push to GitHub
Write-Host "[5/5] Pushing to GitHub (origin main)..." -ForegroundColor Yellow
Write-Host "Note: If prompted, authenticate using your GitHub Username and Personal Access Token (PAT)." -ForegroundColor DarkGray
git push -u origin main

Write-Host "==========================================================" -ForegroundColor Green
Write-Host " Deployment script finished!" -ForegroundColor Green
Write-Host " Next Steps:" -ForegroundColor Cyan
Write-Host " 1. Go to: https://github.com/xrahulyadav/the/settings/secrets/actions" -ForegroundColor White
Write-Host "    Add Secrets: GEMINI_API_KEY, THREADS_ACCESS_TOKEN, THREADS_USER_ID" -ForegroundColor White
Write-Host " 2. Enable Workflow Read & Write Permissions in Settings -> Actions -> General" -ForegroundColor White
Write-Host " 3. Enable GitHub Pages in Settings -> Pages (Source: Deploy from branch 'main', root /)" -ForegroundColor White
Write-Host " Live Dashboard will be at: https://xrahulyadav.github.io/the/" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Green
