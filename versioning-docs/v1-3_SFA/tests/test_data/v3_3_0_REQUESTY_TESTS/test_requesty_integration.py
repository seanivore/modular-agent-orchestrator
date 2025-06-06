#!/usr/bin/env python3
"""
Test script for SFA v3_3_0 Requesty API integration
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path

# Add the parent directory to PATH
sys.path.append(str(Path(__file__).parents[3]))  # Go up three levels to reach the project root

def setup_test_environment():
    """Set up test directories and files."""
    print("Setting up test environment...")
    
    # Create test directories
    test_dir = Path(__file__).parent
    
    # Create sample job description
    job_description = """# Frontend Developer

**Company:** Tech Innovators, Inc.
**Location:** Remote, United States

## Job Description
We're looking for a talented Frontend Developer to join our team. The ideal candidate has experience with React, JavaScript, and responsive design.

## Requirements
- 3+ years of experience with JavaScript and React
- Experience with responsive design and CSS frameworks
- Knowledge of modern frontend build tools
- Excellent communication skills

## Nice-to-have
- Experience with TypeScript
- Knowledge of GraphQL
- Experience with Redux or similar state management libraries
    """
    
    # Create sample resume
    base_resume = """# Sean Developer

**Email:** sean@example.com
**Phone:** (555) 123-4567
**Location:** San Francisco, CA

## Experience

### Senior Developer, Current Company (2020-Present)
- Led development of responsive web applications using React and TypeScript
- Implemented complex state management using Redux
- Collaborated with design team to create intuitive user interfaces

### Web Developer, Previous Company (2017-2020)
- Built and maintained multiple client websites
- Implemented responsive designs using CSS frameworks
- Integrated third-party APIs for payment processing

