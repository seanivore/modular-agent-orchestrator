#!/usr/bin/env python3
"""
Test script for the image editing tool
"""

import os
import sys
import unittest
from PIL import Image

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the tool
from tools.image_editing import edit_image

class TestImageEditing(unittest.TestCase):
    """Test cases for the image editing tool"""
    
    def setUp(self):
        """Create a test image for the tests"""
        self.test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Create a simple test image
        self.test_image_path = os.path.join(self.test_dir, "test_image.png")
        img = Image.new('RGB', (500, 300), color=(73, 109, 137))
        img.save(self.test_image_path)
        
        # Output paths
        self.resize_output = os.path.join(self.test_dir, "resized.webp")
        self.crop_output = os.path.join(self.test_dir, "cropped.webp")
        self.text_output = os.path.join(self.test_dir, "text.webp")
        self.combined_output = os.path.join(self.test_dir, "combined.webp")
    
    def tearDown(self):
        """Clean up test files"""
        for file_path in [self.resize_output, self.crop_output, self.text_output, self.combined_output]:
            if os.path.exists(file_path):
                os.remove(file_path)
    
    def test_resize(self):
        """Test image resizing"""
        result = edit_image(
            image_path=self.test_image_path,
            output_path=self.resize_output,
            resize=True,
            width=300
        )
        
        self.assertEqual(result["status"], "success")
        self.assertTrue(os.path.exists(self.resize_output))
        
        # Check dimensions
        img = Image.open(self.resize_output)
        self.assertEqual(img.width, 300)
    
    def test_crop(self):
        """Test image cropping"""
        result = edit_image(
            image_path=self.test_image_path,
            output_path=self.crop_output,
            crop=True,
            crop_method="coordinates",
            x=100,
            y=50,
            crop_width=200,
            crop_height=150
        )
        
        self.assertEqual(result["status"], "success")
        self.assertTrue(os.path.exists(self.crop_output))
        
        # Check dimensions
        img = Image.open(self.crop_output)
        self.assertEqual(img.width, 200)
        self.assertEqual(img.height, 150)
    
    def test_add_text(self):
        """Test adding text to image"""
        result = edit_image(
            image_path=self.test_image_path,
            output_path=self.text_output,
            add_text=True,
            text="Test Text",
            shade_opacity=30
        )
        
        self.assertEqual(result["status"], "success")
        self.assertTrue(os.path.exists(self.text_output))
    
    def test_combined_operations(self):
        """Test combining multiple operations"""
        result = edit_image(
            image_path=self.test_image_path,
            output_path=self.combined_output,
            resize=True,
            width=400,
            crop=True,
            crop_method="aspect_ratio",
            aspect_ratio="16:9",
            add_text=True,
            text="Combined Test",
            shade_opacity=50
        )
        
        self.assertEqual(result["status"], "success")
        self.assertTrue(os.path.exists(self.combined_output))
        
        # Check dimensions (should maintain 16:9 ratio)
        img = Image.open(self.combined_output)
        ratio = img.width / img.height
        self.assertAlmostEqual(ratio, 16/9, places=1)

if __name__ == "__main__":
    unittest.main()