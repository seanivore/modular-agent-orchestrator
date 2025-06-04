#!/bin/bash
# Test script for verifying tool functionality
# This script creates test files and runs the agent to test various features

set -e  # Exit on error

PARENT_DIR="$(dirname "$(dirname "$(dirname "$(readlink -f "$0")")")")"
SFA_SCRIPT="${PARENT_DIR}/sfa_main.py"
TOOLS_DIR="${PARENT_DIR}/tools"
TEST_DIR="${PARENT_DIR}/use-case/tag-content/test"

# Create test directory if it doesn't exist
mkdir -p $TEST_DIR

echo "Setting up test environment..."

# Check for required dependencies
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required but not found"
    exit 1
fi

# Create test files
echo "Creating test files..."

# 1. Create a small test file
cat > $TEST_DIR/small_file.md << EOF
# Small Test File

This is a small test file with minimal content.
EOF

# 2. Create a medium-sized test file
cat > $TEST_DIR/medium_file.md << EOF
# Medium Test File

$(for i in {1..100}; do echo "This is line $i of the medium test file."; done)

## Section 2

$(for i in {1..100}; do echo "More content for testing purposes - line $i."; done)
EOF

# 3. Create a large test file (approximately 10k tokens)
cat > $TEST_DIR/large_file.md << EOF
# Large Test File

$(for i in {1..500}; do echo "This is paragraph $i of the large test file. It contains multiple sentences to increase token count. Each paragraph should take up a reasonable amount of tokens to test the system's ability to handle large files. We want to ensure that our safety mechanisms for file editing work correctly."; done)
EOF

# Create a test config file
cat > $TEST_DIR/test-config.json << EOF
{
  "test-workflow.sh": {
    "TASK_1": [
      {
        "S": ["${PARENT_DIR}/sfa_main.py"],
        "U": "You are a helpful assistant for testing file editing capabilities.",
        "X": "This is a test workflow to verify the text_editor tool functionality and other features. Please perform the following tasks: 1) Read the small_file.md and add a new line at the end, 2) Edit medium_file.md to add a front matter section at the top, 3) Try to edit large_file.md - this should trigger the safety features. Finally, add a summary of your findings.",
        "X_PATH": ["${TEST_DIR}/small_file.md", "${TEST_DIR}/medium_file.md", "${TEST_DIR}/large_file.md"],
        "Y": "After completing these tasks, use workflow_adjustment to add a new phase, and then in the new phase create a summary report of all the tests you performed.",
        "Y_PATH": [],
        "Z": "Test results and observations",
        "O": ["${TEST_DIR}/test_results.md"]
      }
    ],
    "TASK_2": [
      {
        "S": ["${PARENT_DIR}/sfa_main.py"],
        "U": "You are a helpful assistant for testing workflow phase transitions.",
        "X": "This is the second phase of the test. Review what you did in the first phase and create a summary report of all tests performed, results observed, and any issues encountered.",
        "X_PATH": ["${TEST_DIR}/small_file.md", "${TEST_DIR}/medium_file.md", "${TEST_DIR}/large_file.md"],
        "Y": "Be sure to mention any warnings or errors encountered during the tests, especially with large files.",
        "Y_PATH": [],
        "Z": "Test summary report",
        "O": ["${TEST_DIR}/test_summary.md"]
      }
    ]
  },
  "A": "test-workflow",
  "F": "${TEST_DIR}/"
}
EOF

echo "Test environment setup complete."
echo "To run the test, use the command: python3 $SFA_SCRIPT --config-file $TEST_DIR/test-config.json --phase 0"
echo "After phase 0 completes, run: python3 $SFA_SCRIPT --config-file $TEST_DIR/test-config.json --phase 1" 