## Skills
- JavaScript / TypeScript
- React / Redux
- HTML5 / CSS3
- Responsive Design
- Git / GitHub
- Node.js basics
    """
    
    # Write files
    with open(test_dir / "job_description.md", "w") as f:
        f.write(job_description)
    
    with open(test_dir / "base_resume.md", "w") as f:
        f.write(base_resume)
    
    # Create test config
    config = {
        "A": "job-app-test",
        "F": str(test_dir),
        "M": "google/gemini-2.5-pro-exp-03-25",
        "job-app": [
            {
                "PHASE_0": [{
                    "U": "You are a professional resume writer helping job applicants customize their resumes.",
                    "X": "Create a targeted resume based on the job description and base resume. Focus on highlighting relevant skills and experience to match the job requirements. Keep the same basic format but reorder or emphasize different aspects to match the job.",
                    "Y": [str(test_dir / "base_resume.md"), str(test_dir / "job_description.md")],
                    "Z": "A targeted resume in markdown format highlighting relevant experience.",
                    "O": [str(test_dir / "targeted_resume_gemini.md")]
                }]
            }
        ]
    }
    
    # Create the same config without model (will use Claude by default)
    config_claude = dict(config)
    config_claude.pop("M", None)  # Remove model field
    config_claude["job-app"][0]["PHASE_0"][0]["O"] = [str(test_dir / "targeted_resume_claude.md")]
    
    # Write configs
    with open(test_dir / "config_gemini.json", "w") as f:
        json.dump(config, f, indent=2)
    
    with open(test_dir / "config_claude.json", "w") as f:
        json.dump(config_claude, f, indent=2)
    
    print(f"✓ Test environment set up successfully")
    return test_dir

def run_model_test(model_name, config_path):
    """Run a test with the specified model and config."""
    print(f"\n=== Testing with {model_name} ===")
    
    try:
        # Check if sfa_v3_3_0_main.py exists
        if not Path("sfa_v3_3_0_main.py").exists():
            print(f"ERROR: sfa_v3_3_0_main.py not found in current directory")
            return False, None
            
        # Run the SFA with the config
        start_time = time.time()
        result = subprocess.run(
            [sys.executable, "sfa_v3_3_0_main.py", "--config-file", str(config_path), "--phase", "0"],
            capture_output=True,
            text=True
        )
        end_time = time.time()
        
        # Check the result
        if result.returncode != 0:
            print(f"ERROR: Process failed with code {result.returncode}")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False, None
        
        # Parse token usage and performance metrics
        elapsed_time = end_time - start_time
        metrics = {"elapsed_time": elapsed_time}
        
        for line in result.stdout.split("\n"):
            if "Token Usage - Total:" in line:
                parts = line.split("|")
                for part in parts:
                    if "Input:" in part:
                        metrics["input_tokens"] = int(part.split("Input:")[1].strip().replace(",", ""))
                    elif "Output:" in part:
                        metrics["output_tokens"] = int(part.split("Output:")[1].strip().replace(",", ""))
                    elif "Cost:" in part:
                        metrics["cost"] = float(part.split("Cost: $")[1].strip())
        
        print(f"✓ Test completed in {elapsed_time:.2f} seconds")
        print(f"✓ Input tokens: {metrics.get('input_tokens', 'unknown')}")
        print(f"✓ Output tokens: {metrics.get('output_tokens', 'unknown')}")
        print(f"✓ Cost: ${metrics.get('cost', 'unknown')}")
        
        return True, metrics
    
    except Exception as e:
        print(f"ERROR: Test failed: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False, None

def compare_results(test_dir, gemini_metrics, claude_metrics):
    """Compare the results from different models."""
    print("\n=== Comparing Results ===")
    
    if not gemini_metrics or not claude_metrics:
        print("ERROR: Missing metrics for comparison")
        return False
        
    print("Performance Comparison:")
    print(f"  Execution time: Gemini: {gemini_metrics['elapsed_time']:.2f}s vs Claude: {claude_metrics['elapsed_time']:.2f}s")
    
    if 'input_tokens' in gemini_metrics and 'input_tokens' in claude_metrics:
        print(f"  Input tokens: Gemini: {gemini_metrics['input_tokens']} vs Claude: {claude_metrics['input_tokens']}")
    
    if 'output_tokens' in gemini_metrics and 'output_tokens' in claude_metrics:
        print(f"  Output tokens: Gemini: {gemini_metrics['output_tokens']} vs Claude: {claude_metrics['output_tokens']}")
    
    if 'cost' in gemini_metrics and 'cost' in claude_metrics:
        print(f"  Cost: Gemini: ${gemini_metrics['cost']:.6f} vs Claude: ${claude_metrics['cost']:.6f}")
        print(f"  Cost saving with Gemini: ${claude_metrics['cost'] - gemini_metrics['cost']:.6f}")
    
    # Check if output files exist
    gemini_output = test_dir / "targeted_resume_gemini.md"
    claude_output = test_dir / "targeted_resume_claude.md"
    
    if gemini_output.exists() and claude_output.exists():
        with open(gemini_output, "r") as f:
            gemini_content = f.read()
        
        with open(claude_output, "r") as f:
            claude_content = f.read()
            
        print("\nOutput Comparison:")
        print(f"  Gemini output length: {len(gemini_content)} characters")
        print(f"  Claude output length: {len(claude_content)} characters")
        
    return True

def run_all_tests():
    """Run all tests for Requesty API integration."""
    print("=== Running SFA v3_3_0 Requesty API Integration Tests ===")
    
    # Setup test environment
    test_dir = setup_test_environment()
    
    # Run test with Gemini model
    gemini_success, gemini_metrics = run_model_test("Gemini", test_dir / "config_gemini.json")
    
    # Run test with Claude model
    claude_success, claude_metrics = run_model_test("Claude", test_dir / "config_claude.json")
    
    # Compare results if both tests were successful
    if gemini_success and claude_success:
        comparison_success = compare_results(test_dir, gemini_metrics, claude_metrics)
    else:
        comparison_success = False
    
    # Overall status
    all_success = gemini_success and claude_success and comparison_success
    
    if all_success:
        print("\n=== All tests passed! ===")
    else:
        print("\n=== Some tests failed. See above for details. ===")
    
    return all_success

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 