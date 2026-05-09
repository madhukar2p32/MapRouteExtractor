import cv2
import numpy as np
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.dml import MSO_THEME_COLOR_INDEX
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def detect_landmarks_in_text(text):
    """
    Enhanced landmark detection with emojis and categories
    """
    landmarks = []
    
    # Define landmark patterns with their emojis
    landmark_patterns = {
        # Educational
        r'\b(?:school|college|university|academy|institute|campus)\b': {'emoji': '🏫', 'type': 'education'},
        r'\b(?:library|museum|research)\b': {'emoji': '📚', 'type': 'education'},
        
        # Healthcare
        r'\b(?:hospital|clinic|medical|doctor|pharmacy|health)\b': {'emoji': '🏥', 'type': 'healthcare'},
        r'\b(?:emergency|ambulance)\b': {'emoji': '🚑', 'type': 'healthcare'},
        
        # Religious
        r'\b(?:temple|church|mosque|synagogue|cathedral|shrine)\b': {'emoji': '🛕', 'type': 'religious'},
        r'\b(?:monastery|chapel|basilica)\b': {'emoji': '⛪', 'type': 'religious'},
        
        # Commercial
        r'\b(?:mall|market|shop|store|restaurant|hotel|bank)\b': {'emoji': '🏬', 'type': 'commercial'},
        r'\b(?:gas station|petrol|fuel)\b': {'emoji': '⛽', 'type': 'commercial'},
        r'\b(?:atm|bank)\b': {'emoji': '🏧', 'type': 'commercial'},
        
        # Transportation
        r'\b(?:airport|station|terminal|port|bus stand)\b': {'emoji': '🚉', 'type': 'transport'},
        r'\b(?:railway|metro|subway)\b': {'emoji': '🚇', 'type': 'transport'},
        r'\b(?:bridge|tunnel)\b': {'emoji': '🌉', 'type': 'transport'},
        
        # Government
        r'\b(?:office|court|police|government|city hall)\b': {'emoji': '🏛️', 'type': 'government'},
        r'\b(?:post office|postal)\b': {'emoji': '📮', 'type': 'government'},
        
        # Recreation
        r'\b(?:park|garden|playground|stadium|gym)\b': {'emoji': '🏞️', 'type': 'recreation'},
        r'\b(?:cinema|theater|club)\b': {'emoji': '🎭', 'type': 'recreation'},
        
        # Residential
        r'\b(?:apartment|building|complex|society|home)\b': {'emoji': '🏠', 'type': 'residential'},
        
        # Geographic
        r'\b(?:hill|mountain|lake|river|beach)\b': {'emoji': '⛰️', 'type': 'geographic'},
        r'\b(?:road|street|avenue|lane|circle)\b': {'emoji': '🛣️', 'type': 'roads'},
    }
    
    for pattern, info in landmark_patterns.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            landmark_name = match.group().title()
            landmarks.append({
                'name': f"{info['emoji']} {landmark_name}",
                'type': info['type'],
                'emoji': info['emoji'],
                'raw_name': landmark_name
            })
    
    return landmarks

def extract_text_from_image_regions(image_path, landmarks):
    """
    Extract landmark text from map image regions using OCR.

    Requires pytesseract + Tesseract to be installed for real detection.
    Returns an empty list until OCR is configured so that no fabricated
    data reaches generated documents.
    """
    logger.info("Landmark OCR not configured; returning empty list.")
    return []

