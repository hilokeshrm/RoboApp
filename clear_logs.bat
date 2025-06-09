@echo off
echo Clearing server logs...
if exist ollama_chat_server.log (
    del ollama_chat_server.log
    echo ✅ Log file cleared successfully!
) else (
    echo ℹ️  No log file found.
)
echo.
echo You can now start the server with fresh logs.
pause

