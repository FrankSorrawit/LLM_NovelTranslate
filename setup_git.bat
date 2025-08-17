@echo off
echo ===================================
echo    GIT REPOSITORY SETUP
echo ===================================
echo.
echo This will help you set up and push to GitHub
echo.
echo Step 1: Initialize Git repository
git init
echo.
echo Step 2: Add all files
git add .
echo.
echo Step 3: Create initial commit
git commit -m "Initial commit: Thai Novel Translation System with working PDFs"
echo.
echo ===================================
echo    READY FOR GITHUB
echo ===================================
echo.
echo Next steps to push to GitHub:
echo.
echo 1. Create a new repository on GitHub
echo 2. Copy the repository URL
echo 3. Run these commands:
echo.
echo    git remote add origin [YOUR_GITHUB_URL]
echo    git branch -M main
echo    git push -u origin main
echo.
echo Your repository:
echo    git remote add origin git@github.com:FrankSorrawit/LLM_NovelTranslate.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo ===================================
echo.
pause