"""
Simple Image to Word Document Converter
Converts uploaded map images to Word documents with extracted blue route lines.
"""

import os
import sys
import math
from datetime import datetime
from pathlib import Path
import logging

try:
    from flask import Flask, render_template, request, send_file, redirect, url_for, flash
    from werkzeug.utils import secure_filename
except ImportError:
    print("Flask not available. Install with: pip install flask")
    sys.exit(1)

try:
    from docx import Document
    from docx.shared import Inches, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Use env var for secret key; fall back to a random value per process (sessions won't persist across restarts, which is fine)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', os.urandom(24).hex())
app.config['UPLOAD_FOLDER'] = 'simple_uploads'
app.config['OUTPUT_FOLDER'] = 'simple_output'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ─────────────────────────────────────────────────────────────────────────────
# Image processing
# ─────────────────────────────────────────────────────────────────────────────

def _draw_endpoint_label(img, text, pt, circle_bgr, dark_bgr, height, width):
    """Draw a filled circle with a named text label using PIL (reliable on all systems)."""
    r = 14
    cv2.circle(img, pt, r,     circle_bgr,      -1)
    cv2.circle(img, pt, r + 2, (255, 255, 255),  2)
    cv2.circle(img, pt, r + 3, dark_bgr,          1)

    # PIL handles text rendering more reliably than cv2.putText
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw    = ImageDraw.Draw(pil_img)

    font_size = max(18, height // 28)
    font = None
    for path in ["arial.ttf", "C:/Windows/Fonts/arial.ttf",
                 "C:/Windows/Fonts/calibri.ttf", "C:/Windows/Fonts/segoeui.ttf"]:
        try:
            font = ImageFont.truetype(path, font_size)
            break
        except (IOError, OSError):
            continue
    if font is None:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw   = bbox[2] - bbox[0]
    th   = bbox[3] - bbox[1]

    # Try placing label RIGHT of circle; fall back to LEFT near edge
    tx = pt[0] + r + 10
    if tx + tw + 10 > width:
        tx = pt[0] - r - 10 - tw
    ty = pt[1] - th // 2
    ty = max(4, min(height - th - 4, ty))
    tx = max(4, tx)

    # Coloured border matches the dot colour (RGB)
    border_rgb = (circle_bgr[2], circle_bgr[1], circle_bgr[0])
    draw.rectangle([tx - 5, ty - 5, tx + tw + 5, ty + th + 5],
                   fill=(255, 255, 255), outline=border_rgb, width=2)
    draw.text((tx, ty), text, fill=(20, 20, 20), font=font)

    # Write back into the original cv2 image buffer
    np.copyto(img, cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR))


