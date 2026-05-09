@echo off
echo ========================================
echo   Map Route Extractor - Web Application
echo ========================================
echo.
echo Starting server...
echo Access at: http://localhost:5000
echo Press Ctrl+C to stop
echo.
"%~dp0venv\Scripts\python.exe" "%~dp0app.py"
echo.
echo Server stopped.
pause
