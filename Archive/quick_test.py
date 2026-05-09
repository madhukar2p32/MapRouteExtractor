from simple_converter import extract_blue_lines_from_image, create_document_with_route

def quick_test():
    """Quick test of the complete process"""
    print("Testing complete blue route extraction process...")
    
    # Input and output paths
    image_path = r"c:\Users\Madhukar K\Desktop\Python_Code\MapRouteExtractor\Image1.jpg"
    output_image = r"c:\Users\Madhukar K\Desktop\Python_Code\MapRouteExtractor\simple_output\quick_test_blue_route.png"
    output_doc = r"c:\Users\Madhukar K\Desktop\Python_Code\MapRouteExtractor\simple_output\quick_test_route.docx"
    
    # Extract the blue route
    result_path, landmarks = extract_blue_lines_from_image(image_path, output_image)
    
    print(f"✅ Blue route extracted!")
    print(f"   Image saved to: {result_path}")
    print(f"   Landmarks found: {len(landmarks)}")
    
    for landmark in landmarks:
        print(f"   - {landmark['name']} ({landmark['type']}): ({landmark['x']}, {landmark['y']})")
    
    # Create document
    try:
        doc_path = create_document_with_route(
            original_image=image_path,
            processed_image=result_path,
            source="Home",
            destination="Office",
            landmarks=landmarks,
            filename=output_doc
        )
        print(f"✅ Document created: {doc_path}")
        
    except Exception as e:
        print(f"❌ Document creation failed: {e}")
    
    print("\n🎉 Test complete! Check the simple_output folder for results.")

if __name__ == "__main__":
    quick_test()
