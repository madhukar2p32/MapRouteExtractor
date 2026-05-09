"""Runs a full end-to-end demo using Image1.jpg and prints the results."""
from simple_converter import (
    extract_blue_lines_with_labels,
    create_route_word_document,
    rotate_route_image_for_document,
)
import os

SOURCE      = "Home"
DESTINATION = "NTR Garden"

upload_path      = "Image1.jpg"
route_image_path = "simple_output/demo_route.png"
doc_path         = "simple_output/demo_RouteMap.docx"

print("=" * 55)
print("        MAP ROUTE EXTRACTOR  —  Demo Run")
print("=" * 55)

print("\nStep 1  Extract blue route from image")
route_image_path, landmarks = extract_blue_lines_with_labels(
    upload_path, route_image_path, SOURCE, DESTINATION
)
print("  Route image :", route_image_path)
print("  Landmarks   :", len(landmarks), "found")
for lm in landmarks:
    name = lm["name"]
    kind = lm["type"]
    x, y = lm["x"], lm["y"]
    print(f"    * {name!s:<20} ({kind})  pixel ({x}, {y})")

print("\nStep 2  Rotate image — source at TOP, destination at BOTTOM")
rotated = rotate_route_image_for_document(route_image_path, landmarks)
print("  Rotated image :", rotated)

print("\nStep 3  Generate Word document")
result = create_route_word_document(
    upload_path, route_image_path, landmarks, SOURCE, DESTINATION, doc_path
)
size = os.path.getsize(doc_path)
print("  Word document :", result)
print("  File size     :", f"{size:,} bytes")

print("\n" + "=" * 55)
print("WORD DOCUMENT CONTENTS OVERVIEW")
print("=" * 55)
print(f"  Heading       : Route Map")
print(f"  Subtitle      : {SOURCE}  ->  {DESTINATION}")
print(f"  Page 1 layout :")
print(f"    [green label]  {SOURCE}  (Starting Point - Top)")
print(f"    [route image - rotated so source is at top]")
print(f"    [red label]    {DESTINATION}  (Destination - Bottom)")
print(f"  Page 2        : Original source image")
print("=" * 55)
print("Demo complete.")
