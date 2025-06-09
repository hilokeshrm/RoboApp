@echo off
echo =============================================
echo    🚀 OLLAMA CHAT SERVER WITH LOGGING
echo =============================================
echo.
echo 🔍 NEW: Detailed logging is now enabled!
echo 📝 All activity will be logged to:
echo     - Console (this window)
echo     - File: ollama_chat_server.log
echo.
echo 📋 You'll see detailed information about:
echo     • Incoming requests from Flutter/Web
echo     • Communication with Ollama
echo     • Streaming token details
echo     • Response times and errors
echo.
echo Checking if Ollama is running...
curl -s http://localhost:11434/api/version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Ollama is not running!
    echo Please start Ollama first, then run this script again.
    pause
    exit /b 1
)

echo ✅ Ollama is running!
echo.
echo 🚀 Starting Flask server with detailed logging...
echo 📋 Watch this console for real-time activity!
echo.
python ollama_chat_server.py

echo.
echo 📋 Server stopped. Check ollama_chat_server.log for session details.
echo Press any key to exit...
pause >nul

