#!/usr/bin/env python3
"""
Simple web server launcher for the Blue Route Extractor
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def start_server():
    """Start the Flask server"""
    try:
        print("🚀 Starting Blue Route Extractor Web Application...")
        print("📍 Application URL: http://localhost:5001")
        print("💡 The app will open in your browser automatically")
        print("🔄 Processing improvements: Single main route extraction")
        print("\n⏳ Starting server...")
        
        # Start the Flask app
        result = subprocess.run([
            sys.executable, 'simple_converter.py'
        ], check=True, capture_output=False)
        
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("💡 Try running: python simple_converter.py")

if __name__ == "__main__":
    start_server()
