"""
Login CLI Command - UI Display Patterns
Essential data structure for authentication flow display per NEW_USER_FLOW.md
"""

from typing import Dict, Any

def display_login_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Organize login command results for UI display per NEW_USER_FLOW.md specifications.
    
    Returns structured data for login workflow display.
    Focus: Authentication flow UI patterns as specified in NEW_USER_FLOW.md.
    """
    if not result.get("success", True):
        return _format_error_display(result)
    
    login_type = result.get("login_type", "unknown")
    
    # Route to appropriate display formatter based on login type
    display_formatters = {
        "existing_session": _format_existing_session,
        "username_required": _format_username_prompt,
        "existing_user": _format_successful_login,
        "new_user_created": _format_new_user_welcome,
        "user_not_found": _format_user_not_found,
        "username_recovery": _format_search_results
    }
    
    formatter = display_formatters.get(login_type, _format_generic_success)
    return formatter(result)

def _format_existing_session(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format display for already logged in user"""
    user_data = result.get("user_data", {})
    username = user_data.get("username", "Unknown")
    
    return {
        "display_type": "session_status",
        "header": {
            "title": "Mao welcomes you!",
            "session_active": True
        },
        "content": {
            "message": f"Already logged in as {username}",
            "user_info": {
                "username": username,
                "user_id": user_data.get("user_id", ""),
                "last_login": user_data.get("last_login", "")
            }
        },
        "actions": {
            "continue_available": True,
            "logout_available": True
        },
        "footer": {
            "show_help_hint": True,
            "help_message": "/logout to switch users, /config to change settings"
        }
    }

