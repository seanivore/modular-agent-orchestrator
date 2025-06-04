#!/usr/bin/env python3
"""
Test script for SFA v3_3_0 model parameter handling
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def create_test_configs():
    """Create test configuration files with different model settings."""
    print("Creating test configurations...")
    
    test_dir = Path(__file__).parent
    
    # Config with model in config file
    config_with_model = {
        "A": "model-test-config",
        "F": str(test_dir),
        "M": "google/gemini-2.5-pro-exp-03-25",
        "test": [
            {
                "PHASE_0": [{
                    "U": "You are a test assistant",
                    "X": "Print the name of the model being used",
                    "O": [str(test_dir / "model_from_config.txt")]
                }]
            }
        ]
    }
    
    # Config without model
    config_without_model = {
        "A": "model-test-config-no-model",
        "F": str(test_dir),
        "test": [
            {
                "PHASE_0": [{
                    "U": "You are a test assistant",
                    "X": "Print the name of the model being used",
                    "O": [str(test_dir / "model_from_arg.txt")]
                }]
            }
        ]
    }
    
    # Write the config files
    with open(test_dir / "config_with_model.json", "w") as f:
        json.dump(config_with_model, f, indent=2)
    
    with open(test_dir / "config_without_model.json", "w") as f:
        json.dump(config_without_model, f, indent=2)
    
    return test_dir

def run_model_tests(sfa_path, test_dir):
    """Run model handling tests."""
    if not Path(sfa_path).exists():
        print(f"ERROR: Agent file not found: {sfa_path}")
        return False
    
    print(f"\n=== Testing model handling in {sfa_path} ===")
    tests = []
    
    # Test 1: Model from config file
    print("\n--- Test 1: Model from config file ---")
    try:
        cmd = [sys.executable, sfa_path, "--config-file", str(test_dir / "config_with_model.json"), "--phase", "0"]
        print(f"Running: {' '.join(cmd)}")
        
        # For actual testing, remove the --dry-run flag
        result = subprocess.run(cmd + ["--dry-run"], capture_output=True, text=True)
        print(f"Command returned: {result.returncode}")
        
        # Check if model name appears in output
        if "google/gemini-2.5-pro-exp-03-25" in result.stdout:
            print("✓ Model from config appears in output")
            tests.append(True)
        else:
            print("✗ Model from config not found in output")
            tests.append(False)
    except Exception as e:
        print(f"ERROR: Test 1 failed: {str(e)}")
        tests.append(False)
    
    # Test 2: Model from command line argument
    print("\n--- Test 2: Model from command line argument ---")
    try:
        cmd = [
            sys.executable, 
            sfa_path, 
            "--config-file", 
            str(test_dir / "config_without_model.json"), 
            "--phase", 
            "0", 
            "--model", 
            "claude-3-opus-20240229"
        ]
        print(f"Running: {' '.join(cmd)}")
        
        # For actual testing, remove the --dry-run flag
        result = subprocess.run(cmd + ["--dry-run"], capture_output=True, text=True)
        print(f"Command returned: {result.returncode}")
        
        # Check if model name appears in output
        if "claude-3-opus-20240229" in result.stdout:
            print("✓ Model from argument appears in output")
            tests.append(True)
        else:
            print("✗ Model from argument not found in output")
            tests.append(False)
    except Exception as e:
        print(f"ERROR: Test 2 failed: {str(e)}")
        tests.append(False)
    
    # Test 3: Command line model overrides config model
    print("\n--- Test 3: Command line model overrides config model ---")
    try:
        cmd = [
            sys.executable, 
            sfa_path, 
            "--config-file", 
            str(test_dir / "config_with_model.json"), 
            "--phase", 
            "0", 
            "--model", 
            "claude-3-sonnet-20240229"
        ]
        print(f"Running: {' '.join(cmd)}")
        
        # For actual testing, remove the --dry-run flag
        result = subprocess.run(cmd + ["--dry-run"], capture_output=True, text=True)
        print(f"Command returned: {result.returncode}")
        
        # Check if the right model name appears in output
        if "claude-3-sonnet-20240229" in result.stdout and "google/gemini-2.5-pro-exp-03-25" not in result.stdout:
            print("✓ Command line model overrides config model")
            tests.append(True)
        else:
            print("✗ Command line model override failed")
            tests.append(False)
    except Exception as e:
        print(f"ERROR: Test 3 failed: {str(e)}")
        tests.append(False)
    
    # Overall result
    if all(tests):
        print("\n=== All model handling tests passed! ===")
        return True
    else:
        print("\n=== Some model handling tests failed. See above for details. ===")
        return False

def main():
    """Main function to run the tests."""
    print("=== Running SFA v3_3_0 Model Parameter Handling Tests ===")
    
    # Create test configurations
    test_dir = create_test_configs()
    
    # Check for agent file - use underscore naming convention
    sfa_path = Path(__file__).parents[3] / "sfa_v3_3_0_main.py"
    
    if not sfa_path.exists():
        print(f"WARNING: Main agent file not found at {sfa_path}")
        print("Cannot run actual model tests without the agent file.")
        print("This script would validate:")
        print("1. Model parameter from config file")
        print("2. Model parameter from command line arguments")
        print("3. Command line arguments overriding config file settings")
        return False
    
    # Run the tests
    return run_model_tests(str(sfa_path), test_dir)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 