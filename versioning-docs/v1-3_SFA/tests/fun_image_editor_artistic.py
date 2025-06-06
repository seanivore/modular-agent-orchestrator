#!/usr/bin/env python3
"""
Artistic Image Editor - Creates visually balanced memes with proper text placement and shading
"""

import os
import sys
import random
import requests
import re

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the image editing tool
from tools.image_editing import edit_image

# Paths
INPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_image_input")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_image_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Input image
IMAGE_PATH = os.path.join(INPUT_DIR, "sean.jpg")

def get_funny_quotes(num_quotes=10):
    """Fetch some funny programming quotes/memes"""
    print("Searching for funny programming quotes...")
    
    try:
        quotes = []
        
        # Try to get programming jokes from an API
        response = requests.get("https://v2.jokeapi.dev/joke/Programming?type=single&amount=5")
        if response.status_code == 200:
            joke_data = response.json()
            if "jokes" in joke_data:
                for joke in joke_data["jokes"]:
                    if "joke" in joke:
                        quotes.append(joke["joke"])
            elif "joke" in joke_data:
                quotes.append(joke_data["joke"])
        
        # Backup funny programming quotes
        backup_quotes = [
            "I'm not a great programmer; I'm just a good programmer with great habits.",
            "Documentation is like code comments, but someone told management about it.",
            "The best thing about a boolean is even if you are wrong, you are only off by a bit.",
            "Debugging is twice as hard as writing the code in the first place.",
            "A user interface is like a joke. If you have to explain it, it's not that good.",
            "If debugging is the process of removing software bugs, then programming must be the process of putting them in.",
            "The code works? Ship it!",
            "It works on my machine!",
            "It compiles; ship it!",
            "Sleep is for the weak. And for those who don't have debugging to do.",
            "Code never lies, comments sometimes do.",
            "Two states of every programmer: 1) I'm the smartest coder alive 2) I have no idea what I'm doing",
            "My code doesn't work, I have no idea why. My code works, I have no idea why.",
            "The hardest part of programming is naming things.",
            "When I wrote this code, only God and I understood what it did. Now only God knows."
        ]
        
        # Add backup quotes if we don't have enough
        if len(quotes) < num_quotes:
            quotes.extend(backup_quotes[:num_quotes - len(quotes)])
        
        return quotes[:num_quotes]
    except Exception as e:
        print(f"Error fetching quotes: {str(e)}")
        return [
            "Error loading jokes.js",
            "404: Humor Not Found",
            "It works on my machine!",
            "When I wrote this code, only God and I understood what it did. Now only God knows."
        ]

def assess_text_and_image(text):
    """
    Step 1: Assess the image and text to determine best approach
    - Analyzes text length to determine font size and position
    - Decides on shade opacity based on text importance
    - Determines crop focus and aspect ratio
    - Plans the edit sequence (crop first or text first)
    """
    print("\n[ARTISTIC ASSESSMENT]")
    print(f"Text to place: '{text}'")
    
    # Analyze text length to determine font size and placement
    text_length = len(text)
    words = len(text.split())
    
    # Determine text placement
    if text_length < 30:
        # Short text - can be centered
        text_position = "center"
        print("✓ Short, impactful text - will place in center for maximum emphasis")
    elif text_length < 60:
        # Medium text - better at top or bottom
        text_position = random.choice(["top", "bottom"])
        print(f"✓ Medium-length text - will place at {text_position} for readability")
    else:
        # Longer text - better at bottom
        text_position = "bottom"
        print("✓ Longer text - will place at bottom for best reading experience")
    
    # Determine shade opacity based on text length and importance
    # Longer texts need more contrast to be readable
    if text_length > 80:
        shade_opacity = random.randint(60, 80)  # Heavy shade for very long text
        print("✓ Using stronger shade (60-80%) for longer text to improve readability")
    elif text_length > 40:
        shade_opacity = random.randint(40, 60)  # Medium shade for medium text
        print("✓ Using medium shade (40-60%) for balanced text-to-image relationship")
    else:
        shade_opacity = random.randint(25, 45)  # Lighter shade for short text
        print("✓ Using lighter shade (25-45%) to maintain image visibility with shorter text")
    
    # Select font based on text style and length
    if re.search(r'[!?]$', text) or text.isupper():  # Text ends with ! or ? or is all caps
        font = "Bebas Neue"  # More impactful font for exclamations
        print("✓ Using bold, impactful font (Bebas Neue) to match text energy")
    elif words < 8:
        font = random.choice(["Bebas Neue", "Playfair Display"])  # Decorative for short phrases
        print(f"✓ Using decorative font ({font}) for short phrase")
    else:
        font = random.choice(["Open Sans", "Montserrat"])  # More readable for longer text
        print(f"✓ Using readable font ({font}) for longer text")
    
    # Determine crop aspect ratio and approach
    crop_first = random.choice([True, False])
    aspect_ratio = random.choice(["16:9", "4:3", "1:1"])
    
    if crop_first:
        print(f"✓ Artistic decision: Will crop to {aspect_ratio} FIRST, then add text")
    else:
        print(f"✓ Artistic decision: Will add text FIRST, then crop to {aspect_ratio}")
    
    return {
        "text_position": text_position,
        "shade_opacity": shade_opacity,
        "font": font,
        "crop_first": crop_first,
        "aspect_ratio": aspect_ratio
    }

