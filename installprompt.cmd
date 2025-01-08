REM Install necessary Python packages using pip
@echo off

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

REM Create a temporary requirements file
echo os > requirements.txt
echo pyperclip >> requirements.txt
echo platform >> requirements.txt
echo psutil >> requirements.txt
echo socket >> requirements.txt
echo datetime >> requirements.txt
echo base64 >> requirements.txt
echo hashlib >> requirements.txt
echo requests >> requirements.txt
echo difflib >> requirements.txt
echo mmap >> requirements.txt
echo struct >> requirements.txt

REM Install the packages
pip install -r requirements.txt

REM Clean up
del requirements.txt

REM Done
echo All packages have been installed.
pause
