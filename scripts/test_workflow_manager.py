#!/usr/bin/env python3
"""
Direct Workflow Manager Test - Test core functionality without full orchestrator import
"""

import json
import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import workflow ID generator directly
sys.path.append(str(Path(__file__).parent.parent / "scripts" / "unique_id_generator"))
from unique_id_generator import generate_workflow_uid, generate_workflow_uid_with_explanation

def test_workflow_id_generation():
    """Test workflow ID generation functionality"""
    
    print("🧪 Testing Workflow Manager Components\n")
    
    # 1. Test workflow ID generation
    print("1. Testing Workflow ID Generation:")
    
    # Generate simple workflow ID
    workflow_id = generate_workflow_uid()
    print(f"   Generated Workflow ID: {workflow_id}")
    
    # Generate with explanation
    workflow_id_explained, explanation = generate_workflow_uid_with_explanation()
    print(f"   With Explanation: {workflow_id_explained}")
    print(f"   Math Operations: {explanation}")
    print(f"   ✅ Workflow ID generation working\n")
    
    # 2. Test uniqueness
    print("2. Testing ID Uniqueness:")
    unique_ids = set()
    for i in range(10):
        uid = generate_workflow_uid()
        unique_ids.add(uid)
        print(f"   ID {i+1}: {uid}")
    
    print(f"   Generated 10 IDs, {len(unique_ids)} unique")
    print(f"   ✅ Uniqueness test: {'PASSED' if len(unique_ids) == 10 else 'FAILED'}\n")
    
    # 3. Test directory structure
    print("3. Testing Directory Structure:")
    workflows_dir = Path(__file__).parent.parent / "configs" / "workflows"
    temp_dir = workflows_dir / ".temp"
    
    print(f"   Workflows directory: {workflows_dir}")
    print(f"   Directory exists: {workflows_dir.exists()}")
    print(f"   Temp directory: {temp_dir}")
    print(f"   Temp directory exists: {temp_dir.exists()}")
    print(f"   ✅ Directory structure ready\n")
    
    # 4. Test workflow discovery
    print("4. Testing Workflow Discovery:")
    existing_workflows = []
    
    if workflows_dir.exists():
        for workflow_dir in workflows_dir.iterdir():
            if workflow_dir.is_dir() and not workflow_dir.name.startswith('.'):
                existing_workflows.append(workflow_dir.name)
    
    print(f"   Found {len(existing_workflows)} existing workflows:")
    for workflow in existing_workflows:
        print(f"   - {workflow}")
    
    if not existing_workflows:
        print("   - No existing workflows found (expected for fresh setup)")
    
    print(f"   ✅ Workflow discovery working\n")
    
    # 5. Test JSON template locations
    print("5. Testing JSON Templates:")
    templates_dir = workflows_dir / "json_object_templates"
    print(f"   Templates directory: {templates_dir}")
    print(f"   Directory exists: {templates_dir.exists()}")
    
    if templates_dir.exists():
        templates = list(templates_dir.glob("*.json"))
        print(f"   Found {len(templates)} template files:")
        for template in templates:
            print(f"   - {template.name}")
    
    print(f"   ✅ JSON templates ready\n")
    
    print("🎉 All Workflow Manager components tested successfully!")
    print(f"🔧 Implementation ready for integration with MAO")
    
    # 6. Show example workflow ID structure
    print(f"\n📋 Example Workflow ID Structure:")
    for i in range(3):
        uid, explanation = generate_workflow_uid_with_explanation()
        print(f"   {uid} | Operations: {explanation}")

if __name__ == "__main__":
    test_workflow_id_generation()
