import cv2
import numpy as np
from simple_converter import extract_blue_lines_from_image

def diagnose_current_output():
    """Check what's actually being produced vs what you're seeing"""
    print("🔍 DIAGNOSING CURRENT OUTPUT...")
    
    # Test extraction
    image_path = "Image1.jpg"
    output_path = "diagnostic_output.png"
    
    result_path, landmarks = extract_blue_lines_from_image(image_path, output_path)
    
    print(f"\n📊 EXTRACTION RESULTS:")
    print(f"  - Landmarks found: {len(landmarks)}")
    for lm in landmarks:
        print(f"    * {lm['name']}: ({lm['x']}, {lm['y']})")
    
    # Load and analyze the output image
    output_img = cv2.imread(output_path)
    if output_img is not None:
        print(f"\n🖼️  OUTPUT IMAGE ANALYSIS:")
        print(f"  - Dimensions: {output_img.shape}")
        
        # Check what colors are in the output
        unique_colors = set()
        h, w = output_img.shape[:2]
        
        # Sample some pixels to see what we have
        for y in range(0, h, 50):
            for x in range(0, w, 50):
                b, g, r = output_img[y, x]
                unique_colors.add((r, g, b))
        
        print(f"  - Unique colors found: {len(unique_colors)}")
        
        # Check specifically for blue pixels
        blue_mask = (output_img[:,:,0] > 200) & (output_img[:,:,1] < 100) & (output_img[:,:,2] < 100)  # Blue in BGR
        blue_pixels = np.sum(blue_mask)
        
        # Check for white pixels (background)
        white_mask = (output_img[:,:,0] > 200) & (output_img[:,:,1] > 200) & (output_img[:,:,2] > 200)
        white_pixels = np.sum(white_mask)
        
        print(f"  - Blue pixels: {blue_pixels}")
        print(f"  - White pixels: {white_pixels}")
        print(f"  - Total pixels: {h * w}")
        
        # Check if image is mostly white (which would mean extraction worked)
        if white_pixels > (h * w * 0.8):
            print("  ✅ Output appears to be clean (mostly white background)")
        else:
            print("  ❌ Output may still contain original image data")
            
        # Look for non-white, non-blue pixels (leftover noise)
        non_clean_mask = ~(blue_mask | white_mask)
        noise_pixels = np.sum(non_clean_mask)
        
        if noise_pixels > (h * w * 0.1):
            print(f"  ⚠️  WARNING: {noise_pixels} pixels are neither blue nor white (potential noise)")
        else:
            print(f"  ✅ Clean output: only {noise_pixels} noise pixels")
    
    print(f"\n📁 Files created:")
    print(f"  - Output image: {output_path}")
    print(f"  - You can check this image to see what's actually being produced")
    
    # Also check what the web app would produce
    print(f"\n🌐 WEB APP STATUS:")
    print(f"  - If you uploaded via web app, check: simple_output/ folder")
    print(f"  - Latest files will have today's timestamp: 20250713")

if __name__ == "__main__":
    diagnose_current_output()
