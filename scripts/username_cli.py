#!/usr/bin/env python3
"""
Username Manager CLI - Testing and demonstration utility
Usage: python username_cli.py [command] [args...]
"""

import sys
import os
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from orchestrator.username_manager import UsernameManager

def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    manager = UsernameManager()
    
    try:
        if command == "create":
            if len(sys.argv) < 3:
                print("Usage: python username_cli.py create <username> [first_name] [last_name] [email] [dob]")
                return
            
            username = sys.argv[2]
            first_name = sys.argv[3] if len(sys.argv) > 3 else ""
            last_name = sys.argv[4] if len(sys.argv) > 4 else ""
            email = sys.argv[5] if len(sys.argv) > 5 else ""
            dob = sys.argv[6] if len(sys.argv) > 6 else ""
            
            result = manager.create_user(username, first_name, last_name, email, dob)
            print(json.dumps(result, indent=2))
        
        elif command == "load":
            if len(sys.argv) < 3:
                print("Usage: python username_cli.py load <username>")
                return
            
            username = sys.argv[2]
            result = manager.load_user(username)
            if result:
                print(json.dumps(result, indent=2))
            else:
                print(f"User '{username}' not found")
        
        elif command == "session":
            result = manager.get_session_user()
            if result:
                print(f"Current session user: {result['username']} ({result['user_id']})")
                print(json.dumps(result, indent=2))
            else:
                print("No active session")
        
        elif command == "login":
            if len(sys.argv) < 3:
                print("Usage: python username_cli.py login <username>")
                return
            
            username = sys.argv[2]
            result = manager.set_session_user(username)
            print(json.dumps(result, indent=2))
        
        elif command == "logout":
            result = manager.logout_user()
            print(json.dumps(result, indent=2))
        
        elif command == "list":
            users = manager.list_users()
            print(f"Found {len(users)} users:")
            for user in users:
                print(f"  {user['username']} ({user['user_id']}) - {user.get('first_name', '')} {user.get('last_name', '')}")
        
        elif command == "find":
            if len(sys.argv) < 3:
                print("Usage: python username_cli.py find <search_term>")
                return
            
            search_term = sys.argv[2]
            users = manager.find_user(search_term)
            print(f"Found {len(users)} matches for '{search_term}':")
            for user in users:
                print(f"  {user['username']} ({user['user_id']}) - {user.get('first_name', '')} {user.get('last_name', '')}")
        
        elif command == "settings":
            if len(sys.argv) < 4:
                print("Usage: python username_cli.py settings <username> <setting_key> <setting_value>")
                return
            
            username = sys.argv[2]
            setting_key = sys.argv[3]
            setting_value = sys.argv[4]
            
            # Try to parse as JSON for complex values
            try:
                setting_value = json.loads(setting_value)
            except:
                pass  # Keep as string
            
            result = manager.update_user_settings(username, {setting_key: setting_value})
            print(json.dumps(result, indent=2))
        
        else:
            print(f"Unknown command: {command}")
            print_help()
    
    except Exception as e:
        print(f"Error: {str(e)}")

def print_help():
    print("""
Username Manager CLI

Commands:
  create <username> [first] [last] [email] [dob]  Create new user
  load <username>                                 Load user data
  session                                         Show current session user
  login <username>                                Set session user
  logout                                          Clear session
  list                                            List all users
  find <search_term>                              Find users by name/email/etc
  settings <username> <key> <value>               Update user setting

Examples:
  python username_cli.py create seanivore Sean Horvath sean@august.style 1987-07-21
  python username_cli.py login seanivore
  python username_cli.py session
  python username_cli.py find sean
  python username_cli.py settings seanivore theme "dark mode"
""")

if __name__ == "__main__":
    main()
