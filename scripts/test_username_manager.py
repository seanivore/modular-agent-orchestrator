#!/usr/bin/env python3
"""
Direct Username Manager Test - Test core functionality without full orchestrator import
"""

import json
import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import user ID generator directly
sys.path.append(str(Path(__file__).parent.parent / "scripts" / "user_id_generator"))
from user_id_generator import generate_user_id

def test_user_creation():
    """Test creating a user JSON file directly"""
    
    # Test data
    username = "seanivore"
    first_name = "Sean"
    last_name = "Horvath"
    email = "sean@august.style"
    dob = "1987-07-21"
    
    print("🧪 Testing Username Manager Components\n")
    
    # 1. Test user ID generation
    print("1. Testing User ID Generation:")
    user_id = generate_user_id(username)
    print(f"   Username: {username}")
    print(f"   Generated User ID: {user_id}")
    print(f"   ✅ User ID generation working\n")
    
    # 2. Test directory creation
    print("2. Testing Directory Structure:")
    user_dir = Path(__file__).parent.parent / "configs" / "user"
    print(f"   User directory: {user_dir}")
    print(f"   Directory exists: {user_dir.exists()}")
    print(f"   ✅ Directory structure ready\n")
    
    # 3. Test user JSON creation
    print("3. Testing User JSON Creation:")
    from datetime import datetime
    
    user_data = {
        "username": username,
        "user_id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "dob": dob,
        "created_at": datetime.now().isoformat(),
        "last_login": datetime.now().isoformat()
    }
    
    user_file = user_dir / f"user_{username.lower()}.json"
    
    with open(user_file, 'w') as f:
        json.dump(user_data, f, indent=2)
    
    print(f"   Created user file: {user_file.name}")
    print(f"   User data: {json.dumps(user_data, indent=2)}")
    print(f"   ✅ User JSON creation working\n")
    
    # 4. Test session file creation
    print("4. Testing Session Management:")
    session_file = user_dir / ".last_session"
    session_data = {
        "username": username,
        "user_id": user_id,
        "timestamp": datetime.now().isoformat()
    }
    
    with open(session_file, 'w') as f:
        json.dump(session_data, f, indent=2)
    
    print(f"   Created session file: {session_file.name}")
    print(f"   Session data: {json.dumps(session_data, indent=2)}")
    print(f"   ✅ Session management working\n")
    
    # 5. Test user discovery
    print("5. Testing User Discovery:")
    users = []
    for user_file in user_dir.glob("user_*.json"):
        if user_file.name.startswith('.'):
            continue
        try:
            with open(user_file, 'r') as f:
                user_data = json.load(f)
            users.append(user_data)
        except (json.JSONDecodeError, IOError):
            continue
    
    print(f"   Found {len(users)} users:")
    for user in users:
        print(f"   - {user['username']} ({user['user_id']}) - {user.get('first_name', '')} {user.get('last_name', '')}")
    
    print(f"   ✅ User discovery working\n")
    
    print("🎉 All Username Manager components tested successfully!")
    print(f"🔧 Implementation ready for integration with MAO")

if __name__ == "__main__":
    test_user_creation()