def _format_username_prompt(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format display for username input prompt per NEW_USER_FLOW.md"""
    return {
        "display_type": "login_prompt",
        "header": {
            "title": "Mao welcomes you!"
        },
        "content": {
            "primary_message": "What is your name?",
            "secondary_message": "Please enter User ID to continue",
            "input_required": True,
            "input_type": "username"
        },
        "input_field": {
            "placeholder": "",
            "validation": "6-20 alpha-numeric characters"
        },
        "help": {
            "message": "6-20 alpha-numeric characters",
            "show_search_option": True,
            "search_hint": "Forgot username? Try search mode"
        }
    }

def _format_successful_login(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format display for successful existing user login"""
    user_data = result.get("user_data", {})
    username = user_data.get("username", "Unknown")
    
    return {
        "display_type": "login_success",
        "header": {
            "title": "Mao welcomes you!"
        },
        "content": {
            "greeting": f"Welcome back, {username}!",
            "session_message": "Session established successfully",
            "user_info": {
                "username": username,
                "user_id": user_data.get("user_id", ""),
                "last_login": user_data.get("last_login", "")
            }
        },
        "actions": {
            "continue_to_workspace": True,
            "show_workspace_hint": True
        },
        "footer": {
            "show_help_hint": True,
            "help_message": "/help for help, /config to change settings"
        }
    }

def _format_new_user_welcome(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format display for new user creation per NEW_USER_FLOW.md theme selection flow"""
    user_data = result.get("user_data", {})
    username = user_data.get("username", "Unknown")
    
    return {
        "display_type": "new_user_welcome",
        "header": {
            "title": "Mao welcomes you!"
        },
        "conversation_flow": {
            "user_input": username,
            "greeting": f"Mao, {username}!",
            "first_time_message": "This is your first time here",
            "settings_message": "We won't ask you again, mao.",
            "settings_note": "We'll save your settings to your User ID",
            "config_hint": "Change this and other settings with /config"
        },
        "next_step": {
            "theme_selection_required": True,
            "proceed_to_theme_selection": True
        },
        "user_info": {
            "username": username,
            "user_id": user_data.get("user_id", ""),
            "created_at": user_data.get("created_at", "")
        }
    }

def _format_user_not_found(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format display for user not found scenario"""
    return {
        "display_type": "user_not_found",
        "header": {
            "title": "Mao welcomes you!"
        },
        "content": {
            "error_message": result.get("error", "User not found"),
            "suggestions": result.get("suggestions", [])
        },
        "actions": {
            "retry_available": True,
            "search_available": result.get("show_search_option", False),
            "create_new_available": True
        },
        "help": {
            "show_search_hint": True,
            "search_message": "Try search mode to find your username",
            "create_message": "Create new account if you're a first-time user"
        }
    }

def _format_search_results(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format display for username search results"""
    matches = result.get("matches", [])
    total_matches = result.get("total_matches", 0)
    
    return {
        "display_type": "search_results",
        "header": {
            "title": "Username Search Results"
        },
        "content": {
            "message": f"Found {total_matches} matching user(s)",
            "matches": [
                {
                    "username": match.get("username", ""),
                    "user_id": match.get("user_id", ""),
                    "display_name": f"{match.get('first_name', '')} {match.get('last_name', '')}".strip() or match.get("username", ""),
                    "last_login": match.get("last_login", "")
                }
                for match in matches
            ]
        },
        "actions": {
            "select_user_available": True,
            "new_search_available": True
        }
    }

def _format_error_display(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format display for error states"""
    return {
        "display_type": "error",
        "header": {
            "title": "Login Error"
        },
        "content": {
            "error_message": result.get("error", "Unknown error occurred"),
            "suggestions": result.get("suggestions", [])
        },
        "actions": {
            "retry_available": True,
            "help_available": True
        },
        "help": {
            "show_help_hint": True,
            "help_message": "Check username format or try search mode"
        }
    }

def _format_generic_success(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format display for generic success states"""
    return {
        "display_type": "success",
        "header": {
            "title": "Login Successful"
        },
        "content": {
            "message": result.get("message", "Login completed successfully")
        },
        "actions": {
            "continue_available": True
        }
    }

def get_display_requirements() -> Dict[str, Any]:
    """
    Define essential display requirements for UI implementation per NEW_USER_FLOW.md.
    
    Returns what a UI designer would need to know for login flow.
    """
    return {
        "layout_pattern": "new_user_flow_compliant",
        "essential_elements": [
            "header_with_mao_branding",
            "conversation_flow_display",
            "input_field_with_validation",
            "help_messages_with_question_mark",
            "action_buttons_contextual"
        ],
        "branding_requirements": {
            "header_format": "Mao welcomes you!",
            "conversation_bullets": "Primary messages and secondary context",
            "user_input_display": "Input field with faded placeholder text",
            "help_indicator": "Help text under input field"
        },
        "interaction_patterns": {
            "username_input": "text field with validation",
            "search_mode": "optional username recovery",
            "new_user_flow": "automatic theme selection after creation",
            "session_management": "persistent login state"
        },
        "authentication_flow": [
            "check_existing_session",
            "prompt_username_if_needed", 
            "validate_and_authenticate",
            "handle_new_user_creation",
            "set_session_and_proceed"
        ],
        "error_handling": {
            "validation_errors": "inline with input field",
            "authentication_errors": "with retry options",
            "search_no_results": "with alternative suggestions"
        },
        "security_considerations": [
            "session_based_caching",
            "username_format_validation",
            "no_password_storage_required",
            "secure_session_management"
        ]
    }

def display_error(error_message: str) -> Dict[str, Any]:
    """Provide error display structure"""
    return {
        "display_type": "error",
        "error_message": error_message,
        "suggestions": [
            "Check username format (6-20 alphanumeric)",
            "Try username search if you forgot it",
            "Contact administrator if you need help"
        ],
        "show_help_hint": True
    }

def get_theme_selection_display() -> Dict[str, Any]:
    """
    Provide theme selection display structure for new users per NEW_USER_FLOW.md.
    
    This is called after successful new user creation.
    """
    return {
        "display_type": "theme_selection",
        "header": {
            "title": "Mao welcomes you!"
        },
        "content": {
            "message": "Which text style looks best on your screen?",
            "options": [
                {"id": 1, "name": "Dark mode", "description": "Standard dark mode"},
                {"id": 2, "name": "Light mode", "description": "Standard light mode"},
                {"id": 3, "name": "Dark mode (CVD)", "description": "High contrast for colorblind users"},
                {"id": 4, "name": "Light mode (CVD)", "description": "High contrast light mode"},
                {"id": 5, "name": "Dark mode (ANSI colors only)", "description": "Terminal compatibility"},
                {"id": 6, "name": "Light mode (ANSI colors only)", "description": "Terminal compatibility"}
            ],
            "preview_available": True
        },
        "interaction": {
            "selection_method": "arrow_keys_and_enter",
            "preview_updates": "real_time_as_user_navigates"
        }
    }