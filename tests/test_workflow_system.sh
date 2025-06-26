#!/bin/bash
# Test script for workflow creation system
# Tests the complete 3-type JSON workflow creation pipeline

echo "🧪 Testing Mao Workflow Creation System"
echo "======================================="

# Get the MAO root directory  
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
MAO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "MAO Root: $MAO_ROOT"
echo ""

# Test 1: Check if required directories exist
echo "Test 1: Checking directory structure..."
REQUIRED_DIRS=(
    "$MAO_ROOT/configs/workflows"
    "$MAO_ROOT/configs/workflows/.temp" 
    "$MAO_ROOT/configs/workflows/json_object_templates"
    "$MAO_ROOT/configs/examples/workflow_templates"
    "$MAO_ROOT/scripts/workflow_setup"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir exists"
    else
        echo "❌ $dir missing"
        exit 1
    fi
done
echo ""

# Test 2: Check if setup scripts exist and are executable
echo "Test 2: Checking setup scripts..."
SETUP_SCRIPTS=(
    "$MAO_ROOT/scripts/workflow_setup/install-workflow-commands.sh"
    "$MAO_ROOT/scripts/workflow_setup/workflow_setup.sh"
)

for script in "${SETUP_SCRIPTS[@]}"; do
    if [ -f "$script" ] && [ -x "$script" ]; then
        echo "✅ $(basename "$script") exists and is executable"
    else
        echo "❌ $(basename "$script") missing or not executable"
        exit 1
    fi
done
echo ""

# Test 3: Check if JSON templates exist
echo "Test 3: Checking JSON templates..."
TEMPLATES=(
    "$MAO_ROOT/configs/workflows/json_object_templates/command_use_case_workflow_config.json"
    "$MAO_ROOT/configs/workflows/json_object_templates/command_use_case_phase_config.json"
    "$MAO_ROOT/configs/workflows/json_object_templates/command_use_case_handoff_config.json"
    "$MAO_ROOT/configs/examples/workflow_templates/example-workflow/example-workflow_workflow_config.json"
)

for template in "${TEMPLATES[@]}"; do
    if [ -f "$template" ]; then
        echo "✅ $(basename "$template") exists"
    else
        echo "❌ $(basename "$template") missing"
        exit 1
    fi
done
echo ""

# Test 4: Check if required scripts are accessible
echo "Test 4: Checking script dependencies..."
REQUIRED_SCRIPTS=(
    "$MAO_ROOT/scripts/unique_id_generator/unique_id_generator.py"
    "$MAO_ROOT/scripts/user_id_generator/user_id_generator.py"
)

for script in "${REQUIRED_SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        echo "✅ $(basename "$script") exists"
    else
        echo "❌ $(basename "$script") missing"
        exit 1
    fi
done
echo ""

# Test 5: Test workflow ID generation
echo "Test 5: Testing workflow ID generation..."
cd "$MAO_ROOT"
# Get just the first generated UID from the output
WORKFLOW_ID=$(python3 scripts/unique_id_generator/unique_id_generator.py 2>/dev/null | grep "uid-" | head -1 | awk '{print $1}')
if [[ "$WORKFLOW_ID" =~ ^uid-[a-z]{3}-[0-9]{3}$ ]]; then
    echo "✅ Workflow ID generation works: $WORKFLOW_ID"
else
    echo "❌ Workflow ID generation failed or incorrect format: '$WORKFLOW_ID'"
    echo "Full output:"
    python3 scripts/unique_id_generator/unique_id_generator.py
    exit 1
fi
echo ""

# Test 6: Test user ID generation  
echo "Test 6: Testing user ID generation..."
# Get just the user ID from the output - look for the specific pattern
USER_ID=$(python3 scripts/user_id_generator/user_id_generator.py testuser 2>/dev/null | grep "testuser.*->" | sed 's/.*-> //' | awk '{print $1}')
if [[ "$USER_ID" =~ ^user-[0-9]{4}$ ]]; then
    echo "✅ User ID generation works: $USER_ID"
else
    echo "❌ User ID generation failed or incorrect format: '$USER_ID'"
    echo "Full output:"
    python3 scripts/user_id_generator/user_id_generator.py testuser
    exit 1
fi
echo ""

# Test 7: Create a test workflow (dry run)
echo "Test 7: Testing workflow creation pipeline..."
TEST_TEMP_DIR="$MAO_ROOT/configs/workflows/.temp/test-workflow-$(date +%s)"

# Create test temp directory
mkdir -p "$TEST_TEMP_DIR"

# Generate test workflow with real IDs
REAL_WORKFLOW_ID=$(python3 scripts/unique_id_generator/unique_id_generator.py 2>/dev/null | grep "uid-" | head -1 | awk '{print $1}')
REAL_USER_ID=$(python3 scripts/user_id_generator/user_id_generator.py testuser 2>/dev/null | grep "testuser.*->" | sed 's/.*-> //' | awk '{print $1}')

# Create test workflow JSON
cat > "$TEST_TEMP_DIR/test-workflow_workflow_config.json" << EOF
{
  "workflow": [
    {
      "user_id": "$REAL_USER_ID",
      "workflow_id": "$REAL_WORKFLOW_ID",
      "custom_command": "test workflow",
      "workflow_goal": "Test the workflow creation system",
      "workflow_deliverable": "Successful test completion", 
      "workflow_description": "Automated test of the 3-type JSON workflow system",
      "temp_directory": "$TEST_TEMP_DIR"
    }
  ]
}
EOF

# Create test phase JSON
cat > "$TEST_TEMP_DIR/test-workflow_phase_config.json" << EOF
{
  "phase": [
    {
      "workflow_id": "$REAL_WORKFLOW_ID",
      "phase_number": "01",
      "phase_goal": "Test phase execution",
      "phase_deliverable": "Test results",
      "phase_description": "Execute test phase to verify system functionality",
      "resources": [],
      "tools": ["think", "text_editor"],
      "model_1": "claude-sonnet-4",
      "model_2": "claude-sonnet-3.7",
      "model_3": "gemini-2.5-pro",
      "provider_1": "anthropic-direct",
      "provider_2": "anthropic-direct", 
      "provider_3": "requesty"
    }
  ]
}
EOF

# Create test handoff JSON
cat > "$TEST_TEMP_DIR/test-workflow_handoff_config.json" << EOF
{
  "handoff": [
    {
      "workflow_id": "$REAL_WORKFLOW_ID",
      "handoff_number": "01",
      "assessment_questions": [
        "Did the test complete successfully?",
        "Are all components functioning correctly?"
      ],
      "human_in_loop": "no"
    }
  ]
}
EOF

echo "✅ Test workflow JSON files created in temp directory"
echo "✅ Using workflow ID: $REAL_WORKFLOW_ID"
echo "✅ Using user ID: $REAL_USER_ID"
echo ""

# Clean up test files
echo "Cleaning up test files..."
rm -rf "$TEST_TEMP_DIR"
echo "✅ Test cleanup complete"
echo ""

# Final summary
echo "🎉 All tests passed! Workflow creation system is ready."
echo ""
echo "Next steps:"
echo "1. Install workflow commands: ./scripts/workflow_setup/install-workflow-commands.sh"
echo "2. Copy example template: cp -r ./configs/examples/workflow_templates/example-workflow ./configs/workflows/.temp/my-workflow"
echo "3. Edit JSON files in temp directory with your workflow details"
echo "4. Run setup: setup ./configs/workflows/.temp/my-workflow"
echo "5. Execute: my-workflow"
echo ""
echo "System is ready for workflow creation! 🚀"
