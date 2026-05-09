@echo off
echo ==========================================
echo   Map Route Extractor - Direct Converter
echo ==========================================
echo.
echo Upload a map image, get a Word document instantly.
echo.
echo Starting server...
echo Access at: http://localhost:5001
echo Press Ctrl+C to stop
echo.
"%~dp0venv\Scripts\python.exe" "%~dp0simple_converter.py"
echo.
echo Server stopped.
pause