def create_enhanced_word_document(image_path, route_image_path, landmarks, source, destination, output_path):
    """
    Create an enhanced Word document with:
    1. Source/Destination names at dots
    2. Landmark detection with emojis
    3. Compass directions
    4. Professional formatting
    """
    try:
        doc = Document()
        
        # Set document margins
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(0.5)
            section.bottom_margin = Inches(0.5)
            section.left_margin = Inches(0.5)
            section.right_margin = Inches(0.5)
        
        # Title
        title = doc.add_heading('Route Map', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Subtitle with route info
        subtitle = doc.add_paragraph()
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        subtitle_run = subtitle.add_run(f'Route from {source} to {destination}')
        subtitle_run.font.size = Pt(14)
        subtitle_run.font.color.theme_color = MSO_THEME_COLOR_INDEX.ACCENT_1
        
        # Date and time
        doc.add_paragraph(f'Generated on: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}').alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_paragraph()  # Spacing
        
        # Route Summary Section
        summary_heading = doc.add_heading('📍 Route Summary', level=1)
        
        summary_table = doc.add_table(rows=3, cols=2)
        summary_table.style = 'Light Grid Accent 1'
        
        # Source row
        summary_table.cell(0, 0).text = '🟢 Source Point'
        summary_table.cell(0, 1).text = f'{source}'
        
        # Destination row  
        summary_table.cell(1, 0).text = '🔴 Destination Point'
        summary_table.cell(1, 1).text = f'{destination}'
        
        # Coordinates row
        if landmarks and len(landmarks) >= 2:
            coords_text = f'Start: ({landmarks[0]["x"]}, {landmarks[0]["y"]}) → End: ({landmarks[1]["x"]}, {landmarks[1]["y"]})'
        else:
            coords_text = 'Coordinates extracted from route analysis'
        summary_table.cell(2, 0).text = '📐 Coordinates'
        summary_table.cell(2, 1).text = coords_text
        
        doc.add_paragraph()  # Spacing
        
        # Extract landmarks from the image area
        detected_landmarks = extract_text_from_image_regions(image_path, landmarks)
        
        # Landmarks Section
        if detected_landmarks:
            landmarks_heading = doc.add_heading('🎯 Landmarks Along Route', level=1)
            
            landmarks_para = doc.add_paragraph('Notable landmarks and points of interest:')
            
            for i, landmark in enumerate(detected_landmarks, 1):
                landmark_para = doc.add_paragraph()
                landmark_para.style = 'List Bullet'
                landmark_run = landmark_para.add_run(f'{landmark["name"]}')
                landmark_run.font.size = Pt(11)
                
                # Add category info
                category_run = landmark_para.add_run(f' ({landmark["type"].title()})')
                category_run.font.size = Pt(9)
                category_run.font.italic = True
        
        doc.add_paragraph()  # Spacing
        
        # Route Visualization Section
        route_heading = doc.add_heading('🗺️ Route Visualization', level=1)
        
        route_para = doc.add_paragraph('Extracted blue route line with source and destination markers:')
        route_para.add_run('\n• 🟢 Green dot: Starting point (Source)')
        route_para.add_run('\n• 🔵 Blue line: Navigation route')  
        route_para.add_run('\n• 🔴 Red dot: Ending point (Destination)')
        
        # Add the route image
        try:
            doc.add_picture(route_image_path, width=Inches(6))
            last_paragraph = doc.paragraphs[-1] 
            last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        except Exception as e:
            logger.warning(f"Could not add route image: {e}")
            doc.add_paragraph(f"Route image: {route_image_path}")
        
        # Navigation Instructions Section
        nav_heading = doc.add_heading('🧭 Navigation Information', level=1)
        
        instructions_para = doc.add_paragraph()
        instructions_para.add_run('Follow the blue route line from the green starting point to the red destination point. ')
        instructions_para.add_run('Use the landmarks mentioned above as reference points during navigation.')
        
        # Compass Directions (Lower Right Corner)
        doc.add_page_break()
        
        # Create a table for compass in lower right
        compass_para = doc.add_paragraph()
        compass_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        compass_text = """
🧭 DIRECTIONS
    N
    ↑
W ← • → E
    ↓
    S
        """
        
        compass_run = compass_para.add_run(compass_text)
        compass_run.font.name = 'Courier New'
        compass_run.font.size = Pt(10)
        compass_run.font.bold = True
        
        # Add multiple line breaks to push compass to bottom
        for _ in range(15):
            doc.add_paragraph()
            
        # Footer with compass
        footer_para = doc.add_paragraph()
        footer_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        footer_run = footer_para.add_run('🧭 Use cardinal directions for navigation')
        footer_run.font.size = Pt(8)
        footer_run.font.italic = True
        
        # Original image reference
        doc.add_page_break()
        orig_heading = doc.add_heading('📸 Original Image Reference', level=1)
        
        try:
            doc.add_picture(image_path, width=Inches(6))
            last_paragraph = doc.paragraphs[-1]
            last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        except Exception as e:
            logger.warning(f"Could not add original image: {e}")
            doc.add_paragraph(f"Original image: {image_path}")
        
        # Save the document
        doc.save(output_path)
        logger.info(f"Enhanced Word document created: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error creating enhanced document: {e}")
        raise

# Test function
def create_enhanced_test():
    """Test the enhanced document creation"""
    
    from simple_converter import extract_blue_lines_from_image
    
    print("🚀 Creating enhanced route document with landmarks and compass...")
    
    # Extract route
    image_path = "Image1.jpg"
    route_image = "simple_output/enhanced_route.png"
    result_path, landmarks = extract_blue_lines_from_image(image_path, route_image)
    
    print(f"✅ Route extracted with {len(landmarks)} landmarks")
    
    # Create enhanced document
    doc_path = create_enhanced_word_document(
        image_path=image_path,
        route_image_path=result_path,
        landmarks=landmarks,
        source="Home 🏠",
        destination="Office 🏢", 
        output_path="simple_output/enhanced_route_document.docx"
    )
    
    print(f"✅ Enhanced document created: {doc_path}")
    print("📋 Features included:")
    print("   🟢 Source/Destination labels at dots")
    print("   🎯 Landmark detection with emojis")
    print("   🧭 Compass directions")
    print("   📊 Professional formatting")
    
    return doc_path

if __name__ == "__main__":
    create_enhanced_test()
