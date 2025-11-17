#!/usr/bin/env python3
"""
Gmail Element Detection Script
Captures screenshot and detects precise coordinates of UI elements
"""

import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab, Image, ImageDraw, ImageFont
import sys

def capture_screenshot():
    """Capture the current screen"""
    print("Capturing screenshot...")
    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)
    # Convert RGB to BGR for OpenCV
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    return screenshot, screenshot_bgr

def find_checkbox_by_template(image_bgr):
    """Find the select-all checkbox using template matching and shape detection"""
    print("\nSearching for Select All Checkbox...")

    # Convert to grayscale
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # Look for checkbox-like squares in the top-left region
    # Gmail checkbox is typically in top 200 pixels, left 300 pixels
    roi_y_start, roi_y_end = 0, 300
    roi_x_start, roi_x_end = 0, 400

    roi = gray[roi_y_start:roi_y_end, roi_x_start:roi_x_end]

    # Apply edge detection
    edges = cv2.Canny(roi, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    checkbox_candidates = []

    for contour in contours:
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)

        # Checkbox should be roughly square, size typically 16-24 pixels
        if 12 <= w <= 30 and 12 <= h <= 30:
            aspect_ratio = w / float(h)
            if 0.8 <= aspect_ratio <= 1.2:  # Nearly square
                # Adjust coordinates back to full image
                abs_x = x + roi_x_start
                abs_y = y + roi_y_start
                center_x = abs_x + w // 2
                center_y = abs_y + h // 2

                checkbox_candidates.append({
                    'bbox': (abs_x, abs_y, abs_x + w, abs_y + h),
                    'center': (center_x, center_y),
                    'size': (w, h)
                })

    # Return the topmost, leftmost checkbox (typically the select-all)
    if checkbox_candidates:
        # Sort by y-coordinate first, then x-coordinate
        checkbox_candidates.sort(key=lambda c: (c['center'][1], c['center'][0]))
        return checkbox_candidates[0]

    return None

