import cv2
import numpy as np
from simple_converter import extract_blue_lines_from_image

def test_improved_extraction():
    """Test the improved extraction with more realistic thresholds"""
    print("Testing improved blue line extraction...")
    
    # Test with the actual image
    test_image = r"c:\Users\Madhukar K\Desktop\Python_Code\MapRouteExtractor\Image1.jpg"
    output_image = r"c:\Users\Madhukar K\Desktop\Python_Code\MapRouteExtractor\test_extraction\improved_output.png"
    
    # Run the extraction
    result_path, landmarks = extract_blue_lines_from_image(test_image, output_image)
    
    print(f"Extraction completed!")
    print(f"Result saved to: {result_path}")
    print(f"Landmarks found: {len(landmarks)}")
    
    for i, landmark in enumerate(landmarks):
        print(f"  {i+1}. {landmark['name']} ({landmark['type']}): ({landmark['x']}, {landmark['y']})")
    
    # Also show what blue pixels we're detecting
    img = cv2.imread(test_image)
    if img is not None:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Test multiple blue ranges
        ranges = [
            ("Standard", [100, 80, 80], [130, 255, 255]),
            ("Narrow", [105, 100, 100], [125, 255, 255]),
            ("Wide", [90, 50, 50], [140, 255, 255])
        ]
        
        for name, lower, upper in ranges:
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            blue_pixels = np.sum(mask > 0)
            total_pixels = mask.shape[0] * mask.shape[1]
            percentage = (blue_pixels / total_pixels) * 100
            
            print(f"\n{name} range {lower}-{upper}:")
            print(f"  Blue pixels: {blue_pixels} ({percentage:.2f}%)")
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            print(f"  Contours found: {len(contours)}")
            
            # Analyze contours
            for i, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                arc_length = cv2.arcLength(contour, False)
                if area > 10 or arc_length > 10:  # Show any reasonable contour
                    print(f"    Contour {i+1}: area={area:.1f}, length={arc_length:.1f}")

if __name__ == "__main__":
    test_improved_extraction()
