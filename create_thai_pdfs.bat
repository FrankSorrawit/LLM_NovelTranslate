@echo off
echo ===================================
echo    THAI PDF CREATOR
echo ===================================
echo.
echo This will create Thai PDFs with proper font support
echo.
echo Step 1: Fix text formatting...
python format_fixer.py
echo.
echo Step 2: Create Thai PDFs...
python thai_pdf_fixer.py
echo.
echo ✅ Thai PDFs created!
echo Check these files:
echo - matriarch_thai_font.pdf
echo - viridescent_thai_font.pdf
echo.
pause