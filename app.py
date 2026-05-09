"""
Flask Web Application for Map Route Extraction
Uploads map images, extracts blue routes, and generates Word documents.
"""

import os
import math
import logging
from datetime import datetime
from pathlib import Path

try:
    from flask import (Flask, render_template, request, jsonify,
                       send_file, flash, redirect, url_for)
    from werkzeug.utils import secure_filename
except ImportError:
    raise SystemExit("Flask is not installed. Run: pip install flask")

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
    from PIL import Image
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Flask setup
# ─────────────────────────────────────────────────────────────────────────────

app = Flask(__name__)
# Never hard-code a secret key. Use an environment variable; fall back to a
# per-process random value (sessions won't survive restarts, which is fine).
app.config['SECRET_KEY']          = os.environ.get('FLASK_SECRET_KEY', os.urandom(24).hex())
app.config['UPLOAD_FOLDER']       = 'uploads'
app.config['OUTPUT_FOLDER']       = 'output'
app.config['MAX_CONTENT_LENGTH']  = 16 * 1024 * 1024   # 16 MB

Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ─────────────────────────────────────────────────────────────────────────────
# Image processing
# ─────────────────────────────────────────────────────────────────────────────

def extract_blue_lines_with_labels(image_path, output_path,
                                   source_name="Source",
                                   destination_name="Destination"):
    """
    Detect the main blue route in a map image, annotate it with source /
    destination labels and a compass rose, and write the result to output_path.

    Returns (output_path, landmarks) where landmarks is a list of dicts
    with keys: name, type, x, y.
    """
    if not CV2_AVAILABLE:
        import shutil
        shutil.copy2(image_path, output_path)
        return output_path, []

    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Cannot load image: {image_path}")

        height, width = img.shape[:2]
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Google Maps route lines are vivid blue/indigo; high saturation
        # threshold (>= 120) excludes water bodies and faded map labels.
        lower_blue = np.array([100, 120, 80])
        upper_blue = np.array([135, 255, 255])
        blue_mask  = cv2.inRange(hsv, lower_blue, upper_blue)

        # Close tiny gaps (dashed segments) without distorting the shape
        kernel    = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernel, iterations=1)

        # ── Keep only the largest connected component (the main route) ──────────
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
            blue_mask, connectivity=8
        )

        route_mask = np.zeros_like(blue_mask)
        if num_labels > 1:
            largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
            route_mask[labels == largest_label] = 255

        # ── White canvas; paint route pixels directly — preserves exact shape ──
        result_img = np.ones((height, width, 3), dtype=np.uint8) * 255
        result_img[route_mask > 0] = [220, 50, 50]   # vivid blue (BGR)

        # ── Find endpoints ────────────────────────────────────────────────────
        landmarks = []
        ys, xs = np.where(route_mask > 0)

        if len(ys) > 0:
            # Topmost pixel  → destination (red pin at top in Google Maps)
            top_idx  = int(np.argmin(ys))
            dest_pt  = (int(xs[top_idx]), int(ys[top_idx]))

            # Bottommost pixel → source (starting circle at bottom in Google Maps)
            bot_idx  = int(np.argmax(ys))
            src_pt   = (int(xs[bot_idx]), int(ys[bot_idx]))

            for pt, colour, dark in [
                (src_pt,  (0, 200, 0), (0, 120, 0)),
                (dest_pt, (0, 0, 200), (0, 0, 120)),
            ]:
                cv2.circle(result_img, pt, 14, colour, -1)
                cv2.circle(result_img, pt, 16, (255, 255, 255), 2)
                cv2.circle(result_img, pt, 17, dark, 1)

            landmarks = [
                {'name': source_name,      'type': 'start',
                 'x': src_pt[0],  'y': src_pt[1]},
                {'name': destination_name, 'type': 'end',
                 'x': dest_pt[0], 'y': dest_pt[1]},
            ]

        # Compass rose (lower-right)
        cs, margin = 80, 20
        cx, cy = width - cs - margin, height - cs - margin
        centre = (cx + cs // 2, cy + cs // 2)
        cv2.circle(result_img, centre, cs // 2, (220, 220, 220), -1)
        cv2.circle(result_img, centre, cs // 2, (0, 0, 0), 2)
        for dx, dy, label, lx, ly in [
            ( 0, -1, 'N', -5, -(cs // 3) - 12),
            ( 1,  0, 'E',  cs // 3 + 5, 5),
            ( 0,  1, 'S', -5,  cs // 3 + 18),
            (-1,  0, 'W', -(cs // 3) - 20, 5),
        ]:
            tip = (centre[0] + dx * cs // 3, centre[1] + dy * cs // 3)
            cv2.arrowedLine(result_img, centre, tip, (0, 0, 0), 2, tipLength=0.3)
            cv2.putText(result_img, label,
                        (centre[0] + lx, centre[1] + ly),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        cv2.imwrite(output_path, result_img)
        return output_path, landmarks

    except Exception as e:
        logger.error(f"Route extraction failed: {e}")
        return image_path, []


def rotate_route_image_for_document(route_image_path, landmarks):
    """
    Rotate the extracted route image so the source (green dot) is at the TOP
    and the destination (red dot) is at the BOTTOM.

    PIL.Image.rotate(angle) is CCW-positive.
    The required rotation is:  PIL_angle = current_angle - 90°
    where current_angle = atan2(dest_y - src_y, dest_x - src_x).
    """
    if not CV2_AVAILABLE or not landmarks or len(landmarks) < 2:
        return route_image_path

    src = landmarks[0]
    dst = landmarks[1]
    dx  = dst['x'] - src['x']
    dy  = dst['y'] - src['y']

    current_angle = math.degrees(math.atan2(dy, dx))
    rotation      = current_angle - 90.0
    rotation      = ((rotation + 180) % 360) - 180   # normalise to (-180, 180]

    if abs(rotation) < 1:
        return route_image_path

    rotated_path = os.path.splitext(route_image_path)[0] + '_rotated.png'
    img = Image.open(route_image_path).convert('RGB')
    img = img.rotate(rotation, expand=True, fillcolor=(255, 255, 255))
    img.save(rotated_path)
    logger.info(f"Rotated route image by {rotation:.1f} deg")
    return rotated_path


def create_route_word_document(image_path, route_image_path, landmarks,
                               source, destination, output_path):
    """
    Build a Word document with:
      • Heading: "Route Map"
      • Route image with source label ABOVE and destination label BELOW
        (image is rotated so green dot is at top, red dot at bottom)
      • Original map on page 2
    """
    if not DOCX_AVAILABLE:
        return None

    doc = Document()

    for section in doc.sections:
        section.top_margin    = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin   = Inches(1.0)
        section.right_margin  = Inches(1.0)

    # ── Heading ───────────────────────────────────────────────────────────────
    heading = doc.add_heading('Route Map', level=0)
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # ── Subtitle ──────────────────────────────────────────────────────────────
    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = sub.add_run(f'{source}  →  {destination}')
    run.bold = True
    run.font.size = Pt(13)

    # ── Timestamp ─────────────────────────────────────────────────────────────
    ts = doc.add_paragraph(f'Generated: {datetime.now().strftime("%B %d, %Y  %I:%M %p")}')
    ts.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph()

    # ── Route details table ───────────────────────────────────────────────────
    doc.add_heading('Route Details', level=1)
    tbl = doc.add_table(rows=2, cols=2)
    tbl.style = 'Light Grid Accent 1'

    for row_idx, (label, value) in enumerate([
        ('🟢  Starting Point', source),
        ('🔴  Destination',    destination),
    ]):
        row = tbl.rows[row_idx]
        row.cells[0].text = label
        row.cells[1].text = value
        for cell in row.cells:
            for para in cell.paragraphs:
                for r in para.runs:
                    r.bold = True

    doc.add_paragraph()

    # ── Route visualization ───────────────────────────────────────────────────
    doc.add_heading('Route Visualization', level=1)

    # Source label above the image
    sp = doc.add_paragraph()
    sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sp_run = sp.add_run(f'🟢  {source}  (Starting Point — Top)')
    sp_run.bold = True
    sp_run.font.size = Pt(11)

    # Rotated route image (source at top, destination at bottom)
    rotated = rotate_route_image_for_document(route_image_path, landmarks)
    try:
        doc.add_picture(rotated, width=Inches(5.5))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    except Exception as e:
        logger.warning(f"Cannot embed route image: {e}")
        doc.add_paragraph(f'[Route image: {rotated}]').alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Destination label below the image
    dp = doc.add_paragraph()
    dp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    dp_run = dp.add_run(f'🔴  {destination}  (Destination — Bottom)')
    dp_run.bold = True
    dp_run.font.size = Pt(11)

    doc.add_paragraph()

    # ── Legend ────────────────────────────────────────────────────────────────
    doc.add_heading('Legend', level=1)
    for item in [
        '🟢  Green circle — Starting point',
        '🔵  Blue line — Route path',
        '🔴  Red circle — Destination',
        '🧭  Compass rose — In the lower-right corner of the route image',
    ]:
        doc.add_paragraph(item, style='List Bullet')

    doc.add_paragraph()

    # ── Navigation instructions ───────────────────────────────────────────────
    doc.add_heading('Navigation Instructions', level=1)
    for step in [
        f'Find the green circle at the TOP of the route image — your starting point: {source}.',
        'Follow the blue route line from top to bottom.',
        f'You have arrived when you reach the red circle at the BOTTOM: {destination}.',
        'Use the compass rose for cardinal direction orientation.',
    ]:
        p = doc.add_paragraph(style='List Number')
        p.add_run(step)

    doc.add_paragraph()

    # ── Disclaimer ────────────────────────────────────────────────────────────
    disc_run = doc.add_paragraph().add_run(
        'Disclaimer: This document is generated automatically from image analysis '
        'and is for reference only. Verify actual road conditions before travelling.'
    )
    disc_run.font.size = Pt(9)
    disc_run.italic    = True

    # ─────────────────────────────────────────────────────────────────────────
    # Page 2 — Original source image
    # ─────────────────────────────────────────────────────────────────────────
    doc.add_page_break()
    doc.add_heading('Original Source Image', level=1)
    doc.add_paragraph('Reference image used for route extraction:')

    try:
        doc.add_picture(image_path, width=Inches(6))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    except Exception as e:
        logger.warning(f"Cannot embed original image: {e}")
        doc.add_paragraph(f'Original image: {image_path}')

    doc.add_paragraph()
    info_para = doc.add_paragraph()
    for line in [
        f'Source file: {os.path.basename(image_path)}',
        f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
        'Generated by: Map Route Extractor',
    ]:
        r = info_para.add_run(line + '\n')
        r.font.size = Pt(9)
        r.italic    = True

    doc.save(output_path)
    logger.info(f"Word document saved: {output_path}")
    return output_path


# ─────────────────────────────────────────────────────────────────────────────
# Flask routes
# ─────────────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'map_image' not in request.files:
            flash('No file selected')
            return redirect(request.url)

        file        = request.files['map_image']
        source      = request.form.get('source', '').strip()
        destination = request.form.get('destination', '').strip()

        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        if not source or not destination:
            flash('Please provide both source and destination')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Invalid file type. Supported: PNG, JPG, JPEG, BMP, GIF')
            return redirect(request.url)

        if not DOCX_AVAILABLE:
            flash('python-docx is not installed. Cannot generate Word documents.')
            return redirect(request.url)

        if not CV2_AVAILABLE:
            flash('OpenCV / Pillow is not installed. Cannot process images.')
            return redirect(request.url)

        try:
            filename  = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base      = os.path.splitext(filename)[0]
            ext       = os.path.splitext(filename)[1]

            upload_path      = os.path.join(app.config['UPLOAD_FOLDER'],
                                            f'{base}_{timestamp}{ext}')
            route_image_path = os.path.join(app.config['OUTPUT_FOLDER'],
                                            f'route_{base}_{timestamp}.png')
            doc_path         = os.path.join(app.config['OUTPUT_FOLDER'],
                                            f'route_{base}_{timestamp}.docx')

            file.save(upload_path)
            logger.info(f"Processing route: {source} → {destination}")

            # Real image processing
            route_image_path, landmarks = extract_blue_lines_with_labels(
                upload_path, route_image_path, source, destination
            )

            # Generate Word document
            doc_result = create_route_word_document(
                upload_path, route_image_path, landmarks,
                source, destination, doc_path
            )

            if not doc_result:
                flash('Error generating Word document.')
                return redirect(request.url)

            route_data = {
                'source':      source,
                'destination': destination,
                'landmarks':   landmarks,
                'processed_at': datetime.now().isoformat(),
            }

            doc_filename = os.path.basename(doc_path)
            flash('Route processed successfully!')
            return render_template('result.html',
                                   route_data=route_data,
                                   doc_filename=doc_filename)

        except Exception as e:
            logger.error(f"Upload error: {e}")
            flash(f'Error processing route: {e}')
            return redirect(request.url)

    return render_template('upload.html')


@app.route('/download/<filename>')
def download_file(filename):
    """
    Serve files from the output folder only.
    Accepts a plain filename (no path separators) to prevent path traversal.
    """
    # Strip any directory component — only bare filenames are allowed
    safe_name = os.path.basename(filename)
    if safe_name != filename or not safe_name:
        return jsonify({'error': 'Invalid filename'}), 400

    output_dir = os.path.abspath(app.config['OUTPUT_FOLDER'])
    file_path  = os.path.join(output_dir, safe_name)

    if not os.path.exists(file_path):
        flash('File not found')
        return redirect(url_for('index'))

    return send_file(file_path, as_attachment=True)


@app.route('/api/process_route', methods=['POST'])
def api_process_route():
    """JSON API — returns route info (does not generate a document)."""
    try:
        data = request.get_json()
        if not data or 'source' not in data or 'destination' not in data:
            return jsonify({'error': 'Missing source or destination'}), 400

        return jsonify({
            'success': True,
            'message': 'Submit via /upload to get a Word document.',
            'source':      data['source'],
            'destination': data['destination'],
        })

    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health_check():
    return jsonify({
        'status':    'healthy',
        'timestamp': datetime.now().isoformat(),
        'service':   'Map Route Extractor',
        'cv2':       CV2_AVAILABLE,
        'docx':      DOCX_AVAILABLE,
    })


if __name__ == '__main__':
    print("Map Route Extractor — Web Application")
    print("=" * 40)
    print("Access at:     http://localhost:5000")
    print("Health check:  http://localhost:5000/health")
    print("Press Ctrl+C to stop")
    app.run(debug=True, host='0.0.0.0', port=5000)
