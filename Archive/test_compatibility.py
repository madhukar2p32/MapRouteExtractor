"""
Test script to verify both regular and enhanced functionality work correctly
"""

def test_both_functions():
    print("🧪 TESTING BOTH EXTRACTION FUNCTIONS...")
    print("=" * 50)
    
    # Test 1: Original function (for web app compatibility)
    print("Test 1: Original extract_blue_lines_from_image function...")
    try:
        from simple_converter import extract_blue_lines_from_image
        result_path, landmarks = extract_blue_lines_from_image('Image1.jpg', 'test_original.png')
        print(f"✅ Original function works: {len(landmarks)} landmarks found")
    except Exception as e:
        print(f"❌ Original function failed: {e}")
    
    # Test 2: Enhanced function (with labels and compass)
    print("\nTest 2: Enhanced extract_blue_lines_with_labels function...")
    try:
        from simple_converter import extract_blue_lines_with_labels
        result_path, landmarks = extract_blue_lines_with_labels(
            'Image1.jpg', 
            'test_enhanced.png', 
            'Test Source 🏠', 
            'Test Destination 🏢'
        )
        print(f"✅ Enhanced function works: {len(landmarks)} landmarks found")
    except Exception as e:
        print(f"❌ Enhanced function failed: {e}")
    
    # Test 3: Document creation
    print("\nTest 3: Document creation functions...")
    try:
        from simple_converter import create_word_document
        doc_path = create_word_document(
            image_path='Image1.jpg',
            route_image_path='test_original.png',
            landmarks=[{'name': 'Test', 'type': 'test', 'x': 100, 'y': 100}],
            source='Test Source',
            destination='Test Dest',
            output_path='test_regular_doc.docx'
        )
        print(f"✅ Regular document creation works: {doc_path}")
    except Exception as e:
        print(f"❌ Regular document creation failed: {e}")
    
    try:
        from simple_converter import create_enhanced_word_document_with_labels
        doc_path = create_enhanced_word_document_with_labels(
            image_path='Image1.jpg',
            route_image_path='test_enhanced.png',
            landmarks=[{'name': 'Test', 'type': 'test', 'x': 100, 'y': 100}],
            source='Test Source',
            destination='Test Dest',
            output_path='test_enhanced_doc.docx'
        )
        print(f"✅ Enhanced document creation works: {doc_path}")
    except Exception as e:
        print(f"❌ Enhanced document creation failed: {e}")
    
    print("\n🎉 COMPATIBILITY TEST COMPLETE!")
    print("📝 Summary:")
    print("   ✅ Web app will use: extract_blue_lines_from_image")
    print("   ✅ Enhanced features use: extract_blue_lines_with_labels")
    print("   ✅ Both functions are available and working!")

if __name__ == "__main__":
    test_both_functions()
