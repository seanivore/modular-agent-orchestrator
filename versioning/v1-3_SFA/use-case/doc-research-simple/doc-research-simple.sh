#!/bin/bash

# SFA workflow for research
# Generated from doc-research-simple-config.json

echo "Running research workflow with 15 phases..."

CONFIG_FILE="/Users/seanivore/Development/single-file-agents/use-case/doc-research-simple/doc-research-simple-config.json"
SFA_SCRIPT="/Users/seanivore/Development/single-file-agents/sfa_write_review_agent.py"

# Run each phase in sequence
echo "Phase 1 of 15"
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

echo "Phase 2 of 15"
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

echo "Phase 3 of 15"
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

echo "Phase 4 of 15"
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

echo "Phase 5 of 15"
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

echo "Phase 6 of 15"
if command -v uv &> /dev/null; then
    uv run "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 5
else
    python3 "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 5
fi
if [ $? -ne 0 ]; then
    echo "Error in phase 6"
    exit 1
fi
echo "Phase 6 completed"
echo

echo "Phase 7 of 15"
if command -v uv &> /dev/null; then
    uv run "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 6
else
    python3 "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 6
fi
if [ $? -ne 0 ]; then
    echo "Error in phase 7"
    exit 1
fi
echo "Phase 7 completed"
echo

echo "Phase 8 of 15"
if command -v uv &> /dev/null; then
    uv run "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 7
else
    python3 "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 7
fi
if [ $? -ne 0 ]; then
    echo "Error in phase 8"
    exit 1
fi
echo "Phase 8 completed"
echo

echo "Phase 9 of 15"
if command -v uv &> /dev/null; then
    uv run "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 8
else
    python3 "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 8
fi
if [ $? -ne 0 ]; then
    echo "Error in phase 9"
    exit 1
fi
echo "Phase 9 completed"
echo

echo "Phase 10 of 15"
if command -v uv &> /dev/null; then
    uv run "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 9
else
    python3 "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 9
fi
if [ $? -ne 0 ]; then
    echo "Error in phase 10"
    exit 1
fi
echo "Phase 10 completed"
echo

echo "Phase 11 of 15"
if command -v uv &> /dev/null; then
    uv run "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 10
else
    python3 "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 10
fi
if [ $? -ne 0 ]; then
    echo "Error in phase 11"
    exit 1
fi
echo "Phase 11 completed"
echo

echo "Phase 12 of 15"
if command -v uv &> /dev/null; then
    uv run "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 11
else
    python3 "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 11
fi
if [ $? -ne 0 ]; then
    echo "Error in phase 12"
    exit 1
fi
echo "Phase 12 completed"
echo

echo "Phase 13 of 15"
if command -v uv &> /dev/null; then
    uv run "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 12
else
    python3 "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 12
fi
if [ $? -ne 0 ]; then
    echo "Error in phase 13"
    exit 1
fi
echo "Phase 13 completed"
echo

echo "Phase 14 of 15"
if command -v uv &> /dev/null; then
    uv run "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 13
else
    python3 "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 13
fi
if [ $? -ne 0 ]; then
    echo "Error in phase 14"
    exit 1
fi
echo "Phase 14 completed"
echo

echo "Phase 15 of 15"
if command -v uv &> /dev/null; then
    uv run "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 14
else
    python3 "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase 14
fi
if [ $? -ne 0 ]; then
    echo "Error in phase 15"
    exit 1
fi
echo "Phase 15 completed"
echo

echo "research workflow completed successfully!"
