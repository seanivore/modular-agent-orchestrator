#!/bin/bash

# SFA workflow for write
# Generated from doc-write-best-config.json

echo "Running write workflow with 2 phases..."

CONFIG_FILE="/Users/seanivore/Development/single-file-agents/use-case/doc-write-best/doc-write-best-config.json"
SFA_SCRIPT="/Users/seanivore/Development/single-file-agents/sfa_write_review_agent.py"

# Run each phase in sequence
echo "Phase 1 of 2"
if command -v uv &> /dev/null; then
    uv run "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 0
else
    python3 "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 0
fi
if [ $? -ne 0 ]; then
    echo "Error in phase 1"
    exit 1
fi
echo "Phase 1 completed"
echo

echo "Phase 2 of 2"
if command -v uv &> /dev/null; then
    uv run "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 1
else
    python3 "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 1
fi
if [ $? -ne 0 ]; then
    echo "Error in phase 2"
    exit 1
fi
echo "Phase 2 completed"
echo

echo "write workflow completed successfully!"
