import sys
sys.path.append('.')

from simple_converter import extract_blue_lines_with_labels, create_enhanced_word_document_with_labels

def test_enhanced_features():
    """Test the enhanced route extraction with labels and landmarks"""
    
    print("🚀 Testing Enhanced Route Extraction with Labels...")
    print("=" * 60)
    
    # Input parameters
    image_path = "Image1.jpg"
    source_name = "Home 🏠"
    destination_name = "Office 🏢"
    
    # Output files
    enhanced_route_image = "simple_output/enhanced_route_with_labels.png"
    enhanced_document = "simple_output/enhanced_route_document_with_labels.docx"
    
    print(f"📍 Source: {source_name}")
    print(f"📍 Destination: {destination_name}")
    print()
    
    # Step 1: Extract route with labels
    print("Step 1: Extracting blue route with source/destination labels...")
    try:
        result_path, landmarks = extract_blue_lines_with_labels(
            image_path, 
            enhanced_route_image, 
            source_name, 
            destination_name
        )
        
        print(f"✅ Route extracted successfully!")
        print(f"   📁 Image saved: {result_path}")
        print(f"   📍 Landmarks found: {len(landmarks)}")
        
        for landmark in landmarks:
            print(f"      • {landmark['name']} ({landmark['type']}): ({landmark['x']}, {landmark['y']})")
        
    except Exception as e:
        print(f"❌ Route extraction failed: {e}")
        return
    
    print()
    
    # Step 2: Create enhanced document
    print("Step 2: Creating enhanced Word document...")
    try:
        doc_path = create_enhanced_word_document_with_labels(
            image_path=image_path,
            route_image_path=result_path,
            landmarks=landmarks,
            source=source_name,
            destination=destination_name,
            output_path=enhanced_document
        )
        
        print(f"✅ Enhanced document created!")
        print(f"   📄 Document saved: {doc_path}")
        
    except Exception as e:
        print(f"❌ Document creation failed: {e}")
        return
    
    print()
    print("🎉 ENHANCED FEATURES SUCCESSFULLY IMPLEMENTED!")
    print("=" * 60)
    print("✨ New Features Added:")
    print("   🏷️  Source and destination names displayed at dots")
    print("   🧭 Compass directions in lower right corner")
    print("   🎯 Enhanced landmarks section with emojis")
    print("   📊 Professional document formatting")
    print("   📐 Coordinate and distance information")
    print("   🗺️  Multiple reference sections")
    print()
    print("📁 Files Created:")
    print(f"   🖼️  Enhanced Route Image: {enhanced_route_image}")
    print(f"   📄 Enhanced Document: {enhanced_document}")
    print()
    print("🎯 What to Check:")
    print("   1. Open the enhanced route image to see labels on dots")
    print("   2. Open the Word document to see landmarks and compass")
    print("   3. Notice the professional formatting and detailed sections")

if __name__ == "__main__":
    test_enhanced_features()