def find_delete_button(image_bgr, screenshot_pil):
    """Find the delete/trash button using OCR and icon detection"""
    print("\nSearching for Delete Button...")

    # Convert to grayscale
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # Search in the top toolbar area (typically top 200 pixels)
    roi_y_start, roi_y_end = 0, 250
    roi = gray[roi_y_start:roi_y_end, :]

    # Apply edge detection to find button-like shapes
    edges = cv2.Canny(roi, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Also use OCR to find text near delete icons
    roi_pil = screenshot_pil.crop((0, roi_y_start, screenshot_pil.width, roi_y_end))
    ocr_data = pytesseract.image_to_data(roi_pil, output_type=pytesseract.Output.DICT)

    delete_candidates = []

    # Look for "Delete" or trash icon areas
    for i, text in enumerate(ocr_data['text']):
        if text.lower() in ['delete', 'trash', 'remove']:
            x, y, w, h = (ocr_data['left'][i], ocr_data['top'][i],
                         ocr_data['width'][i], ocr_data['height'][i])

            # Adjust for ROI offset
            abs_y = y + roi_y_start
            center_x = x + w // 2
            center_y = abs_y + h // 2

            delete_candidates.append({
                'bbox': (x, abs_y, x + w, abs_y + h),
                'center': (center_x, center_y),
                'method': 'OCR',
                'text': text
            })

    # Look for trash icon shapes (vertical rectangles in toolbar)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Trash icon is typically 20-40 pixels wide, similar height
        if 15 <= w <= 50 and 15 <= h <= 50:
            abs_y = y + roi_y_start
            center_x = x + w // 2
            center_y = abs_y + h // 2

            # Skip if too far left (likely checkbox area)
            if center_x < 200:
                continue

            delete_candidates.append({
                'bbox': (x, abs_y, x + w, abs_y + h),
                'center': (center_x, center_y),
                'method': 'shape',
                'size': (w, h)
            })

    if delete_candidates:
        # Prefer OCR results, otherwise use shape detection
        ocr_results = [c for c in delete_candidates if c.get('method') == 'OCR']
        if ocr_results:
            return ocr_results[0]
        else:
            # Return shape closest to expected position (around x=150-300, y=100-180)
            delete_candidates.sort(key=lambda c: abs(c['center'][0] - 200) + abs(c['center'][1] - 140))
            return delete_candidates[0]

    return None

def find_select_all_link(screenshot_pil):
    """Find 'Select all conversations' link using OCR"""
    print("\nSearching for 'Select all conversations' link...")

    # This link appears in the middle-top area after clicking checkbox
    # Search in top 400 pixels
    roi = screenshot_pil.crop((0, 0, screenshot_pil.width, 400))

    # Use OCR to find the text
    ocr_data = pytesseract.image_to_data(roi, output_type=pytesseract.Output.DICT)

    # Look for variations of "select all" text
    for i in range(len(ocr_data['text'])):
        text = ocr_data['text'][i].lower()

        if 'select' in text or 'all' in text or 'conversation' in text:
            # Check nearby words to confirm it's the right link
            context = ' '.join([ocr_data['text'][j].lower() for j in range(max(0, i-2), min(len(ocr_data['text']), i+5))])

            if 'select all' in context or 'all conversation' in context:
                x, y, w, h = (ocr_data['left'][i], ocr_data['top'][i],
                             ocr_data['width'][i], ocr_data['height'][i])

                center_x = x + w // 2
                center_y = y + h // 2

                return {
                    'bbox': (x, y, x + w, y + h),
                    'center': (center_x, center_y),
                    'text': context
                }

    print("  ⚠ 'Select all conversations' link not found (may not be visible yet)")
    return None

def draw_annotations(screenshot_pil, elements):
    """Draw bounding boxes and labels on screenshot"""
    print("\nCreating annotated screenshot...")

    annotated = screenshot_pil.copy()
    draw = ImageDraw.Draw(annotated)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except:
        font = ImageFont.load_default()

    colors = {
        'checkbox': '#00FF00',  # Green
        'delete': '#FF0000',    # Red
        'select_all_link': '#0000FF'  # Blue
    }

    for name, element in elements.items():
        if element is None:
            continue

        bbox = element['bbox']
        center = element['center']
        color = colors.get(name, '#FFFF00')

        # Draw bounding box
        draw.rectangle(bbox, outline=color, width=3)

        # Draw center point
        cross_size = 10
        cx, cy = center
        draw.line([(cx - cross_size, cy), (cx + cross_size, cy)], fill=color, width=2)
        draw.line([(cx, cy - cross_size), (cx, cy + cross_size)], fill=color, width=2)
        draw.ellipse([(cx - 5, cy - 5), (cx + 5, cy + 5)], outline=color, width=2)

        # Draw label
        label = name.replace('_', ' ').title()
        label_pos = (bbox[0], bbox[1] - 25)
        draw.text(label_pos, label, fill=color, font=font)

    return annotated

def main():
    print("=" * 70)
    print("Gmail Element Detection - Precise Coordinate Finder")
    print("=" * 70)

    # Capture screenshot
    screenshot_pil, screenshot_bgr = capture_screenshot()
    screenshot_pil.save('/home/tayyabcheema777/ali/gmail_current_screenshot.png')
    print(f"✓ Screenshot saved: gmail_current_screenshot.png")
    print(f"  Resolution: {screenshot_pil.width} x {screenshot_pil.height}")

    # Detect elements
    elements = {}

    # 1. Find Select All Checkbox
    checkbox = find_checkbox_by_template(screenshot_bgr)
    elements['checkbox'] = checkbox

    # 2. Find Delete Button
    delete_btn = find_delete_button(screenshot_bgr, screenshot_pil)
    elements['delete'] = delete_btn

    # 3. Find Select All Link
    select_all_link = find_select_all_link(screenshot_pil)
    elements['select_all_link'] = select_all_link

    # Create annotated screenshot
    annotated = draw_annotations(screenshot_pil, elements)
    annotated.save('/home/tayyabcheema777/ali/gmail_annotated.png')
    print(f"✓ Annotated screenshot saved: gmail_annotated.png")

    # Print results
    print("\n" + "=" * 70)
    print("DETECTION RESULTS")
    print("=" * 70)

    if checkbox:
        print("\n✓ SELECT ALL CHECKBOX FOUND:")
        print(f"  Center Coordinates: ({checkbox['center'][0]}, {checkbox['center'][1]})")
        print(f"  Bounding Box: {checkbox['bbox']}")
        print(f"  Size: {checkbox['size']} pixels")
        print(f"  Confidence: HIGH")
    else:
        print("\n✗ SELECT ALL CHECKBOX: NOT FOUND")

    if delete_btn:
        print("\n✓ DELETE BUTTON FOUND:")
        print(f"  Center Coordinates: ({delete_btn['center'][0]}, {delete_btn['center'][1]})")
        print(f"  Bounding Box: {delete_btn['bbox']}")
        print(f"  Detection Method: {delete_btn.get('method', 'unknown')}")
        print(f"  Confidence: MEDIUM-HIGH")
    else:
        print("\n✗ DELETE BUTTON: NOT FOUND")

    if select_all_link:
        print("\n✓ 'SELECT ALL CONVERSATIONS' LINK FOUND:")
        print(f"  Center Coordinates: ({select_all_link['center'][0]}, {select_all_link['center'][1]})")
        print(f"  Bounding Box: {select_all_link['bbox']}")
        print(f"  Detected Text: {select_all_link.get('text', 'N/A')}")
        print(f"  Confidence: MEDIUM")
    else:
        print("\n⚠ 'SELECT ALL CONVERSATIONS' LINK: NOT VISIBLE")
        print("  (This link only appears after clicking the main checkbox)")

    print("\n" + "=" * 70)
    print("AUTOMATION-READY COORDINATES")
    print("=" * 70)

    if checkbox:
        print(f"\nCHECKBOX_CENTER = ({checkbox['center'][0]}, {checkbox['center'][1]})")
    if delete_btn:
        print(f"DELETE_BTN_CENTER = ({delete_btn['center'][0]}, {delete_btn['center'][1]})")
    if select_all_link:
        print(f"SELECT_ALL_LINK_CENTER = ({select_all_link['center'][0]}, {select_all_link['center'][1]})")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
