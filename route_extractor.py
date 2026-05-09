"""
Map Route Extraction and Documentation System
Computer-vision pipeline for extracting blue routes from map images.
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime
import json
import logging
from typing import Dict, List, Tuple, Optional
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MapRouteExtractor:
    """Extract blue-line routes from map images using computer vision."""

    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self._setup_directories()

    def _load_config(self, config_path: str) -> Dict:
        defaults = {
            "blue_color_range": {
                "lower": [100, 80, 80],
                "upper": [130, 255, 255]
            },
            "output_dir": "output",
            "temp_dir":   "temp",
            "supported_formats": [".jpg", ".jpeg", ".png", ".bmp"],
        }
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    defaults.update(json.load(f))
            except Exception as e:
                logger.warning(f"Could not load config ({e}); using defaults.")
        return defaults

    def _setup_directories(self):
        for d in [self.config["output_dir"], self.config["temp_dir"]]:
            Path(d).mkdir(parents=True, exist_ok=True)

    # ── Core CV ───────────────────────────────────────────────────────────────

    def extract_blue_route(self, image_path: str) -> Tuple[np.ndarray, List[Tuple[int, int]]]:
        """
        Detect the blue route in a map image.

        Returns:
            mask         — binary mask of detected blue pixels
            route_points — ordered list of (x, y) pixel coordinates along the route
        """
        logger.info(f"Extracting blue route from {image_path}")
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Cannot load image: {image_path}")

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lo = np.array(self.config["blue_color_range"]["lower"])
        hi = np.array(self.config["blue_color_range"]["upper"])
        mask = cv2.inRange(hsv, lo, hi)

        # Morphological cleanup
        k    = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  k)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return mask, []

        # Prefer the longest contour (most likely the route, not a blue icon/label)
        best = max(contours, key=cv2.arcLength, closed=False)
        route_points = [tuple(pt[0]) for pt in best]
        return mask, route_points

    def detect_landmarks(self, image_path: str) -> List[Dict]:
        """
        Placeholder for landmark detection.

        A full implementation would use an OCR library (e.g. pytesseract) or a
        vision model to read text from the image.  Until that is wired up, this
        method returns an empty list so that no fabricated data reaches the
        generated document.
        """
        logger.info("Landmark detection: returning empty list (OCR not configured).")
        return []

    def calculate_direction(self, source_pos: Tuple[int, int],
                            dest_pos: Tuple[int, int]) -> str:
        """Return a cardinal/inter-cardinal direction label (image coords: y ↓)."""
        dx = dest_pos[0] - source_pos[0]
        dy = dest_pos[1] - source_pos[1]

        angle = np.degrees(np.arctan2(dy, dx))
        if angle < 0:
            angle += 360

        if   22.5  <= angle < 67.5:  return "South-East"
        elif 67.5  <= angle < 112.5: return "South"
        elif 112.5 <= angle < 157.5: return "South-West"
        elif 157.5 <= angle < 202.5: return "West"
        elif 202.5 <= angle < 247.5: return "North-West"
        elif 247.5 <= angle < 292.5: return "North"
        elif 292.5 <= angle < 337.5: return "North-East"
        else:                        return "East"

    def create_route_visualization(self, source: str, destination: str,
                                   landmarks: List[Dict], direction: str,
                                   output_path: str):
        """Render a simple top-to-bottom route diagram."""
        fig, ax = plt.subplots(figsize=(8, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')

        # Route arrow (top → bottom)
        route_arrow = patches.FancyArrowPatch(
            (5, 9), (5, 1),
            arrowstyle='->', mutation_scale=20,
            color='blue', linewidth=3
        )
        ax.add_patch(route_arrow)

        # Source at top (y=9), destination at bottom (y=1)
        ax.plot(5, 9, 'go', markersize=15, label='Starting Point')
        ax.plot(5, 1, 'ro', markersize=15, label='Destination')
        ax.text(5, 9.3, source,      ha='center', va='bottom', fontsize=12, fontweight='bold')
        ax.text(5, 0.7, destination, ha='center', va='top',    fontsize=12, fontweight='bold')

        # Spread up to 5 landmarks along the route
        if landmarks:
            ys = np.linspace(7.5, 2.5, min(len(landmarks), 5))
            for y, lm in zip(ys, landmarks[:5]):
                ax.plot(5, y, 'ys', markersize=10, alpha=0.8)
                ax.text(5.3, y, lm['name'], va='center', fontsize=9)

        # Direction label
        ax.text(5, 5, f"Direction: {direction}", ha='center', va='center',
                fontsize=13, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.4", facecolor="lightblue", alpha=0.7))

        ax.set_title(f'Route Map\n{source} → {destination}',
                     fontsize=15, fontweight='bold', pad=15)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(True, alpha=0.25)
        ax.legend(loc='upper right')

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        logger.info(f"Route visualization saved: {output_path}")

    def process_route(self, image_path: str, source: str, destination: str) -> Dict:
        """Full pipeline: extract → direction → visualize → return result dict."""
        logger.info(f"Processing route: {source} → {destination}")

        mask, route_points = self.extract_blue_route(image_path)
        landmarks          = self.detect_landmarks(image_path)

        if len(route_points) >= 2:
            direction = self.calculate_direction(route_points[0], route_points[-1])
        else:
            direction = "Unknown"

        viz_path = os.path.join(self.config["output_dir"],
                                f'route_viz_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
        self.create_route_visualization(source, destination, landmarks, direction, viz_path)

        return {
            "source":             source,
            "destination":        destination,
            "direction":          direction,
            "landmarks":          landmarks,
            "route_point_count":  len(route_points),
            "visualization_path": viz_path,
            "processed_at":       datetime.now().isoformat(),
        }


def main():
    extractor = MapRouteExtractor()
    print("Map Route Extraction System")
    print("=" * 35)
    source, destination = "Home", "NTR Garden"
    print(f"Generating sample visualization: {source} → {destination}")

    viz_path = os.path.join(extractor.config["output_dir"], "route_visualization.png")
    extractor.create_route_visualization(source, destination, [], "North-East", viz_path)
    print(f"Saved: {viz_path}")


if __name__ == "__main__":
    main()