def create_artistic_meme(text, output_filename="sean_artistic_meme.webp"):
    """Create a meme with artistic considerations"""
    
    # Step 1: Assess the image and plan our approach
    assessment = assess_text_and_image(text)
    
    # Determine if we're cropping first or adding text first
    if assessment["crop_first"]:
        print("\n[STEP 1] First resizing and cropping the image...")
        # Resize and crop first
        temp_path = os.path.join(OUTPUT_DIR, "temp_cropped.webp")
        crop_result = edit_image(
            image_path=IMAGE_PATH,
            output_path=temp_path,
            resize=True,
            width=800,
            maintain_aspect_ratio=True,
            crop=True,
            crop_method="aspect_ratio",
            aspect_ratio=assessment["aspect_ratio"],
            focus="center",
            output_format="webp"
        )
        
        if crop_result["status"] != "success":
            print(f"Error in cropping: {crop_result['message']}")
            return None
        
        print("\n[STEP 2] Now adding text with shade layer...")
        # Then add text to the cropped image
        final_path = os.path.join(OUTPUT_DIR, output_filename)
        final_result = edit_image(
            image_path=temp_path,
            output_path=final_path,
            add_text=True,
            text=text,
            font=assessment["font"],
            text_position=assessment["text_position"],
            shade_opacity=assessment["shade_opacity"],
            output_format="webp"
        )
        
        if final_result["status"] == "success":
            # Remove temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return final_result
        else:
            print(f"Error adding text: {final_result['message']}")
            return None
    else:
        print("\n[STEP 1] First adding text with shade layer...")
        # Add text first
        temp_path = os.path.join(OUTPUT_DIR, "temp_text.webp")
        text_result = edit_image(
            image_path=IMAGE_PATH,
            output_path=temp_path,
            resize=True,
            width=800,
            maintain_aspect_ratio=True,
            add_text=True,
            text=text,
            font=assessment["font"],
            text_position=assessment["text_position"],
            shade_opacity=assessment["shade_opacity"],
            output_format="webp"
        )
        
        if text_result["status"] != "success":
            print(f"Error adding text: {text_result['message']}")
            return None
        
        print("\n[STEP 2] Now cropping the image...")
        # Then crop the text-added image
        final_path = os.path.join(OUTPUT_DIR, output_filename)
        final_result = edit_image(
            image_path=temp_path,
            output_path=final_path,
            crop=True,
            crop_method="aspect_ratio",
            aspect_ratio=assessment["aspect_ratio"],
            focus="center",
            output_format="webp"
        )
        
        if final_result["status"] == "success":
            # Remove temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return final_result
        else:
            print(f"Error cropping: {final_result['message']}")
            return None

def main():
    # Step 1: Get funny quotes
    quotes = get_funny_quotes()
    print("\nFound funny quotes:")
    for i, quote in enumerate(quotes[:5], 1):
        print(f"{i}. {quote}")
    
    # Step 2: Select a quote for the meme
    chosen_quote = random.choice(quotes)
    print(f"\nChosen quote for meme: {chosen_quote}")
    
    # Step 3: Create the meme with artistic considerations!
    result = create_artistic_meme(chosen_quote)
    
    if result:
        print(f"\n✨ Meme created successfully! ✨")
        print(f"🔍 Image dimensions: {result['final']['dimensions']['width']}x{result['final']['dimensions']['height']}")
        print(f"💾 Saved to: {result['output_path']}")
        operations = [op['operation'] for op in result['operations']]
        print(f"🎨 Operations performed: {', '.join(operations)}")
    else:
        print("\nMeme creation failed.")

if __name__ == "__main__":
    main() 