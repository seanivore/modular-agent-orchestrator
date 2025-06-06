#!/usr/bin/env python3

import json
import urllib.request
import urllib.parse

def test_requesty():
    """Test if Requesty API is working with a simple request"""
    
    requesty_url = 'https://requesty-api.fly.dev/api/v1/chat/completions'
    
    payload = {
        'model': 'google/gemini-2.5-pro-exp-03-25',
        'messages': [{'role': 'user', 'content': 'Hello! Please respond with just "Requesty is working!" to test the connection.'}],
        'max_tokens': 50
    }
    
    try:
        # Convert payload to JSON and encode
        data = json.dumps(payload).encode('utf-8')
        
        # Create request
        req = urllib.request.Request(
            requesty_url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        print("Testing Requesty connection...")
        
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode('utf-8'))
        
        if 'choices' in response_data and len(response_data['choices']) > 0:
            content = response_data['choices'][0]['message']['content']
            print(f"✅ SUCCESS: {content}")
            return True
        else:
            print(f"❌ FAILED: No content returned")
            print(f"Response: {response_data}")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    test_requesty()
