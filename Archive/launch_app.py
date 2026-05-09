"""
Simple Flask App Launcher
"""

import sys
import os

def start_app():
    """Start the Flask application"""
    print("🚀 Starting Map Route Extractor...")
    print("=" * 40)
    
    try:
        # Import and start the Flask app
        from app import app
        
        print("✅ Flask app loaded successfully")
        print("🌐 Starting server on http://localhost:5000")
        print("🛑 Press Ctrl+C to stop")
        print("-" * 40)
        
        # Start the Flask development server
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=True,
            use_reloader=False  # Disable reloader to avoid issues
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start_app()
