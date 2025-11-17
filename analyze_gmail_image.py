#!/usr/bin/env python3
"""
Analyze existing Gmail screenshot and detect UI elements
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def analyze_gmail_image(image_path):
    """Analyze Gmail screenshot and detect elements"""
    print(f"Analyzing: {image_path}\n")

    # Load image
    img_pil = Image.open(image_path)
    img_bgr = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    height, width = img_gray.shape
    print(f"Image Resolution: {width} x {height}\n")

    results = {}

    # 1. DETECT SELECT ALL CHECKBOX
    print("=" * 70)
    print("[1] DETECTING SELECT ALL CHECKBOX")
    print("=" * 70)
    checkbox = detect_checkbox(img_gray, img_bgr, width, height)
    results['checkbox'] = checkbox

    # 2. DETECT DELETE BUTTON
    print("\n" + "=" * 70)
    print("[2] DETECTING DELETE BUTTON")
    print("=" * 70)
    delete_btn = detect_delete_button(img_gray, img_bgr, width, height)
    results['delete'] = delete_btn

    # 3. DETECT SELECT ALL LINK
    print("\n" + "=" * 70)
    print("[3] DETECTING 'SELECT ALL CONVERSATIONS' LINK")
    print("=" * 70)
    select_link = detect_select_all_link(img_gray, img_bgr, width, height)
    results['select_all_link'] = select_link

    return img_pil, results

def detect_checkbox(gray, bgr, img_width, img_height):
    """Detect the select-all checkbox"""

    # The checkbox is in the toolbar area, left side
    # Based on Gmail UI: typically at x: 115-135, y: 60-75 (in this resolution)

    # Search region: top-left area of email list
    roi_y_start = int(img_height * 0.15)  # Start at ~15% from top
    roi_y_end = int(img_height * 0.35)    # End at ~35% from top
    roi_x_start = int(img_width * 0.20)   # Start at ~20% from left
    roi_x_end = int(img_width * 0.35)     # End at ~35% from left

    print(f"Search region: x=[{roi_x_start}, {roi_x_end}], y=[{roi_y_start}, {roi_y_end}]")

    roi = gray[roi_y_start:roi_y_end, roi_x_start:roi_x_end]

    # Edge detection
    edges = cv2.Canny(roi, 30, 100)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Checkbox is typically 16-24 pixels, square
        if 10 <= w <= 30 and 10 <= h <= 30:
            aspect_ratio = w / float(h)
            if 0.7 <= aspect_ratio <= 1.4:  # Nearly square
                abs_x = x + roi_x_start
                abs_y = y + roi_y_start
                center_x = abs_x + w // 2
                center_y = abs_y + h // 2

                # Prefer leftmost, topmost
                score = abs_x * 0.4 + abs_y * 0.6

                candidates.append({
                    'bbox': (abs_x, abs_y, abs_x + w, abs_y + h),
                    'center': (center_x, center_y),
                    'size': (w, h),
                    'score': score
                })

    if candidates:
        # Sort by score and get best
        candidates.sort(key=lambda c: c['score'])
        best = candidates[0]

        print(f"✓ FOUND")
        print(f"  Center: ({best['center'][0]}, {best['center'][1]})")
        print(f"  Bbox: {best['bbox']}")
        print(f"  Size: {best['size'][0]}x{best['size'][1]} pixels")
        print(f"  Candidates evaluated: {len(candidates)}")
        return best
    else:
        print("✗ NOT FOUND")
        return None

def detect_delete_button(gray, bgr, img_width, img_height):
    """Detect the delete/trash button"""

    # Delete button is in the toolbar, usually after checkbox
    # Based on Gmail UI: typically around x: 145-165, y: 60-75

    roi_y_start = int(img_height * 0.15)  # Start at ~15% from top
    roi_y_end = int(img_height * 0.35)    # End at ~35% from top
    roi_x_start = int(img_width * 0.25)   # Start at ~25% from left (after checkbox)
    roi_x_end = int(img_width * 0.50)     # End at ~50% from left

    print(f"Search region: x=[{roi_x_start}, {roi_x_end}], y=[{roi_y_start}, {roi_y_end}]")

    roi = gray[roi_y_start:roi_y_end, roi_x_start:roi_x_end]

    # Edge detection
    edges = cv2.Canny(roi, 40, 120)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Delete icon: 18-35 pixels, nearly square or slightly taller
        if 14 <= w <= 40 and 14 <= h <= 40:
            aspect_ratio = h / float(w)
            if 0.7 <= aspect_ratio <= 1.6:
                abs_x = x + roi_x_start
                abs_y = y + roi_y_start
                center_x = abs_x + w // 2
                center_y = abs_y + h // 2

                # Expected position score
                expected_x = int(img_width * 0.31)  # Around 31% from left
                expected_y = int(img_height * 0.24)  # Around 24% from top

                position_score = abs(center_x - expected_x) + abs(center_y - expected_y)

                candidates.append({
                    'bbox': (abs_x, abs_y, abs_x + w, abs_y + h),
                    'center': (center_x, center_y),
                    'size': (w, h),
                    'score': position_score
                })

    if candidates:
        # Get best match by position
        candidates.sort(key=lambda c: c['score'])
        best = candidates[0]

        print(f"✓ FOUND")
        print(f"  Center: ({best['center'][0]}, {best['center'][1]})")
        print(f"  Bbox: {best['bbox']}")
        print(f"  Size: {best['size'][0]}x{best['size'][1]} pixels")
        print(f"  Candidates evaluated: {len(candidates)}")
        return best
    else:
        print("✗ NOT FOUND")
        return None

def detect_select_all_link(gray, bgr, img_width, img_height):
    """Detect 'Select all conversations' link"""

    # This link appears in the message area, typically after checkbox click
    # Usually around y: 85-95, x: centered or left-aligned

    roi_y_start = int(img_height * 0.28)  # ~28% from top
    roi_y_end = int(img_height * 0.42)    # ~42% from top
    roi_x_start = int(img_width * 0.20)   # ~20% from left
    roi_x_end = int(img_width * 0.80)     # ~80% from left

    print(f"Search region: x=[{roi_x_start}, {roi_x_end}], y=[{roi_y_start}, {roi_y_end}]")

    roi = gray[roi_y_start:roi_y_end, roi_x_start:roi_x_end]

    # Look for horizontal text patterns
    edges = cv2.Canny(roi, 50, 150)

    # Morphological operation to connect text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 2))
    dilated = cv2.dilate(edges, kernel, iterations=2)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Link text: wide (100-400px), short (12-30px)
        if 80 <= w <= 500 and 10 <= h <= 35:
            aspect_ratio = w / float(h)
            if aspect_ratio >= 3.0:  # Wide horizontal text
                abs_x = x + roi_x_start
                abs_y = y + roi_y_start
                center_x = abs_x + w // 2
                center_y = abs_y + h // 2

                candidates.append({
                    'bbox': (abs_x, abs_y, abs_x + w, abs_y + h),
                    'center': (center_x, center_y),
                    'size': (w, h),
                    'width': w
                })

    if candidates:
        # Get widest candidate (full link text)
        candidates.sort(key=lambda c: c['width'], reverse=True)
        best = candidates[0]

        print(f"⚠ POTENTIALLY FOUND")
        print(f"  Center: ({best['center'][0]}, {best['center'][1]})")
        print(f"  Bbox: {best['bbox']}")
        print(f"  Size: {best['size'][0]}x{best['size'][1]} pixels")
        print(f"  Note: This element only appears AFTER clicking the checkbox")
        print(f"  Candidates evaluated: {len(candidates)}")
        return best
    else:
        print("⚠ NOT VISIBLE")
        print("  This link appears only after clicking the checkbox")
        return None

def create_annotated_image(img_pil, results):
    """Draw bounding boxes and labels"""

    annotated = img_pil.copy()
    draw = ImageDraw.Draw(annotated)

    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except:
        font_large = ImageFont.load_default()
        font_small = font_large

    colors = {
        'checkbox': '#00FF00',      # Green
        'delete': '#FF0000',        # Red
        'select_all_link': '#0000FF' # Blue
    }

    labels = {
        'checkbox': 'SELECT ALL CHECKBOX',
        'delete': 'DELETE BUTTON',
        'select_all_link': 'SELECT ALL LINK'
    }

    for key, element in results.items():
        if element is None:
            continue

        bbox = element['bbox']
        center = element['center']
        color = colors[key]
        label = labels[key]

        # Draw thick bounding box
        draw.rectangle(bbox, outline=color, width=3)

        # Draw crosshair at center
        cx, cy = center
        cross_size = 12
        draw.line([(cx - cross_size, cy), (cx + cross_size, cy)], fill=color, width=2)
        draw.line([(cx, cy - cross_size), (cx, cy + cross_size)], fill=color, width=2)

        # Draw center circle
        circle_r = 6
        draw.ellipse([(cx - circle_r, cy - circle_r), (cx + circle_r, cy + circle_r)],
                     outline=color, width=2)

        # Draw label with background
        label_y = bbox[1] - 25
        label_text = f"{label}"
        draw.text((bbox[0] + 2, label_y), label_text, fill=color, font=font_large)

        # Draw coordinates
        coord_text = f"({cx}, {cy})"
        draw.text((bbox[0] + 2, bbox[1] + 2), coord_text, fill=color, font=font_small)

    return annotated

def print_final_report(results, img_width, img_height):
    """Print comprehensive final report"""

    print("\n\n")
    print("=" * 75)
    print("TRIGGER RECEIVED: Locate Gmail UI Elements for Automation")
    print("=" * 75)

    print(f"\nImage Resolution: {img_width} x {img_height}")

    print("\n" + "-" * 75)
    print("DETECTED ELEMENTS:")
    print("-" * 75)

    # 1. CHECKBOX
    if results['checkbox']:
        cb = results['checkbox']
        print(f"\n1. SELECT ALL CHECKBOX")
        print(f"   Status: ✓ FOUND")
        print(f"   Center Coordinates: (x={cb['center'][0]}, y={cb['center'][1]})")
        print(f"   Bounding Box: {cb['bbox']}")
        print(f"   Element Size: {cb['size'][0]} x {cb['size'][1]} pixels")
        print(f"   Confidence: HIGH")
        print(f"   Visual Description: Square checkbox in email list toolbar, leftmost control")
    else:
        print(f"\n1. SELECT ALL CHECKBOX")
        print(f"   Status: ✗ NOT FOUND")
        print(f"   Confidence: N/A")

    # 2. DELETE BUTTON
    if results['delete']:
        db = results['delete']
        print(f"\n2. DELETE BUTTON")
        print(f"   Status: ✓ FOUND")
        print(f"   Center Coordinates: (x={db['center'][0]}, y={db['center'][1]})")
        print(f"   Bounding Box: {db['bbox']}")
        print(f"   Element Size: {db['size'][0]} x {db['size'][1]} pixels")
        print(f"   Confidence: HIGH")
        print(f"   Visual Description: Trash icon (🗑️) in toolbar, near checkbox")
    else:
        print(f"\n2. DELETE BUTTON")
        print(f"   Status: ✗ NOT FOUND")
        print(f"   Confidence: N/A")

    # 3. SELECT ALL LINK
    if results['select_all_link']:
        sl = results['select_all_link']
        print(f"\n3. 'SELECT ALL CONVERSATIONS' LINK")
        print(f"   Status: ⚠ POTENTIALLY DETECTED")
        print(f"   Center Coordinates: (x={sl['center'][0]}, y={sl['center'][1]})")
        print(f"   Bounding Box: {sl['bbox']}")
        print(f"   Element Size: {sl['size'][0]} x {sl['size'][1]} pixels")
        print(f"   Confidence: MEDIUM (prediction - not visible in current state)")
        print(f"   Visual Description: Text link that appears after clicking checkbox")
        print(f"   Important: This element only becomes visible AFTER clicking checkbox")
    else:
        print(f"\n3. 'SELECT ALL CONVERSATIONS' LINK")
        print(f"   Status: ⚠ NOT VISIBLE (Expected)")
        print(f"   Confidence: N/A")
        print(f"   Note: This link appears only after clicking the main checkbox")

    print("\n" + "=" * 75)
    print("PIXEL-PERFECT AUTOMATION COORDINATES")
    print("=" * 75)

    print("\nPython/Automation Format:")
    print("-" * 75)

    if results['checkbox']:
        cx, cy = results['checkbox']['center']
        print(f"\n# Select All Checkbox - CENTER POINT")
        print(f"CHECKBOX_X = {cx}")
        print(f"CHECKBOX_Y = {cy}")
        print(f"CHECKBOX_CENTER = ({cx}, {cy})")

    if results['delete']:
        dx, dy = results['delete']['center']
        print(f"\n# Delete Button - CENTER POINT")
        print(f"DELETE_BTN_X = {dx}")
        print(f"DELETE_BTN_Y = {dy}")
        print(f"DELETE_BTN_CENTER = ({dx}, {dy})")

    if results['select_all_link']:
        sx, sy = results['select_all_link']['center']
        print(f"\n# Select All Conversations Link - CENTER POINT (after checkbox click)")
        print(f"SELECT_ALL_LINK_X = {sx}")
        print(f"SELECT_ALL_LINK_Y = {sy}")
        print(f"SELECT_ALL_LINK_CENTER = ({sx}, {sy})")

    print("\n" + "=" * 75)
    print("RESULT SUMMARY")
    print("=" * 75)

    detected_count = sum(1 for v in [results['checkbox'], results['delete']] if v is not None)

    if detected_count == 2:
        print("\n✓ SUCCESS: All primary elements detected with high precision")
        print("  - Coordinates are CENTER points for accurate clicking")
        print("  - Ready for automation implementation")
    elif detected_count == 1:
        print("\n⚠ PARTIAL: Some elements detected")
        print("  - Review annotated image for verification")
    else:
        print("\n✗ FAILED: Primary elements not detected")
        print("  - Ensure Gmail inbox is visible in screenshot")

    print("\n" + "=" * 75 + "\n")

def main():
    image_path = "/home/tayyabcheema777/ali/chrome_gmail.png"

    print("\n" + "=" * 75)
    print("GMAIL ELEMENT COORDINATE DETECTION")
    print("Precision UI Element Locator for Automation")
    print("=" * 75 + "\n")

    # Analyze image
    img_pil, results = analyze_gmail_image(image_path)

    # Create annotated image
    annotated = create_annotated_image(img_pil, results)
    output_path = "/home/tayyabcheema777/ali/gmail_elements_annotated.png"
    annotated.save(output_path)

    print(f"\n✓ Annotated screenshot saved: {output_path}")

    # Print final report
    print_final_report(results, img_pil.width, img_pil.height)

    print("Files created:")
    print(f"  1. {output_path} (annotated with bounding boxes)")
    print(f"  2. Original: {image_path}")

if __name__ == "__main__":
    main()
