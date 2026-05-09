"""
Debug the blue route extraction process
"""

import os
import cv2
import numpy as np
from pathlib import Path

def debug_extraction_process(image_path):
    """Debug what's happening in the extraction process"""
    print("🔍 Debugging Blue Route Extraction")
    print("=" * 40)
    
    try:
        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            print("❌ Could not read image")
            return
        
        height, width = img.shape[:2]
        print(f"📏 Image size: {width}x{height}")
        
        # Convert BGR to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Test different blue ranges
        blue_ranges = [
            ("Loose", [100, 50, 50], [130, 255, 255]),
            ("Medium", [105, 80, 80], [125, 255, 255]),
            ("Strict", [105, 120, 120], [125, 255, 255]),
            ("Ultra", [110, 150, 150], [120, 255, 255])
        ]
        
        debug_dir = 'debug_extraction'
        Path(debug_dir).mkdir(parents=True, exist_ok=True)
        
        for name, lower, upper in blue_ranges:
            print(f"\n🔵 Testing {name} blue range: {lower} - {upper}")
            
            # Create mask
            lower_blue = np.array(lower)
            upper_blue = np.array(upper)
            blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
            
            # Count blue pixels
            blue_pixels = np.sum(blue_mask > 0)
            percentage = (blue_pixels / (width * height)) * 100
            print(f"   📊 Blue pixels: {blue_pixels} ({percentage:.2f}% of image)")
            
            # Find contours
            contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            print(f"   🔢 Found {len(contours)} contours")
            
            # Analyze contours
            significant_contours = 0
            for i, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                arc_length = cv2.arcLength(contour, False)
                
                if area > 50 and arc_length > 30:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = max(w, h) / min(w, h)
                    
                    if aspect_ratio > 2:
                        significant_contours += 1
                        if significant_contours <= 3:  # Show details for top 3
                            print(f"     🎯 Contour {i}: area={area:.0f}, length={arc_length:.0f}, ratio={aspect_ratio:.1f}")
            
            print(f"   ✅ Significant contours: {significant_contours}")
            
            # Save debug image
            debug_img = np.ones((height, width, 3), dtype=np.uint8) * 255
            debug_img[blue_mask > 0] = [255, 0, 0]  # Blue pixels
            debug_path = os.path.join(debug_dir, f"debug_{name.lower()}_range.png")
            cv2.imwrite(debug_path, debug_img)
            print(f"   💾 Saved debug image: {debug_path}")
        
        print(f"\n📁 Check debug images in '{debug_dir}' folder")
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Test with the test image
    test_image = "test_extraction/test_image.png"
    
    if os.path.exists(test_image):
        debug_extraction_process(test_image)
    else:
        print(f"❌ Test image not found: {test_image}")
        print("Run test_route_extraction.py first to create test images")
