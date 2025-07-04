#!/usr/bin/env python3
"""
Fix Requesty integration in SFA main file
"""

import re

def fix_sfa_requesty_integration(file_path):
    """Fix the Requesty integration issues in the SFA main file"""
    
    # Read the original file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix 1: Change environment variable from ROUTER_API_KEY to requesty_api_key
    content = content.replace('os.getenv("ROUTER_API_KEY")', 'os.getenv("requesty_api_key")')
    
    # Fix 2: Remove the extra Authorization header
    # Find the requesty_client initialization block and fix it
    old_client_init = '''requesty_client = openai.OpenAI(
            api_key=requesty_api_key,
            base_url="https://router.requesty.ai/v1",
            default_headers={"Authorization": f"Bearer {requesty_api_key}"}
        )'''
    
    new_client_init = '''requesty_client = openai.OpenAI(
            api_key=requesty_api_key,
            base_url="https://router.requesty.ai/v1"
        )'''
    
    content = content.replace(old_client_init, new_client_init)
    
    # Write the fixed content back
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Fixed Requesty integration in {file_path}")
    print("Changes made:")
    print("1. Changed ROUTER_API_KEY to requesty_api_key")
    print("2. Removed duplicate Authorization header")

if __name__ == "__main__":
    fix_sfa_requesty_integration("/Users/seanivore/Development/single-file-agents/sfa_v3_3_0_main.py")
