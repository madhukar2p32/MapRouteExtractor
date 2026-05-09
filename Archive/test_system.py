"""
Simple test for the Map Route Extractor system
"""

import sys
import os

def test_basic_functionality():
    """Test basic system functionality"""
    print("🧭 Map Route Extractor System Test")
    print("=" * 40)
    
    # Test imports
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
        
        import matplotlib.pyplot as plt
        print("✅ Matplotlib imported successfully")
        
        from PIL import Image
        print("✅ Pillow imported successfully")
        
        import cv2
        print("✅ OpenCV imported successfully")
        
        from flask import Flask
        print("✅ Flask imported successfully")
        
        print("\n📦 All core dependencies are working!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test basic functionality
    try:
        # Test route extractor logic
        from route_extractor import MapRouteExtractor
        extractor = MapRouteExtractor()
        print("✅ Route extractor initialized")
        
        # Test document generator
        from document_generator import RouteDocumentGenerator
        generator = RouteDocumentGenerator(use_hf_models=False)
        print("✅ Document generator initialized")
        
        # Test sample data processing
        route_data = {
            'source': 'Home',
            'destination': 'NTR Garden',
            'direction': 'North-East',
            'landmarks': [
                {'name': 'Reliance Digital', 'type': 'store'},
                {'name': 'Mia by Tanishq', 'type': 'store'},
                {'name': 'SNITCH - Toli Chowki', 'type': 'store'},
                {'name': 'Nehru Zoological Park', 'type': 'park'},
                {'name': 'Aziz Plaza', 'type': 'plaza'}
            ]
        }
        
        # Create directories
        os.makedirs('output', exist_ok=True)
        os.makedirs('uploads', exist_ok=True)
        os.makedirs('temp', exist_ok=True)
        
        # Test visualization
        viz_path = os.path.join('output', 'test_route_visualization.png')
        extractor.create_simplified_route_visualization(
            route_data['source'], 
            route_data['destination'], 
            route_data['landmarks'], 
            route_data['direction'], 
            viz_path
        )
        print(f"✅ Route visualization created: {viz_path}")
        
        # Test document generation
        doc_path = generator.generate_route_document(route_data, 'output', 'html')
        print(f"✅ Document generated: {doc_path}")
        
        print("\n🎉 All tests passed! System is ready to use.")
        print("\n📋 Next steps:")
        print("1. Run: python app.py")
        print("2. Open: http://localhost:5000")
        print("3. Upload your map image and test the system")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)
