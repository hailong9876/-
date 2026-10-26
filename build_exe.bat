@echo off
setlocal
python -m pip install -r requirements.txt
pyinstaller --noconfirm --onefile --windowed --name AutoClicker clicker.py
if exist dist\AutoClicker.exe (
    echo.
    echo EXE built successfully: dist\AutoClicker.exe
) else (
    echo.
    echo Build failed. Please check the error log.
)
pause