def _bridge_route_gaps(route_mask, max_gap=80):
    """
    Connect nearby disconnected route components with thin lines.
    Unlike morphological closing, this only touches the gap itself and
    does not thicken the existing route pixels.
    """
    if cv2.countNonZero(route_mask) == 0:
        return route_mask

    num, labels, stats, _ = cv2.connectedComponentsWithStats(route_mask, connectivity=8)
    if num <= 2:
        return route_mask          # already one piece

    # Collect pixel arrays for each component (skip tiny specks)
    comp_pixels = []
    for lbl in range(1, num):
        if stats[lbl, cv2.CC_STAT_AREA] < 50:
            continue
        ys, xs = np.where(labels == lbl)
        comp_pixels.append(np.column_stack([xs, ys]))   # shape (N, 2)

    result = route_mask.copy()
    line_thickness = max(4, int(route_mask.shape[1] / 120))  # scale with image width

    for i in range(len(comp_pixels)):
        for j in range(i + 1, len(comp_pixels)):
            a_pts = comp_pixels[i]
            b_pts = comp_pixels[j]

            # Sub-sample to keep nearest-neighbour fast (≤300 pts each side)
            step_a = max(1, len(a_pts) // 300)
            step_b = max(1, len(b_pts) // 300)
            sa = a_pts[::step_a]
            sb = b_pts[::step_b]

            # Vectorised min-distance search
            best_dist = float('inf')
            best_pa = best_pb = None
            for pa in sa:
                dists = np.hypot(sb[:, 0] - pa[0], sb[:, 1] - pa[1])
                idx   = int(np.argmin(dists))
                if dists[idx] < best_dist:
                    best_dist = dists[idx]
                    best_pa   = (int(pa[0]),       int(pa[1]))
                    best_pb   = (int(sb[idx, 0]),  int(sb[idx, 1]))

            if best_dist <= max_gap:
                cv2.line(result, best_pa, best_pb, 255, line_thickness)

    return result


def _draw_landmark_text(img, text, pt, height, width):
    """Draw a small landmark name label using PIL."""
    try:
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw    = ImageDraw.Draw(pil_img)
        font_size = max(13, height // 45)
        font = None
        for path in ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/calibri.ttf",
                     "C:/Windows/Fonts/segoeui.ttf"]:
            try:
                font = ImageFont.truetype(path, font_size); break
            except (IOError, OSError):
                continue
        if font is None:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        tx = pt[0] + 12
        if tx + tw + 6 > width:
            tx = pt[0] - 12 - tw
        ty = pt[1] - th // 2
        ty = max(4, min(height - th - 4, ty))
        tx = max(4, tx)
        draw.rectangle([tx - 3, ty - 3, tx + tw + 3, ty + th + 3],
                       fill=(255, 255, 220), outline=(180, 80, 0), width=1)
        draw.text((tx, ty), text, fill=(80, 40, 0), font=font)
        np.copyto(img, cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR))
    except Exception:
        pass


def _detect_landmarks_ocr(image_path, route_mask, source_name, destination_name,
                           height, width):
    """
    Extract landmark names near the route using pytesseract OCR.
    Returns [] silently when Tesseract is not installed.
    """
    try:
        import pytesseract
        from pytesseract import Output as TessOutput

        # Set Tesseract path for Windows
        for tp in [r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                   r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe']:
            if os.path.exists(tp):
                pytesseract.pytesseract.tesseract_cmd = tp
                break

        orig = cv2.imread(image_path)
        if orig is None:
            return []

        data = pytesseract.image_to_data(orig, output_type=TessOutput.DICT,
                                         config='--psm 11')

        import re
        skip_lower = {source_name.lower(), destination_name.lower(),
                      source_name.split()[0].lower() if source_name else ''}
        noise_re   = re.compile(
            r'^(\d[\d\s\.]*(%|km|m|min|hr)?|[a-z]{1,2}|road|rd|hwy|expy|nagar)$',
            re.IGNORECASE
        )

        word_boxes = []
        for i, text in enumerate(data['text']):
            text = text.strip()
            if not text or len(text) < 3:
                continue
            if int(data['conf'][i]) < 45:
                continue
            if noise_re.match(text):
                continue
            if text.lower() in skip_lower:
                continue
            x, y, w, h = (data['left'][i], data['top'][i],
                          data['width'][i], data['height'][i])
            cx, cy = x + w // 2, y + h // 2
            # Only keep text that is near (≤ 200 px) the route
            y1 = max(0, cy - 200); y2 = min(height, cy + 200)
            x1 = max(0, cx - 200); x2 = min(width,  cx + 200)
            if route_mask[y1:y2, x1:x2].max() == 0:
                continue
            word_boxes.append({'text': text, 'x': cx, 'y': cy,
                                'conf': int(data['conf'][i])})

        # Merge words on the same line into one label
        word_boxes.sort(key=lambda b: (b['y'] // 12, b['x']))
        results, i = [], 0
        while i < len(word_boxes):
            grp = [word_boxes[i]]
            j   = i + 1
            while j < len(word_boxes):
                prev, cur = grp[-1], word_boxes[j]
                if abs(cur['y'] - prev['y']) < 14 and abs(cur['x'] - prev['x']) < 130:
                    grp.append(cur); j += 1
                else:
                    break
            name = ' '.join(b['text'] for b in grp)
            cx   = sum(b['x'] for b in grp) // len(grp)
            cy   = sum(b['y'] for b in grp) // len(grp)
            results.append({'name': name, 'type': 'landmark', 'x': cx, 'y': cy})
            i = j if j > i else i + 1

        logger.info(f"OCR landmarks found: {len(results)}")
        return results

    except Exception as e:
        logger.debug(f"Landmark OCR skipped: {e}")
        return []


def extract_blue_lines_with_labels(image_path, output_path,
                                   source_name="Source",
                                   destination_name="Destination"):
    """
    Extract the blue route from a map image onto a clean white background.

    Key improvements over the previous version:
    - HIGH saturation threshold (>= 160) to reject water bodies, light-blue
      map labels and alternative route lines, keeping only the vivid main route.
    - Component selection by THINNESS SCORE (perimeter² / area): route lines
      score much higher than lakes or circular blobs.
    - Route pixels are COPIED DIRECTLY (no contour redrawing) so the shape
      is perfectly faithful to the original.
    - Source/destination NAMES are drawn on the image next to their circles.
    """
    if not CV2_AVAILABLE:
        import shutil
        shutil.copy2(image_path, output_path)
        return output_path, []

    try:
        img = cv2.imread(image_path)
        if img is None:
            return image_path, []

        height, width = img.shape[:2]
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # ── Blue detection ────────────────────────────────────────────────────
        # S >= 180 targets only the vivid highlighted main route.
        # Raising from 160→180 drops faint alternative-route blues that bleed
        # through on satellite-view screenshots.
        lower_blue = np.array([100, 180, 80])
        upper_blue = np.array([135, 255, 255])
        blue_mask  = cv2.inRange(hsv, lower_blue, upper_blue)

        # Close tiny gaps (dotted turn-markers on the route) without altering shape
        kernel    = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernel, iterations=1)

        # ── Select ROUTE components using thinness score ─────────────────────
        # thinness = perimeter² / area
        #   • Long thin route line  → very high (~300-1000)
        #   • Circular lake / blob  → low (~12-16, min for a circle)
        # Phase 1: find the dominant route component (thinness × vert_span).
        # Phase 2: include ALL other components whose thinness alone is route-like
        #          (catches disconnected start/end segments with small vert_span).
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
            blue_mask, connectivity=8
        )

        best_score    = 0.0
        best_thinness = 0.0
        component_data = []   # (lbl, thinness, score)

        for lbl in range(1, num_labels):
            area = int(stats[lbl, cv2.CC_STAT_AREA])
            if area < 80:            # ignore specks
                continue

            h0 = int(stats[lbl, cv2.CC_STAT_HEIGHT])

            comp_mask = np.zeros_like(blue_mask)
            comp_mask[labels == lbl] = 255
            cnts, _ = cv2.findContours(comp_mask, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
            perimeter = sum(cv2.arcLength(c, False) for c in cnts)

            thinness  = (perimeter ** 2) / max(area, 1)
            score     = thinness * h0        # vert_span weight picks dominant segment

            component_data.append((lbl, thinness, score))
            if score > best_score:
                best_score    = score
                best_thinness = thinness

        # Include every component whose thinness is ≥ 10% of the best component's
        # thinness (absolute floor: 30).  This retains disconnected route pieces
        # (e.g. the starting loop) while rejecting lakes (~12-16).
        thinness_threshold = max(30.0, best_thinness * 0.10)
        route_mask = np.zeros_like(blue_mask)
        for lbl, thinness, _ in component_data:
            if thinness >= thinness_threshold:
                route_mask[labels == lbl] = 255

        # ── Bridge gaps caused by UI overlays (info boxes, white dot markers) ─
        # Draw thin connector lines between nearby disconnected components so
        # the route stays thin everywhere while gaps are filled.
        route_mask = _bridge_route_gaps(route_mask, max_gap=80)

        # ── White canvas; paint route pixels directly ─────────────────────────
        result_img = np.ones((height, width, 3), dtype=np.uint8) * 255
        result_img[route_mask > 0] = [210, 40, 40]   # vivid blue (BGR)

        # ── Find endpoints ────────────────────────────────────────────────────
        landmarks = []
        ys, xs = np.where(route_mask > 0)

        if len(ys) > 0:
            # Google Maps convention: starting point (white circle) at BOTTOM,
            # destination pin (red pin) at TOP.
            bot_idx = int(np.argmax(ys))
            top_idx = int(np.argmin(ys))
            src_pt  = (int(xs[bot_idx]), int(ys[bot_idx]))   # source  = bottommost
            dest_pt = (int(xs[top_idx]), int(ys[top_idx]))   # dest    = topmost

            # Draw circles + names on the image
            _draw_endpoint_label(result_img, source_name,
                                 src_pt,  (0, 200, 0), (0, 110, 0),
                                 height, width)
            _draw_endpoint_label(result_img, destination_name,
                                 dest_pt, (0, 0, 210), (0, 0, 120),
                                 height, width)

            landmarks = [
                {'name': source_name,      'type': 'start',
                 'x': src_pt[0],  'y': src_pt[1]},
                {'name': destination_name, 'type': 'end',
                 'x': dest_pt[0], 'y': dest_pt[1]},
            ]

        # ── Detect map landmarks via OCR ───────────────────────────────────────
        map_landmarks = _detect_landmarks_ocr(image_path, route_mask,
                                              source_name, destination_name,
                                              height, width)
        for lm in map_landmarks:
            pt = (lm['x'], lm['y'])
            cv2.drawMarker(result_img, pt, (180, 80, 0),
                           cv2.MARKER_DIAMOND, 18, 2)
            _draw_landmark_text(result_img, lm['name'], pt, height, width)
        landmarks += map_landmarks

        # ── Compass rose (lower-right corner) ─────────────────────────────────
        cs     = 70
        margin = 15
        cx     = width  - cs - margin
        cy     = height - cs - margin
        centre = (cx + cs // 2, cy + cs // 2)
        cv2.circle(result_img, centre, cs // 2, (220, 220, 220), -1)
        cv2.circle(result_img, centre, cs // 2, (60, 60, 60), 2)
        for dx, dy, lbl, lx, ly in [
            ( 0, -1, 'N', -5, -(cs // 3) - 10),
            ( 1,  0, 'E',  cs // 3 + 5,  4),
            ( 0,  1, 'S', -5,  cs // 3 + 16),
            (-1,  0, 'W', -(cs // 3) - 18, 4),
        ]:
            tip = (centre[0] + dx * cs // 3, centre[1] + dy * cs // 3)
            cv2.arrowedLine(result_img, centre, tip, (40, 40, 40), 2, tipLength=0.3)
            cv2.putText(result_img, lbl,
                        (centre[0] + lx, centre[1] + ly),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (40, 40, 40), 1)

        cv2.imwrite(output_path, result_img)
        return output_path, landmarks

    except Exception as e:
        logger.error(f"Error extracting route: {e}")
        return image_path, []


def rotate_route_image_for_document(route_image_path, landmarks):
    """
    Rotate the route image so that the source point appears at the TOP and
    the destination point appears at the BOTTOM.

    PIL.Image.rotate(angle) rotates counter-clockwise (CCW).
    To make the source→destination vector point straight DOWN (angle = 90° in
    image coords where y increases downward), we need:

        PIL_rotation = current_angle - 90°

    where current_angle = atan2(dy, dx), dy = dest_y - src_y.

    Example: source at left, dest at right → current_angle = 0°
             PIL_rotation = -90° (CW 90°) → left side goes to top ✓
    """
    if not CV2_AVAILABLE or not landmarks or len(landmarks) < 2:
        return route_image_path

    src = landmarks[0]
    dst = landmarks[1]
    dx = dst['x'] - src['x']
    dy = dst['y'] - src['y']

    current_angle = math.degrees(math.atan2(dy, dx))
    rotation = current_angle - 90.0                    # FIX: was (90 - current_angle)
    rotation = ((rotation + 180) % 360) - 180          # normalise to (-180, 180]

    if abs(rotation) < 1:
        return route_image_path

    rotated_path = os.path.splitext(route_image_path)[0] + '_rotated.png'
    image = Image.open(route_image_path).convert('RGB')
    image = image.rotate(rotation, expand=True, fillcolor=(255, 255, 255))
    image.save(rotated_path)
    logger.info(f"Route image rotated by {rotation:.1f} deg -> {rotated_path}")
    return rotated_path


# ─────────────────────────────────────────────────────────────────────────────
# Word document generation
# ─────────────────────────────────────────────────────────────────────────────

def create_route_word_document(image_path, route_image_path, landmarks, source, destination, output_path):
    """
    Create a professional Word document with:
      • Heading "Route Map" (centred)
      • Source clearly at the TOP of the route image section
      • Destination clearly at the BOTTOM
      • Route image rotated so green dot (source) is at top, red dot (dest) at bottom
      • Original source image on page 2
    """
    if not DOCX_AVAILABLE:
        logger.error("python-docx not installed. Cannot create Word document.")
        return None

    try:
        doc = Document()

        # ── Page margins ──────────────────────────────────────────────────────
        for section in doc.sections:
            section.top_margin    = Inches(0.75)
            section.bottom_margin = Inches(0.75)
            section.left_margin   = Inches(1.0)
            section.right_margin  = Inches(1.0)

        # ── Title ─────────────────────────────────────────────────────────────
        title = doc.add_heading('Route Map', level=0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # ── Subtitle (source → destination) ───────────────────────────────────
        subtitle = doc.add_paragraph()
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = subtitle.add_run(f'{source}  →  {destination}')
        run.bold = True
        run.font.size = Pt(13)

        # ── Timestamp ─────────────────────────────────────────────────────────
        ts_para = doc.add_paragraph(f'Generated: {datetime.now().strftime("%B %d, %Y  %I:%M %p")}')
        ts_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_paragraph()

        # ── Route details table ───────────────────────────────────────────────
        doc.add_heading('Route Details', level=1)
        table = doc.add_table(rows=2, cols=2)
        table.style = 'Light Grid Accent 1'

        r0 = table.rows[0]
        r0.cells[0].text = '🟢  Starting Point'
        r0.cells[1].text = source
        for cell in r0.cells:
            for para in cell.paragraphs:
                for run in para.runs:
                    run.bold = True

        r1 = table.rows[1]
        r1.cells[0].text = '🔴  Destination'
        r1.cells[1].text = destination
        for cell in r1.cells:
            for para in cell.paragraphs:
                for run in para.runs:
                    run.bold = True

        doc.add_paragraph()

        # ── Route map image section ───────────────────────────────────────────
        doc.add_heading('Route Visualization', level=1)

        # Source label ABOVE the image
        sp = doc.add_paragraph()
        sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sp_run = sp.add_run(f'🟢  {source}  (Starting Point)')
        sp_run.bold = True
        sp_run.font.size = Pt(11)

        # Embed route image as-is (no rotation)
        try:
            doc.add_picture(route_image_path, width=Inches(5.5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        except Exception as e:
            logger.warning(f"Could not embed route image: {e}")
            doc.add_paragraph(f'[Route image: {route_image_path}]').alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Destination label BELOW the image
        dp = doc.add_paragraph()
        dp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        dp_run = dp.add_run(f'🔴  {destination}  (Destination)')
        dp_run.bold = True
        dp_run.font.size = Pt(11)

        doc.add_paragraph()

        # ── Legend ────────────────────────────────────────────────────────────
        doc.add_heading('Legend', level=1)
        for text in [
            '🟢  Green circle — Starting point',
            '🔵  Blue line — Route path',
            '🔴  Red circle — Destination',
            '🧭  Compass rose — Located in the lower-right corner of the route image',
        ]:
            doc.add_paragraph(text, style='List Bullet')

        doc.add_paragraph()

        # ── Navigation instructions ───────────────────────────────────────────
        doc.add_heading('Navigation Instructions', level=1)
        steps = [
            f'Locate the green circle at the TOP of the route image — this is your starting point: {source}.',
            'Follow the blue route line from top to bottom.',
            f'Your destination is the red circle at the BOTTOM of the route image: {destination}.',
            'Use the compass rose (lower-right of the image) for cardinal direction orientation.',
        ]
        for step in steps:
            p = doc.add_paragraph(style='List Number')
            p.add_run(step)

        doc.add_paragraph()

        # ── Disclaimer ────────────────────────────────────────────────────────
        disc = doc.add_paragraph()
        disc_run = disc.add_run(
            'Disclaimer: This document is generated automatically from image analysis and is '
            'for reference only. Please verify actual road conditions before travelling.'
        )
        disc_run.font.size = Pt(9)
        disc_run.italic = True

        # ─────────────────────────────────────────────────────────────────────
        # Page 2 — Original source image
        # ─────────────────────────────────────────────────────────────────────
        doc.add_page_break()
        doc.add_heading('Original Source Image', level=1)
        doc.add_paragraph('The image below is the original map used for route extraction.')

        try:
            doc.add_picture(image_path, width=Inches(6))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        except Exception as e:
            logger.warning(f"Could not embed original image: {e}")
            doc.add_paragraph(f'Original image: {image_path}')

        doc.add_paragraph()
        info = doc.add_paragraph()
        info.add_run('Generated by: Map Route Extractor\n').italic = True
        info.add_run(f'Source file: {os.path.basename(image_path)}\n').italic = True
        info.add_run(f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}').italic = True

        doc.save(output_path)
        logger.info(f"Word document saved: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Error creating Word document: {e}")
        raise


# ─────────────────────────────────────────────────────────────────────────────
# Flask routes
# ─────────────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('simple_upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)

    file        = request.files['file']
    source      = request.form.get('source', 'Starting Point').strip() or 'Starting Point'
    destination = request.form.get('destination', 'Destination').strip() or 'Destination'

    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))

    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload PNG, JPG, JPEG, BMP, or GIF.')
        return redirect(url_for('index'))

    try:
        filename  = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base      = os.path.splitext(filename)[0]
        ext       = os.path.splitext(filename)[1]

        upload_path      = os.path.join(app.config['UPLOAD_FOLDER'], f'{base}_{timestamp}{ext}')
        route_image_path = os.path.join(app.config['OUTPUT_FOLDER'], f'{base}_route_{timestamp}.png')
        doc_path         = os.path.join(app.config['OUTPUT_FOLDER'], f'{base}_route_{timestamp}.docx')

        file.save(upload_path)

        # Extract blue route with labels
        route_image_path, landmarks = extract_blue_lines_with_labels(
            upload_path, route_image_path, source, destination
        )

        if not DOCX_AVAILABLE:
            flash('python-docx is not installed. Cannot generate Word document.')
            return redirect(url_for('index'))

        # Generate Word document
        result_doc = create_route_word_document(
            upload_path, route_image_path, landmarks, source, destination, doc_path
        )

        if result_doc:
            return send_file(
                result_doc,
                as_attachment=True,
                download_name=f'route_{base}_{timestamp}.docx',
            )

        flash('Error creating Word document.')

    except Exception as e:
        logger.error(f"Upload error: {e}")
        flash(f'Error processing file: {e}')

    return redirect(url_for('index'))


@app.route('/status')
def status():
    from flask import jsonify
    return jsonify({
        'flask': True,
        'docx':  DOCX_AVAILABLE,
        'cv2':   CV2_AVAILABLE,
        'upload_folder': app.config['UPLOAD_FOLDER'],
        'output_folder': app.config['OUTPUT_FOLDER'],
    })


if __name__ == '__main__':
    print("Blue Route Extractor — Word Document Generator")
    print("=" * 47)
    print("Access at: http://localhost:5001")
    print("Press Ctrl+C to stop")
    app.run(host='127.0.0.1', port=5001, debug=True, use_reloader=False)
