@echo off
echo Checking for Python Virtual Environment...

if not exist venv (
    echo Creating venv...
    python -m venv venv
)

echo Installing dependencies...
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install pygame pyinstaller

echo Setup complete. You can now run the Build Task (Ctrl+Shift+B).
pause
