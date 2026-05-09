import sys
sys.path.append('.')

# Import both regular and enhanced functions
from simple_converter import (
    extract_blue_lines_from_image,           # Original (for web app compatibility)
    extract_blue_lines_with_labels,         # Enhanced (with labels and compass)
    create_word_document,                    # Original document creation
    create_enhanced_word_document_with_labels # Enhanced document creation
)

print("🚀 COMPLETE TEST - Both Regular and Enhanced Features")
print("=" * 60)

# Test parameters
image_path = "Image1.jpg"
source_name = "Home 🏠"
destination_name = "Office 🏢"

print("TEST 1: Regular Extraction (Web App Compatible)")
print("-" * 50)
result_path1, landmarks1 = extract_blue_lines_from_image(image_path, "simple_output/regular_route.png")
print(f"✅ Regular extraction: {len(landmarks1)} landmarks")
for landmark in landmarks1:
    print(f"   • {landmark['name']}: ({landmark['x']}, {landmark['y']})")

print("\nTEST 2: Enhanced Extraction (With Labels & Compass)")
print("-" * 50)
result_path2, landmarks2 = extract_blue_lines_with_labels(image_path, "simple_output/enhanced_route.png", source_name, destination_name)
print(f"✅ Enhanced extraction: {len(landmarks2)} landmarks")
for landmark in landmarks2:
    print(f"   • {landmark['name']}: ({landmark['x']}, {landmark['y']})")

print("\nTEST 3: Document Creation")
print("-" * 50)

# Regular document
if landmarks1:
    doc_path1 = create_word_document(
        image_path=image_path,
        route_image_path=result_path1,
        landmarks=landmarks1,
        source=source_name,
        destination=destination_name,
        output_path="simple_output/regular_document.docx"
    )
    print(f"✅ Regular document: {doc_path1}")

# Enhanced document
if landmarks2:
    doc_path2 = create_enhanced_word_document_with_labels(
        image_path=image_path,
        route_image_path=result_path2,
        landmarks=landmarks2,
        source=source_name,
        destination=destination_name,
        output_path="simple_output/enhanced_document.docx"
    )
    print(f"✅ Enhanced document: {doc_path2}")

print("\n🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
print("=" * 60)
print("📁 Files Generated:")
print("   🖼️  Regular route: simple_output/regular_route.png")
print("   🖼️  Enhanced route: simple_output/enhanced_route.png (with labels & compass)")
print("   � Regular document: simple_output/regular_document.docx")
print("   📄 Enhanced document: simple_output/enhanced_document.docx")
print("\n💡 Usage:")
print("   • Web app uses the regular function automatically")
print("   • Use enhanced functions for custom scripts with labels & compass")
print("   • Both provide the same high-quality single route extraction!")
