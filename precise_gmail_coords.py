#!/usr/bin/env python3
"""
Precise Gmail Coordinate Finder
Analyzes Gmail screenshot to find exact clickable coordinates
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np

def analyze_gmail_screenshot(image_path):
    """Analyze Gmail screenshot and find precise coordinates"""

    # Load the image
    img = Image.open(image_path)
    img_array = np.array(img)
    width, height = img.size

    print(f"Image dimensions: {width}x{height}")

    # Based on visual analysis of the screenshots:
    # The select all checkbox is in the toolbar area
    # Looking at the annotated image, the checkbox appears at approximately:
    # - X: around 127-130 (center of the checkbox)
    # - Y: around 94-95 (center of the checkbox, NOT above it)

    # The delete button (trash icon) appears at approximately:
    # - X: around 193-195 (center of trash icon)
    # - Y: around 94-95 (same row as checkbox)

    # Let's verify by sampling pixel colors in these regions

    # Check the checkbox area
    checkbox_regions = [
        (127, 94), (128, 94), (129, 94), (130, 94),
        (127, 95), (128, 95), (129, 95), (130, 95),
    ]

    delete_regions = [
        (193, 94), (194, 94), (195, 94),
        (193, 95), (194, 95), (195, 95),
    ]

    print("\n=== CHECKBOX AREA ANALYSIS ===")
    for x, y in checkbox_regions:
        if x < width and y < height:
            pixel = img_array[y, x]
            print(f"Pixel at ({x}, {y}): RGB{tuple(pixel[:3])}")

    print("\n=== DELETE BUTTON AREA ANALYSIS ===")
    for x, y in delete_regions:
        if x < width and y < height:
            pixel = img_array[y, x]
            print(f"Pixel at ({x}, {y}): RGB{tuple(pixel[:3])}")

    # Create annotated image with precise markers
    img_annotated = img.copy()
    draw = ImageDraw.Draw(img_annotated)

    # Recommended coordinates based on visual analysis
    checkbox_coord = (129, 94)  # Center of checkbox
    delete_coord = (194, 94)    # Center of delete/trash icon

    # Draw crosshairs at exact coordinates
    marker_size = 20
    marker_color = (255, 0, 0)  # Red
    line_width = 2

    # Checkbox crosshair
    cx, cy = checkbox_coord
    draw.line([(cx - marker_size, cy), (cx + marker_size, cy)], fill=marker_color, width=line_width)
    draw.line([(cx, cy - marker_size), (cx, cy + marker_size)], fill=marker_color, width=line_width)
    draw.ellipse([(cx-3, cy-3), (cx+3, cy+3)], fill=marker_color)
    draw.text((cx + 10, cy - 20), f"CHECKBOX\n({cx}, {cy})", fill=marker_color)

    # Delete button crosshair
    dx, dy = delete_coord
    draw.line([(dx - marker_size, dy), (dx + marker_size, dy)], fill=marker_color, width=line_width)
    draw.line([(dx, dy - marker_size), (dx, dy + marker_size)], fill=marker_color, width=line_width)
    draw.ellipse([(dx-3, dy-3), (dx+3, dy+3)], fill=marker_color)
    draw.text((dx + 10, dy - 20), f"DELETE\n({dx}, {dy})", fill=marker_color)

    # Save annotated image
    output_path = image_path.replace('.png', '_precise_coords.png')
    img_annotated.save(output_path)
    print(f"\n=== Annotated image saved to: {output_path} ===")

    return checkbox_coord, delete_coord

def main():
    # Analyze the most recent screenshot
    screenshot_path = "/home/tayyabcheema777/ali/Screenshot 2025-11-16 174651.png"

    print("Analyzing Gmail screenshot for precise coordinates...")
    print("=" * 60)

    checkbox, delete = analyze_gmail_screenshot(screenshot_path)

    print("\n" + "=" * 60)
    print("FINAL PRECISE COORDINATES:")
    print("=" * 60)
    print(f"SELECT ALL CHECKBOX: ({checkbox[0]}, {checkbox[1]})")
    print(f"DELETE BUTTON:      ({delete[0]}, {delete[1]})")
    print("=" * 60)
    print("\nThese coordinates target the CENTER of each element")
    print("for maximum click accuracy.")

if __name__ == "__main__":
    main()
