@echo off
echo ===================================
echo    PUSHING TO YOUR GITHUB REPO
echo ===================================
echo.
echo Repository: git@github.com:FrankSorrawit/LLM_NovelTranslate.git
echo.
echo Step 1: Initialize Git (if not done)
git init
echo.
echo Step 2: Add all files
git add .
echo.
echo Step 3: Create initial commit
git commit -m "Initial commit: Thai Novel Translation System with working PDFs"
echo.
echo Step 4: Connect to your GitHub repository
git remote add origin git@github.com:FrankSorrawit/LLM_NovelTranslate.git
echo.
echo Step 5: Set main branch
git branch -M main
echo.
echo Step 6: Push to GitHub
git push -u origin main
echo.
echo ===================================
echo    UPLOAD COMPLETE!
echo ===================================
echo.
echo Your repository is now available at:
echo https://github.com/FrankSorrawit/LLM_NovelTranslate
echo.
echo Files uploaded:
echo ✅ Final working PDFs (matriarch_thai_font.pdf, viridescent_thai_font.pdf)
echo ✅ Translation scripts
echo ✅ Configuration files
echo ✅ Documentation (Thai/English)
echo ✅ Source novels
echo.
echo ❌ Text files excluded (as requested)
echo ❌ Large folders excluded
echo.
pause