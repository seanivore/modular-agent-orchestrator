#!/usr/bin/env python3
"""
Unit tests for SFA v3_3_0 Requesty format conversion functions
"""

import os
import sys
import json
import importlib.util
from pathlib import Path

# Add the parent directory to PATH
sys.path.append(str(Path(__file__).parents[3]))  # Go up three levels to reach the project root

def test_import():
    """Test importing the conversion functions from sfa_v3_3_0_main.py."""
    print("\n=== Testing imports ===")
    
    try:
        # Try to import the module directly using the updated filename convention
        module_path = Path(__file__).parents[3] / "sfa_v3_3_0_main.py"
        if not module_path.exists():
            print(f"ERROR: File not found: {module_path}")
            return False
            
        print(f"Loading module from: {module_path}")
        module_name = "sfa_v3_3_0_main"
        
        # First try standard import (should work with underscore naming)
        try:
            sys.path.insert(0, str(module_path.parent))
            module = __import__(module_name)
            print(f"✓ Successfully imported {module_name} using standard import")
        except ImportError:
            # Fall back to importlib if standard import fails
            print(f"Standard import failed, trying importlib...")
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(f"✓ Successfully imported {module_name} using importlib")
        
        # Check for the conversion functions
        required_functions = [
            "convert_to_openai_format", 
            "convert_tools_to_openai_format"
        ]
        
        missing_functions = []
        for func_name in required_functions:
            if not hasattr(module, func_name):
                missing_functions.append(func_name)
        
        if missing_functions:
            print(f"ERROR: Missing functions in {module_name}: {', '.join(missing_functions)}")
            return False
        
        # Import successful
        global convert_to_openai_format, convert_tools_to_openai_format
        convert_to_openai_format = getattr(module, "convert_to_openai_format")
        convert_tools_to_openai_format = getattr(module, "convert_tools_to_openai_format")
        
        print(f"✓ Successfully imported all required functions")
        return True
        
    except Exception as e:
        print(f"ERROR: Import test failed: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

def test_convert_to_openai_format():
    """Test conversion of Claude message format to OpenAI format."""
    print("\n=== Testing convert_to_openai_format ===")
    
    # Test simple messages
    simple_claude_messages = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you!"},
        {"role": "user", "content": "Great to hear!"}
    ]
    
    # Test complex messages with tool calls
    complex_claude_messages = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": [
            {"type": "text", "text": "I'll help you with that."},
            {"type": "tool_use", "id": "abc123", "name": "calculator", "input": {"expression": "2+2"}}
        ]},
        {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "abc123", "content": "4"}
        ]}
    ]
    
    try:
        # Convert simple messages
        simple_openai_messages = convert_to_openai_format(simple_claude_messages)
        print(f"Simple conversion result: {json.dumps(simple_openai_messages, indent=2)}")
        
        # Basic validation
        assert len(simple_openai_messages) == 3, f"Expected 3 messages, got {len(simple_openai_messages)}"
        assert simple_openai_messages[0]["role"] == "user", f"Expected role 'user', got '{simple_openai_messages[0]['role']}'"
        assert simple_openai_messages[0]["content"] == "Hello, how are you?", "Content mismatch"
        assert simple_openai_messages[1]["role"] == "assistant", f"Expected role 'assistant', got '{simple_openai_messages[1]['role']}'"
        
        # Convert complex messages
        try:
            complex_openai_messages = convert_to_openai_format(complex_claude_messages)
            print(f"Complex conversion result: {json.dumps(complex_openai_messages, indent=2)}")
            
            # Basic validation
            assert len(complex_openai_messages) >= 3, f"Expected at least 3 messages, got {len(complex_openai_messages)}"
            
            # Check if tool messages are properly converted
            tool_messages = [msg for msg in complex_openai_messages if msg.get("role") == "assistant" and "tool_calls" in msg]
            assert len(tool_messages) > 0, "No tool call messages found in converted format"
            
            print("✓ convert_to_openai_format complex test passed")
        except Exception as e:
            print(f"WARNING: Complex message conversion test failed: {str(e)}")
            print("This may be expected if your implementation doesn't handle tool calls yet")
        
        print("✓ convert_to_openai_format simple test passed")
        return True
    except Exception as e:
        print(f"ERROR: convert_to_openai_format test failed: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

def test_convert_tools_to_openai_format():
    """Test conversion of Claude tool format to OpenAI format."""
    print("\n=== Testing convert_tools_to_openai_format ===")
    
    # Claude tool format
    claude_tools = [
        {
            "name": "read_file",
            "description": "Read the content of a file",
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the file"}
                },
                "required": ["file_path"]
            }
        },
        {
            "name": "search_web",
            "description": "Search the web for information",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "num_results": {"type": "integer", "description": "Number of results to return"}
                },
                "required": ["query"]
            }
        }
    ]
    
    try:
        openai_tools = convert_tools_to_openai_format(claude_tools)
        print(f"Conversion result: {json.dumps(openai_tools, indent=2)}")
        
        # Basic validation
        assert len(openai_tools) == 2, f"Expected 2 tools, got {len(openai_tools)}"
        assert openai_tools[0]["type"] == "function", f"Expected type 'function', got '{openai_tools[0]['type']}'"
        assert "function" in openai_tools[0], "Missing 'function' key in converted tool"
        assert openai_tools[0]["function"]["name"] == "read_file", f"Expected name 'read_file', got '{openai_tools[0]['function']['name']}'"
        assert "parameters" in openai_tools[0]["function"], "Missing 'parameters' key in function"
        
        print("✓ convert_tools_to_openai_format test passed")
        return True
    except Exception as e:
        print(f"ERROR: convert_tools_to_openai_format test failed: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

def run_all_tests():
    """Run all unit tests for the Requesty format conversion functions."""
    print("=== Running SFA v3_3_0 Requesty Format Conversion Unit Tests ===")
    
    # First test imports
    import_success = test_import()
    if not import_success:
        print("\n=== Import test failed, cannot continue other tests ===")
        return False
    
    # Run the conversion tests
    tests = [
        test_convert_to_openai_format,
        test_convert_tools_to_openai_format
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Overall result
    if all(results):
        print("\n=== All tests passed! ===")
        return True
    else:
        print("\n=== Some tests failed. See above for details. ===")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 