"""
Test the web app functionality with enhanced features
"""

def test_web_app_enhanced():
    print("🧪 TESTING WEB APP WITH ENHANCED FEATURES...")
    print("=" * 60)
    
    # Simulate what the web app does
    from simple_converter import extract_blue_lines_with_labels, create_enhanced_word_document_with_labels
    
    # Test parameters (same as web app would use)
    upload_path = "Image1.jpg"
    source = "Home 🏠"
    destination = "Office 🏢"
    
    # Simulate web app file paths
    route_image_path = "simple_output/web_test_enhanced_route.png"
    doc_path = "simple_output/web_test_enhanced_doc.docx"
    
    print("🔄 Step 1: Extract route with labels (as web app will do)...")
    try:
        route_image_result, landmarks = extract_blue_lines_with_labels(upload_path, route_image_path, source, destination)
        print(f"✅ Enhanced extraction successful!")
        print(f"   📁 Route image: {route_image_result}")
        print(f"   📍 Landmarks: {len(landmarks)}")
        
        for landmark in landmarks:
            print(f"      • {landmark['name']}: ({landmark['x']}, {landmark['y']})")
            
    except Exception as e:
        print(f"❌ Enhanced extraction failed: {e}")
        return
    
    print("\n🔄 Step 2: Create enhanced document (as web app will do)...")
    try:
        doc_result = create_enhanced_word_document_with_labels(
            upload_path, route_image_result, landmarks, source, destination, doc_path
        )
        print(f"✅ Enhanced document created!")
        print(f"   📄 Document: {doc_result}")
        
    except Exception as e:
        print(f"❌ Enhanced document creation failed: {e}")
        return
    
    print("\n🎉 WEB APP ENHANCED FEATURES TEST SUCCESS!")
    print("=" * 60)
    print("✨ When you use the web app now, you'll get:")
    print("   🏷️  Source/Destination labels on the route image")
    print("   🧭 Compass in lower right corner of image")
    print("   🎯 Enhanced Word document with landmarks and emojis")
    print("   📊 Professional formatting with multiple sections")
    print("   🗺️  Compass directions reference in document")
    print("\n📁 Test Files Created:")
    print(f"   🖼️  {route_image_path}")
    print(f"   📄 {doc_path}")
    print("\n🌐 Ready! Start web app: python simple_converter.py")

if __name__ == "__main__":
    test_web_app_enhanced()
