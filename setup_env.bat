@echo off
echo Checking for Python Virtual Environment...

if not exist venv (
    echo Creating venv...
    python -m venv venv
)

echo Installing/Upgrading essential build tools...
venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel

echo Installing Atomic Adventure dependencies...
:: We use --only-binary to prevent it from trying to 'build' from source again
venv\Scripts\python.exe -m pip install pygame==2.6.1 --only-binary=:all:
venv\Scripts\python.exe -m pip install pyinstaller

echo Setup complete. You can now run the Build Task (Ctrl+Shift+B).
pause
