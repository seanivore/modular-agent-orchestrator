#!/bin/bash

# SFA workflow for content
# Generated from doc-content-plan-config.json

echo "Running content workflow with 3 phases..."

CONFIG_FILE="/Users/seanivore/Development/single-file-agents/use-case/doc-content-plan/doc-content-plan-config.json"
SFA_SCRIPT="/Users/seanivore/Development/single-file-agents/sfa_agent.py"

# Run each phase in sequence
echo "Phase 1 of 3"
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

echo "Phase 2 of 3"
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

echo "Phase 3 of 3"
if command -v uv &> /dev/null; then
    uv run "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 2
else
    python3 "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 2
fi
if [ $? -ne 0 ]; then
    echo "Error in phase 3"
    exit 1
fi
echo "Phase 3 completed"
echo

echo "content workflow completed successfully!"
