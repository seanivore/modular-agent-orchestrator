#!/bin/bash
# Test for agent file selection logic in sfa_workflow.sh

echo "=== Testing agent file selection logic ==="

# Get the current directory
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
PARENT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
echo "Parent directory: $PARENT_DIR"

# Create temporary directory for tests
TEMP_DIR="${SCRIPT_DIR}/temp"
mkdir -p "$TEMP_DIR"

# Create test configuration file
TEST_CONFIG="${TEMP_DIR}/test_config.json"
cat > "$TEST_CONFIG" << EOF
{
  "A": "test-command",
  "F": "${TEMP_DIR}",
  "M": "google/gemini-2.5-pro-exp-03-25",
  "test": [
    {
      "PHASE_0": [{
        "U": "You are a test assistant",
        "X": "This is a test"
      }]
    }
  ]
}
EOF

# Modify the workflow script to output debug information
WORKFLOW_SCRIPT="${PARENT_DIR}/setup-scripts/sfa_workflow.sh"
TEST_WORKFLOW_SCRIPT="${TEMP_DIR}/test_workflow.sh"

echo "Original workflow script: $WORKFLOW_SCRIPT"
if [ ! -f "$WORKFLOW_SCRIPT" ]; then
    echo "ERROR: Workflow script not found: $WORKFLOW_SCRIPT"
    exit 1
fi

# Make a copy of the workflow script with debug info added
cat "$WORKFLOW_SCRIPT" | sed 's/^AGENT_FILE=.*$/AGENT_FILE="$AGENT_FILE"; echo "DEBUG: Selected agent file: $AGENT_FILE"/' > "$TEST_WORKFLOW_SCRIPT"
chmod +x "$TEST_WORKFLOW_SCRIPT"

# Function to test agent file selection
test_file_selection() {
    echo -e "\n--- Testing with available files: $1 ---"
    
    # Create a mock python script that just echoes the command
    MOCK_DIR="${TEMP_DIR}/mock_bin"
    mkdir -p "$MOCK_DIR"
    
    cat > "${MOCK_DIR}/python3" << 'EOF'
#!/bin/bash
echo "MOCK PYTHON CALL: $@"
exit 0
EOF
    chmod +x "${MOCK_DIR}/python3"
    
    # Remove any existing test files
    find "$PARENT_DIR" -maxdepth 1 -name "sfa_v*_main.py" -exec rm {} \;
    
    # Create the specified agent files
    IFS=',' read -ra FILES <<< "$1"
    for file in "${FILES[@]}"; do
        touch "${PARENT_DIR}/${file}"
        echo "Created test file: ${PARENT_DIR}/${file}"
    done
    
    # List files to verify
    echo "Current agent files in directory:"
    find "$PARENT_DIR" -maxdepth 1 -name "sfa_v*_main.py" | sort
    
    # Run the test workflow script
    echo "Running test workflow script..."
    PATH="${MOCK_DIR}:$PATH" bash "$TEST_WORKFLOW_SCRIPT" --config-file "$TEST_CONFIG"
    
    # Show the result
    echo "Test result: $?"
}

# Test with various combinations of available agent files
echo "Running agent file selection tests with debug output..."

# Test 1: Only v3_3_0 available
test_file_selection "sfa_v3_3_0_main.py"

# Test 2: Multiple versions available
test_file_selection "sfa_v3_2_0_main.py,sfa_v3_3_0_main.py"

# Test 3: Only older version available
test_file_selection "sfa_v3_2_0_main.py"

# Test 4: No version available (should fail)
test_file_selection ""

# Cleanup
echo -e "\nCleaning up test files..."
rm -rf "$TEMP_DIR"
find "$PARENT_DIR" -maxdepth 1 -name "sfa_v*_main.py.test" -exec rm {} \;

echo "=== Agent file selection tests completed ===" 