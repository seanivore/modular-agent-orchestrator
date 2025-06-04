#!/usr/bin/env python3
"""
Fun Image Editor - Creates a meme with funny programming quotes
"""

import os
import sys
import random
import requests

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

def create_meme(text, output_filename="sean_meme.webp"):
    """Create a meme with the given text"""
    print(f"Creating meme with text: '{text}'")
    
    # Choose a random font from available options
    fonts = ["Bebas Neue", "Open Sans", "Montserrat", "Playfair Display"]
    chosen_font = random.choice(fonts)
    
    # Choose text position
    positions = ["top", "bottom", "center"]
    chosen_position = random.choice(positions)
    
    # Create output path
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    # Apply image editing with the chosen text
    result = edit_image(
        image_path=IMAGE_PATH,
        output_path=output_path,
        resize=True,
        width=800,
        maintain_aspect_ratio=True,
        crop=True,
        crop_method="aspect_ratio",
        aspect_ratio="4:3",
        focus="center",
        add_text=True,
        text=text,
        font=chosen_font,
        text_position=chosen_position,
        shade_opacity=random.randint(30, 60)
    )
    
    if result["status"] == "success":
        print(f"Meme created successfully! Saved to: {output_path}")
        print(f"Font: {chosen_font}, Position: {chosen_position}")
        return output_path
    else:
        print(f"Error creating meme: {result['message']}")
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
    
    # Step 3: Create the meme!
    meme_path = create_meme(chosen_quote)
    
    if meme_path:
        print(f"\nAll done! Open {meme_path} to view your meme!")
    else:
        print("\nMeme creation failed.")

if __name__ == "__main__":
    main() 