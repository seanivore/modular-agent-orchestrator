#!/usr/bin/env python3

import os
import openai

# Load .env file manually since it's not auto-loaded
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv not available, load manually
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def test_requesty_new():
    """Test the new Requesty API format with OpenAI SDK"""
    
    try:
        # Initialize OpenAI client for Requesty
        client = openai.OpenAI(
            api_key=os.environ.get('requesty_api_key', 'demo-key'),
            base_url="https://router.requesty.ai/v1"
        )

        print("Testing new Requesty connection with OpenAI SDK...")
        
        # Example request
        response = client.chat.completions.create(
            model="google/gemini-2.5-pro-exp-03-25",
            messages=[{"role": "user", "content": "Hello! Please respond with just 'New Requesty format is working!' to test the connection."}],
            max_tokens=50
        )

        # Check if the response is successful
        if not response.choices:
            raise Exception("No response choices found.")

        # Print the result
        content = response.choices[0].message.content
        print(f"✅ SUCCESS: {content}")
        return True

    except openai.OpenAIError as e:
        print(f"❌ OpenAI API error: {e}")
        return False

    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    test_requesty_new()
