@echo off
cd /d "%~dp0"
python app.py
if errorlevel 1 python3 app.py
pause
