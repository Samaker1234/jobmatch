@echo off
REM Lancer l'application Flask AgriOrbit via l'environnement virtuel
title JobMath - Serveur Flask
color 0B

echo ===================================================
echo           JobMath - SYSTEME DE GESTION
echo ===================================================
echo.
echo Lancement du serveur Flask...
echo L'interface est disponible sur : http://localhost:5000
echo.
echo [INFO] Appuyez sur Ctrl+C pour arreter le serveur.
echo ---------------------------------------------------

set FLASK_APP=app.py
set FLASK_ENV=development

python app.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERREUR] Le serveur s'est arrete. Assurez-vous d'avoir installe les dependances:
    echo pip install -r requirements.txt
    pause
)
