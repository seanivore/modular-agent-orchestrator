#!/bin/bash
# Mao Terminal Interface Implementation
# This is the actual implementation script

# Get the absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LAUNCHER_PATH="$PROJECT_DIR/mao_v4.py"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Launch Mao with all arguments passed through
python3 "$LAUNCHER_PATH" "$@"