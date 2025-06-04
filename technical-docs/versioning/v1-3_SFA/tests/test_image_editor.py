#!/usr/bin/env python3
"""
Test script for the SFA image editing tool
"""

import os
import sys
import shutil
from PIL import Image

# Add parent directory to path if running directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the tool
from tools.image_editing import edit_image

# Create test directory
TEST_DIR = "test_image_output"
os.makedirs(TEST_DIR, exist_ok=True)
print(f"Created test directory: {TEST_DIR}")

# Create a test image
test_image_path = os.path.join(TEST_DIR, "test_image.jpg")
img = Image.new('RGB', (800, 500), color=(73, 109, 137))
img.save(test_image_path)
print(f"Created test image: {test_image_path}")

# Test 1: Resize the image
print("\n[TEST 1] Resizing image...")
resize_result = edit_image(
    image_path=test_image_path,
    output_path=os.path.join(TEST_DIR, "resized.webp"),
    resize=True,
    width=600,
    maintain_aspect_ratio=True
)
print(f"Status: {resize_result['status']}")
print(f"Output: {resize_result['output_path']}")
print(f"Original size: {resize_result['original']['dimensions']['width']}x{resize_result['original']['dimensions']['height']}")
print(f"New size: {resize_result['final']['dimensions']['width']}x{resize_result['final']['dimensions']['height']}")

# Test 2: Crop image to 16:9 aspect ratio
print("\n[TEST 2] Cropping image to 16:9...")
crop_result = edit_image(
    image_path=test_image_path,
    output_path=os.path.join(TEST_DIR, "cropped.webp"),
    crop=True,
    crop_method="aspect_ratio",
    aspect_ratio="16:9",
    focus="center"
)
print(f"Status: {crop_result['status']}")
print(f"Output: {crop_result['output_path']}")
ratio = crop_result['final']['dimensions']['width'] / crop_result['final']['dimensions']['height']
print(f"Aspect ratio: {ratio:.2f} (should be close to 1.78)")

# Test 3: Add text with shade
print("\n[TEST 3] Adding text with shade layer...")
text_result = edit_image(
    image_path=test_image_path,
    output_path=os.path.join(TEST_DIR, "text.webp"),
    add_text=True,
    text="Hello World!",
    font="Open Sans",
    text_position="center",
    shade_opacity=40
)
print(f"Status: {text_result['status']}")
print(f"Output: {text_result['output_path']}")
print(f"Text added with {text_result['operations'][0]['shade_opacity']}% opacity shade")

# Test 4: Combined operations
print("\n[TEST 4] Combined resize, crop and text...")
combined_result = edit_image(
    image_path=test_image_path,
    output_path=os.path.join(TEST_DIR, "combined.webp"),
    resize=True,
    width=700,
    crop=True,
    crop_method="aspect_ratio",
    aspect_ratio="16:9",
    add_text=True,
    text="Combined Operations",
    font="Bebas Neue",
    text_position="bottom",
    shade_opacity=50,
    output_format="webp"
)
print(f"Status: {combined_result['status']}")
print(f"Output: {combined_result['output_path']}")
print(f"Operations performed: {', '.join([op['operation'] for op in combined_result['operations']])}")

print("\nTest completed! All output files are in the", TEST_DIR, "directory")
print("You can view these files to verify the image edits worked correctly.") 