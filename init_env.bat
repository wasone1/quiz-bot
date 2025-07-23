@echo off
REM Перевірка наявності Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Помилка: Python не знайдено. Встановіть Python 3.8+ і додайте його в PATH.
    pause
    exit /b
)

REM Створення venv
python -m venv venv
if %errorlevel% neq 0 (
    echo Помилка при створенні venv.
    pause
    exit /b
)

REM Активація та встановлення залежностей
call venv\Scripts\activate.bat
pip install --upgrade pip
if exist requirements.txt (
    pip install -r requirements.txt
    echo Залежності встановлено!
) else (
    echo Файл requirements.txt не знайдено. Створіть його командою: pip freeze > requirements.txt
)

echo Середовище готове! Для активації виконайте: call venv\Scripts\activate.bat
pause