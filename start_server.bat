@echo off
echo ========================================
echo         Ollama Chat Server
echo ========================================
echo.
echo Checking if Ollama is running...
curl -s http://localhost:11434/api/version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Ollama is not running!
    echo Please start Ollama first, then run this script again.
    pause
    exit /b 1
)

echo Ollama is running ✓
echo.
echo Starting Flask server...
echo.
python ollama_chat_server.py

echo.
echo Server stopped. Press any key to exit...
pause >nul

