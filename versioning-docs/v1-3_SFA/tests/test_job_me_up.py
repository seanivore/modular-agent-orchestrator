#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import time
from pathlib import Path

# Add the parent directory to PATH so we can import from the sfa_main module
sys.path.append(str(Path(__file__).parent.parent))

def run_test():
    """Test the job-me-up workflow with our fixed SFA implementation."""
    print("=== Testing job-me-up workflow ===")
    
    # Paths
    cwd = Path.cwd()
    config_path = cwd / "use-case" / "job-me-up" / "job-me-up-config.json"
    token_stats_path = cwd / "use-case" / "job-me-up" / "token_stats_job-me-up-config.json"
    
    # Verify files exist
    if not config_path.exists():
        print(f"ERROR: Config file not found at {config_path}")
        return False
        
    # 1. Reset token stats to ensure clean test
    print("Resetting token stats...")
    try:
        stats = {
            "workflow_id": "job-me-up-config",
            "cumulative_tokens": 0,
            "cumulative_cost": 0.0,
            "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S.%f")
        }
        
        with open(token_stats_path, 'w') as f:
            json.dump(stats, f, indent=2)
            f.write('\n')
        print("✓ Token stats reset")
    except Exception as e:
        print(f"ERROR: Failed to reset token stats: {str(e)}")
        return False
    
    # 2. Run the SFA workflow with the job-me-up config for phase 0 only
    print("\nRunning SFA with job-me-up config (phase 0 only)...")
    try:
        # Run sfa_main.py with the config file
        result = subprocess.run(
            [sys.executable, "sfa_main.py", "--config-file", str(config_path), "--phase", "0"],
            capture_output=True,
            text=True
        )
        
        # Check for successful completion
        if result.returncode != 0:
            print(f"ERROR: SFA process failed with code {result.returncode}")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
        print("✓ SFA process completed successfully")
        
        # Print the interesting parts of the output
        for line in result.stdout.split('\n'):
            if any(marker in line for marker in [
                "Token Usage", "Phase completed", "Progress:", "Output saved", 
                "All expected outputs saved", "Task completed"
            ]):
                print(f"  {line}")
                
    except Exception as e:
        print(f"ERROR: Failed to run SFA: {str(e)}")
        return False
    
    # 3. Verify token stats were properly updated
    print("\nVerifying token stats were updated...")
    try:
        with open(token_stats_path, 'r') as f:
            stats = json.load(f)
            
        if stats["cumulative_tokens"] > 0:
            print(f"✓ Token stats updated - {stats['cumulative_tokens']:,} tokens used")
        else:
            print("ERROR: Token stats were not updated properly")
            return False
    except Exception as e:
        print(f"ERROR: Failed to verify token stats: {str(e)}")
        return False
    
    print("\n=== All tests passed! ===")
    return True

if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1) 