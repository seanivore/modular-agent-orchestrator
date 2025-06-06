#!/bin/bash

# SFA workflow for modulation
# Generated from script-modulation-improved-config.json

echo "Running modulation workflow with 1 phases..."

CONFIG_FILE="/Users/seanivore/Development/single-file-agents/use-case/bland-ai-research/script-modulation-improved-config.json"
SFA_SCRIPT="/Users/seanivore/Development/single-file-agents/sfa_agent.py"

# Run each phase in sequence
echo "Phase 1 of 1"
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

echo "modulation workflow completed successfully!"
