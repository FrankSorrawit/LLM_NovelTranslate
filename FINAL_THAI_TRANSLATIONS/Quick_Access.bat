@echo off
echo ===================================
echo    THAI NOVEL TRANSLATIONS
echo ===================================
echo.
echo Quick access to your translated novels:
echo.
echo [1] Open Complete Novels (Recommended)
echo [2] Open Chapter Collections  
echo [3] Open Individual Chapters
echo [4] Open Text File Backups
echo [5] Open Main Folder
echo [6] Exit
echo.
set /p choice="Choose option (1-6): "

if "%choice%"=="1" (
    explorer "FINAL_THAI_TRANSLATIONS\01_Complete_Novels"
) else if "%choice%"=="2" (
    explorer "FINAL_THAI_TRANSLATIONS\02_Chapter_Collections"
) else if "%choice%"=="3" (
    explorer "FINAL_THAI_TRANSLATIONS\03_Individual_Chapters"
) else if "%choice%"=="4" (
    explorer "FINAL_THAI_TRANSLATIONS\04_Text_Files_Backup"
) else if "%choice%"=="5" (
    explorer "FINAL_THAI_TRANSLATIONS"
) else if "%choice%"=="6" (
    exit
) else (
    echo Invalid choice!
    pause
    goto start
)
