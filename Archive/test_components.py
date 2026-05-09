"""
Simple test to verify all components work
"""

def test_components():
    print("🔧 Testing System Components")
    print("=" * 30)
    
    # Test 1: Basic imports
    try:
        import cv2
        print("✅ OpenCV (cv2) imported successfully")
    except ImportError as e:
        print(f"❌ OpenCV not available: {e}")
    
    try:
        from PIL import Image
        print("✅ Pillow (PIL) imported successfully")
    except ImportError as e:
        print(f"❌ Pillow not available: {e}")
    
    try:
        import matplotlib.pyplot as plt
        print("✅ Matplotlib imported successfully")
    except ImportError as e:
        print(f"❌ Matplotlib not available: {e}")
    
    try:
        from flask import Flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask not available: {e}")
    
    # Test 2: Our modules
    try:
        from route_extractor import MapRouteExtractor
        print("✅ MapRouteExtractor imported successfully")
        
        extractor = MapRouteExtractor()
        print("✅ MapRouteExtractor initialized")
        
    except Exception as e:
        print(f"❌ Route extractor error: {e}")
    
    try:
        from document_generator import RouteDocumentGenerator
        print("✅ RouteDocumentGenerator imported successfully")
        
        generator = RouteDocumentGenerator(use_hf_models=False)
        print("✅ RouteDocumentGenerator initialized (basic mode)")
        
    except Exception as e:
        print(f"❌ Document generator error: {e}")
    
    print("\n🏁 Component test completed!")

if __name__ == "__main__":
    test_components()
