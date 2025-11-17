#!/usr/bin/env python3
"""
Locate Gmail UI elements: Select All Checkbox and Delete Button
"""
import cv2
import numpy as np
from PIL import Image

# Load the screenshot
img_path = '/home/tayyabcheema777/ali/chrome_gmail.png'
img = cv2.imread(img_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

print(f"Image dimensions: {img.shape}")

# Convert to PIL for easier manipulation
pil_img = Image.open(img_path)
width, height = pil_img.size
print(f"PIL dimensions: {width}x{height}")

# Element 1: Select All Checkbox
# Looking at the image, the checkbox is in the top-left of the email list area
# It appears to be around x=128, y=70 based on visual inspection
# The checkbox is just left of the refresh icon and select dropdown

select_all_x = 128
select_all_y = 70

# Element 2: Delete Button (Trash Icon)
# The delete button appears in the toolbar after the refresh icon
# Looking at the toolbar, I can see icons after the checkbox
# The trash/delete icon should be around x=153, y=70

delete_button_x = 153
delete_button_y = 70

# Create annotated image with bounding boxes
img_annotated = img_rgb.copy()

# Draw markers for detected elements
# Select All Checkbox - Blue circle
cv2.circle(img_annotated, (select_all_x, select_all_y), 10, (0, 0, 255), 2)
cv2.putText(img_annotated, "Select All", (select_all_x + 15, select_all_y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# Delete Button - Red circle
cv2.circle(img_annotated, (delete_button_x, delete_button_y), 10, (255, 0, 0), 2)
cv2.putText(img_annotated, "Delete", (delete_button_x + 15, delete_button_y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# Save annotated image
output_path = '/home/tayyabcheema777/ali/gmail_elements_located.png'
cv2.imwrite(output_path, cv2.cvtColor(img_annotated, cv2.COLOR_RGB2BGR))

print("\n=== DETECTION RESULTS ===")
print(f"1. Select All Checkbox: (x={select_all_x}, y={select_all_y})")
print(f"2. Delete Button: (x={delete_button_x}, y={delete_button_y})")
print(f"\nAnnotated image saved to: {output_path}")
