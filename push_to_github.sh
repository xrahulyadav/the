#!/usr/bin/env bash
# Git Initialization & Push Script for xrahulyadav/the

echo "=========================================================="
echo " Instagram Threads Auto-Poster // Deployment to GitHub"
echo " Target Repository: https://github.com/xrahulyadav/the.git"
echo "=========================================================="

# 1. Initialize Git if not initialized
if [ ! -d ".git" ]; then
    echo "[1/5] Initializing Git repository..."
    git init
else
    echo "[1/5] Git repository already initialized."
fi

# 2. Rename branch to main
echo "[2/5] Switching branch to 'main'..."
git branch -M main

# 3. Configure Remote URL
echo "[3/5] Setting remote origin to https://github.com/xrahulyadav/the.git..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/xrahulyadav/the.git

# 4. Stage and commit files
echo "[4/5] Staging files and creating commit..."
git add .github/ script.py index.html posts_log.json requirements.txt README.md .gitignore .env.example
git commit -m "feat: complete instagram threads auto-posting & monitoring system for github actions and pages"

# 5. Push to GitHub
echo "[5/5] Pushing to GitHub (origin main)..."
git push -u origin main

echo "=========================================================="
echo " Push process completed!"
echo " Live Dashboard will be at: https://xrahulyadav.github.io/the/"
echo "=========================================================="
