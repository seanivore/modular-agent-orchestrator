#!/bin/bash

# SFA workflow for combine
# Generated from research-combine-report-config.json

echo "Running combine workflow with 5 phases..."

CONFIG_FILE="/Users/seanivore/Development/single-file-agents/use-case/research-combine-report/research-combine-report-config.json"
SFA_SCRIPT="/Users/seanivore/Development/single-file-agents/sfa_agent.py"

# Run each phase in sequence
echo "Phase 1 of 5"
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

echo "Phase 2 of 5"
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

echo "Phase 3 of 5"
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

echo "Phase 4 of 5"
if command -v uv &> /dev/null; then
    uv run "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 3
else
    python3 "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 3
fi
if [ $? -ne 0 ]; then
    echo "Error in phase 4"
    exit 1
fi
echo "Phase 4 completed"
echo

echo "Phase 5 of 5"
if command -v uv &> /dev/null; then
    uv run "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 4
else
    python3 "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 4
fi
if [ $? -ne 0 ]; then
    echo "Error in phase 5"
    exit 1
fi
echo "Phase 5 completed"
echo

echo "combine workflow completed successfully!"
