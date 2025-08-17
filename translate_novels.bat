@echo off
echo ===================================
echo    DUAL NOVEL TRANSLATION SYSTEM
echo ===================================
echo.
echo Installing required packages...
pip install -r requirements.txt
echo.
echo Starting interactive translation menu...
echo.
python start_translation.py
echo.
pause