"""
URGENT FIX: Start the improved web server
"""
from simple_converter import app
import webbrowser
import threading
import time

def open_browser():
    time.sleep(2)
    webbrowser.open('http://localhost:5001')

if __name__ == '__main__':
    print("🚀 STARTING IMPROVED BLUE ROUTE EXTRACTOR")
    print("=" * 50)
    print("🔧 IMPROVEMENTS ACTIVE:")
    print("  ✅ Single main route extraction") 
    print("  ✅ Better filtering algorithm")
    print("  ✅ Clean output generation")
    print("=" * 50)
    print("🌐 Opening browser to: http://localhost:5001")
    print("📁 Check this file: simple_output/IMPROVED_OUTPUT_150802.png")
    print("=" * 50)
    
    # Open browser after a delay
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=5001, debug=False)
