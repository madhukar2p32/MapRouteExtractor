"""
Test the improved blue route extraction
"""

import os
import sys
import cv2
import numpy as np
from pathlib import Path

def create_test_image():
    """Create a test image with a blue route line and noise"""
    # Create a white image
    img = np.ones((400, 600, 3), dtype=np.uint8) * 255
    
    # Add some background elements (non-blue)
    cv2.rectangle(img, (50, 50), (150, 100), (200, 200, 200), -1)  # Gray rectangle
    cv2.circle(img, (400, 300), 30, (0, 200, 0), -1)  # Green circle
    
    # Add the main blue route line
    cv2.line(img, (100, 350), (500, 50), (255, 0, 0), 5)  # Main blue route
    
    # Add some blue noise (smaller elements)
    cv2.circle(img, (200, 200), 3, (200, 0, 0), -1)  # Small blue dot
    cv2.circle(img, (300, 150), 2, (180, 0, 0), -1)  # Another small blue dot
    
    # Add a shorter blue line (should be filtered out)
    cv2.line(img, (450, 300), (470, 320), (220, 0, 0), 2)
    
    return img

def test_route_extraction():
    """Test the route extraction functions"""
    print("🧪 Testing Blue Route Extraction")
    print("=" * 35)
    
    try:
        # Import the functions
        from simple_converter import extract_main_route_line, extract_blue_lines_from_image
        
        # Create test directory
        test_dir = 'test_extraction'
        Path(test_dir).mkdir(parents=True, exist_ok=True)
        
        # Create test image
        test_img = create_test_image()
        test_img_path = os.path.join(test_dir, 'test_image.png')
        cv2.imwrite(test_img_path, test_img)
        print(f"✅ Test image created: {test_img_path}")
        
        # Test old method (all blue extraction)
        old_output_path = os.path.join(test_dir, 'old_method_output.png')
        old_result, old_landmarks = extract_blue_lines_from_image(test_img_path, old_output_path)
        print(f"📊 Old method found {len(old_landmarks)} landmarks")
        
        # Test new method (main route only)
        new_output_path = os.path.join(test_dir, 'new_method_output.png')
        new_result, new_landmarks = extract_main_route_line(test_img_path, new_output_path)
        print(f"📊 New method found {len(new_landmarks)} landmarks")
        
        # Show results
        print("\n📋 Comparison Results:")
        print(f"   Original image: {test_img_path}")
        print(f"   Old method output: {old_output_path}")
        print(f"   New method output: {new_output_path}")
        
        print("\n🔍 Old Method Landmarks:")
        for landmark in old_landmarks:
            print(f"   • {landmark['name']} at ({landmark['x']}, {landmark['y']})")
            
        print("\n🎯 New Method Landmarks:")
        for landmark in new_landmarks:
            print(f"   • {landmark['name']} at ({landmark['x']}, {landmark['y']})")
            
        print(f"\n✅ Test completed! Check the outputs in '{test_dir}' folder")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_route_extraction()
    print(f"\n{'🎉 Test successful!' if success else '💥 Test failed!'}")
    sys.exit(0 if success else 1)
