#!/bin/bash

# SFA workflow for me
# Generated from job-me-up-config.json

# Check if arguments were provided
if [ $# -eq 0 ]; then
    # No arguments provided, use the default arguments from config
    ARGS="me up"
else
    # Use the provided arguments
    ARGS="$@"
fi

echo "Running me workflow with args: $ARGS"

CONFIG_FILE="/Users/seanivore/Development/single-file-agents/use-case/job-me-up/job-me-up-config.json"
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
PARENT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
SFA_WORKFLOW="$PARENT_DIR/setup-scripts/sfa_workflow.sh"

# Run the workflow in execute mode
exec "$SFA_WORKFLOW" -e "$CONFIG_FILE"
