#!/usr/bin/env python3
"""
Gmail Element Detection for WSL/Windows
Captures Windows screen and detects Gmail UI elements
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess
import os

def capture_windows_screenshot():
    """Capture screenshot from Windows using PowerShell"""
    print("Capturing Windows screenshot via PowerShell...")

    screenshot_path = "/home/tayyabcheema777/ali/gmail_current_screenshot.png"

    # PowerShell command to capture screenshot
    ps_command = """
Add-Type -AssemblyName System.Windows.Forms,System.Drawing
$screens = [Windows.Forms.Screen]::AllScreens
$top = ($screens.Bounds.Top | Measure-Object -Minimum).Minimum
$left = ($screens.Bounds.Left | Measure-Object -Minimum).Minimum
$width = ($screens.Bounds.Right | Measure-Object -Maximum).Maximum
$height = ($screens.Bounds.Bottom | Measure-Object -Maximum).Maximum
$bounds = [Drawing.Rectangle]::FromLTRB($left, $top, $width, $height)
$bmp = New-Object System.Drawing.Bitmap ([int]$bounds.width), ([int]$bounds.height)
$graphics = [Drawing.Graphics]::FromImage($bmp)
$graphics.CopyFromScreen($bounds.Location, [Drawing.Point]::Empty, $bounds.size)
$bmp.Save('C:\\temp_screenshot.png')
$graphics.Dispose()
$bmp.Dispose()
"""

    try:
        # Execute PowerShell command
        subprocess.run(['powershell.exe', '-Command', ps_command], check=True, capture_output=True)

        # Copy from Windows to WSL
        wsl_screenshot = screenshot_path
        subprocess.run(['cp', '/mnt/c/temp_screenshot.png', wsl_screenshot], check=True)

        # Clean up Windows temp file
        subprocess.run(['powershell.exe', '-Command', 'Remove-Item C:\\temp_screenshot.png'], check=False)

        print(f"✓ Screenshot captured successfully")
        return wsl_screenshot

    except Exception as e:
        print(f"✗ PowerShell capture failed: {e}")
        return None

def analyze_gmail_screenshot(image_path):
    """Analyze screenshot and detect Gmail elements"""
    print(f"\nAnalyzing screenshot: {image_path}")

    # Load image
    img_pil = Image.open(image_path)
    img_bgr = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    print(f"Resolution: {img_pil.width} x {img_pil.height}")

    results = {}

    # 1. DETECT SELECT ALL CHECKBOX
    print("\n[1] Detecting Select All Checkbox...")
    checkbox = detect_checkbox(img_gray, img_bgr)
    results['checkbox'] = checkbox

    # 2. DETECT DELETE BUTTON
    print("\n[2] Detecting Delete Button...")
    delete_btn = detect_delete_button(img_gray, img_bgr)
    results['delete'] = delete_btn

    # 3. DETECT SELECT ALL LINK
    print("\n[3] Detecting 'Select all conversations' link...")
    select_link = detect_select_all_link(img_gray, img_bgr, img_pil)
    results['select_all_link'] = select_link

    return img_pil, results

def detect_checkbox(gray, bgr):
    """Detect the select-all checkbox in top-left area"""

    # Focus on top-left region where checkbox typically appears
    # Gmail checkbox is usually within: x: 10-150, y: 50-200
    roi_y_start, roi_y_end = 50, 250
    roi_x_start, roi_x_end = 10, 200

    roi = gray[roi_y_start:roi_y_end, roi_x_start:roi_x_end]

    # Edge detection
    edges = cv2.Canny(roi, 30, 100)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Checkbox criteria: square-ish, 14-28 pixels typically
        if 12 <= w <= 32 and 12 <= h <= 32:
            aspect_ratio = w / float(h)
            if 0.75 <= aspect_ratio <= 1.35:  # Nearly square
                # Convert to absolute coordinates
                abs_x = x + roi_x_start
                abs_y = y + roi_y_start
                center_x = abs_x + w // 2
                center_y = abs_y + h // 2

                # Calculate "leftmost + topmost" score
                score = abs_x * 0.3 + abs_y * 0.7

                candidates.append({
                    'bbox': (abs_x, abs_y, abs_x + w, abs_y + h),
                    'center': (center_x, center_y),
                    'size': (w, h),
                    'score': score
                })

    if candidates:
        # Get the topmost, leftmost checkbox
        best = min(candidates, key=lambda c: c['score'])
        print(f"  ✓ Found at center: ({best['center'][0]}, {best['center'][1]})")
        print(f"    Bbox: {best['bbox']}, Size: {best['size']}")
        return best
    else:
        print("  ✗ Not found")
        return None

def detect_delete_button(gray, bgr):
    """Detect the delete/trash button"""

    # Delete button is typically in toolbar area
    # Usually around x: 100-400, y: 50-200
    roi_y_start, roi_y_end = 50, 250
    roi_x_start, roi_x_end = 80, 500

    roi = gray[roi_y_start:roi_y_end, roi_x_start:roi_x_end]

    # Edge detection
    edges = cv2.Canny(roi, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Delete icon is typically 18-45 pixels, nearly square or slightly taller
        if 16 <= w <= 50 and 16 <= h <= 50:
            aspect_ratio = h / float(w)
            if 0.8 <= aspect_ratio <= 1.5:  # Square to slightly tall
                abs_x = x + roi_x_start
                abs_y = y + roi_y_start
                center_x = abs_x + w // 2
                center_y = abs_y + h // 2

                # Prefer elements around x=150-250 (typical delete button position)
                position_score = abs(center_x - 200) + abs(center_y - 140) * 0.5

                candidates.append({
                    'bbox': (abs_x, abs_y, abs_x + w, abs_y + h),
                    'center': (center_x, center_y),
                    'size': (w, h),
                    'score': position_score
                })

    if candidates:
        # Get best match based on expected position
        best = min(candidates, key=lambda c: c['score'])
        print(f"  ✓ Found at center: ({best['center'][0]}, {best['center'][1]})")
        print(f"    Bbox: {best['bbox']}, Size: {best['size']}")
        return best
    else:
        print("  ✗ Not found")
        return None

def detect_select_all_link(gray, bgr, img_pil):
    """Detect 'Select all conversations' link - appears after clicking checkbox"""

    # This link appears in top area, typically centered or left-aligned
    # Search area: x: 50-800, y: 100-250
    roi_y_start, roi_y_end = 100, 280
    roi_x_start, roi_x_end = 50, 900

    roi = gray[roi_y_start:roi_y_end, roi_x_start:roi_x_end]

    # Look for text-like regions using edge detection and morphology
    edges = cv2.Canny(roi, 50, 150)

    # Apply morphological operations to connect text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 3))
    dilated = cv2.dilate(edges, kernel, iterations=1)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Link text is typically wide (100-400px) and short (15-35px tall)
        if 80 <= w <= 500 and 12 <= h <= 40:
            aspect_ratio = w / float(h)
            if aspect_ratio >= 3.0:  # Wide horizontal text
                abs_x = x + roi_x_start
                abs_y = y + roi_y_start
                center_x = abs_x + w // 2
                center_y = abs_y + h // 2

                candidates.append({
                    'bbox': (abs_x, abs_y, abs_x + w, abs_y + h),
                    'center': (center_x, center_y),
                    'size': (w, h)
                })

    if candidates:
        # Get the widest text element (likely the full link text)
        best = max(candidates, key=lambda c: c['size'][0])
        print(f"  ⚠ Potentially found at center: ({best['center'][0]}, {best['center'][1]})")
        print(f"    Bbox: {best['bbox']}, Size: {best['size']}")
        print(f"    Note: This link only appears AFTER clicking the checkbox")
        return best
    else:
        print("  ⚠ Not visible (appears only after clicking checkbox)")
        return None

def create_annotated_image(img_pil, results):
    """Draw bounding boxes and labels"""
    print("\nCreating annotated image...")

    annotated = img_pil.copy()
    draw = ImageDraw.Draw(annotated)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font = ImageFont.load_default()
        small_font = font

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

        # Draw bounding box
        draw.rectangle(bbox, outline=color, width=4)

        # Draw crosshair at center
        cx, cy = center
        cross_size = 15
        draw.line([(cx - cross_size, cy), (cx + cross_size, cy)], fill=color, width=3)
        draw.line([(cx, cy - cross_size), (cx, cy + cross_size)], fill=color, width=3)

        # Draw center circle
        circle_r = 8
        draw.ellipse([(cx - circle_r, cy - circle_r), (cx + circle_r, cy + circle_r)],
                     outline=color, width=3)

        # Draw label above box
        label_y = bbox[1] - 30
        draw.text((bbox[0], label_y), label, fill=color, font=font)

        # Draw coordinates
        coord_text = f"({cx}, {cy})"
        draw.text((bbox[0], label_y + 25), coord_text, fill=color, font=small_font)

    return annotated

def print_results(results):
    """Print formatted detection results"""

    print("\n" + "=" * 75)
    print("TRIGGER RECEIVED: Locate Gmail UI Elements")
    print("=" * 75)

    print("\nDETECTED ELEMENTS:")
    print("-" * 75)

    if results['checkbox']:
        cb = results['checkbox']
        print(f"\n✓ SELECT ALL CHECKBOX:")
        print(f"  Center Coordinates: (x={cb['center'][0]}, y={cb['center'][1]})")
        print(f"  Bounding Box: {cb['bbox']}")
        print(f"  Size: {cb['size'][0]} x {cb['size'][1]} pixels")
        print(f"  Confidence: HIGH")
        print(f"  Description: Square checkbox in top-left of email list toolbar")
    else:
        print(f"\n✗ SELECT ALL CHECKBOX: NOT FOUND")
        print(f"  Confidence: N/A")

    if results['delete']:
        db = results['delete']
        print(f"\n✓ DELETE BUTTON:")
        print(f"  Center Coordinates: (x={db['center'][0]}, y={db['center'][1]})")
        print(f"  Bounding Box: {db['bbox']}")
        print(f"  Size: {db['size'][0]} x {db['size'][1]} pixels")
        print(f"  Confidence: MEDIUM-HIGH")
        print(f"  Description: Trash/delete icon button in Gmail toolbar")
    else:
        print(f"\n✗ DELETE BUTTON: NOT FOUND")
        print(f"  Confidence: N/A")

    if results['select_all_link']:
        sl = results['select_all_link']
        print(f"\n⚠ SELECT ALL CONVERSATIONS LINK:")
        print(f"  Center Coordinates: (x={sl['center'][0]}, y={sl['center'][1]})")
        print(f"  Bounding Box: {sl['bbox']}")
        print(f"  Size: {sl['size'][0]} x {sl['size'][1]} pixels")
        print(f"  Confidence: LOW-MEDIUM (detection without checkbox clicked)")
        print(f"  Description: Link text that appears after clicking main checkbox")
        print(f"  Note: This link only becomes visible AFTER clicking the checkbox")
    else:
        print(f"\n⚠ SELECT ALL CONVERSATIONS LINK: NOT VISIBLE")
        print(f"  Confidence: N/A")
        print(f"  Note: This element appears only after clicking the main checkbox")

    print("\n" + "=" * 75)
    print("AUTOMATION-READY COORDINATES (Pixel-Perfect Centers)")
    print("=" * 75)

    if results['checkbox']:
        print(f"\nCHECKBOX_X = {results['checkbox']['center'][0]}")
        print(f"CHECKBOX_Y = {results['checkbox']['center'][1]}")

    if results['delete']:
        print(f"\nDELETE_BTN_X = {results['delete']['center'][0]}")
        print(f"DELETE_BTN_Y = {results['delete']['center'][1]}")

    if results['select_all_link']:
        print(f"\nSELECT_ALL_LINK_X = {results['select_all_link']['center'][0]}")
        print(f"SELECT_ALL_LINK_Y = {results['select_all_link']['center'][1]}")

    print("\n" + "=" * 75)
    print("Result: Coordinates returned.")

    if results['checkbox'] and results['delete']:
        print("Status: PRIMARY elements detected successfully.")
    else:
        print("Status: PARTIAL detection. Please verify Gmail window is visible.")

    print("=" * 75 + "\n")

def main():
    print("=" * 75)
    print("Gmail Element Detection - WSL/Windows Edition")
    print("=" * 75)

    # Capture screenshot
    screenshot_path = capture_windows_screenshot()

    if not screenshot_path or not os.path.exists(screenshot_path):
        print("\n✗ ERROR: Could not capture screenshot")
        print("Please ensure:")
        print("  1. Gmail is open in Chrome on Windows")
        print("  2. You have permission to access Windows filesystem from WSL")
        return

    # Analyze screenshot
    img_pil, results = analyze_gmail_screenshot(screenshot_path)

    # Create annotated version
    annotated = create_annotated_image(img_pil, results)
    annotated_path = "/home/tayyabcheema777/ali/gmail_annotated.png"
    annotated.save(annotated_path)
    print(f"\n✓ Annotated screenshot saved: {annotated_path}")

    # Print formatted results
    print_results(results)

if __name__ == "__main__":
    main()
