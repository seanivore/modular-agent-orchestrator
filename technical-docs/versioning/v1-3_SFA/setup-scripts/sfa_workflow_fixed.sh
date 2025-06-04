#!/bin/bash
# SFA Workflow - Unified script for both setup and execution
# Usage: sfa_workflow.sh [options] <config_file.json>

# Function to show usage
show_usage() {
    echo "Usage: sfa [options] <config_file.json>"
    echo ""
    echo "Options:"
    echo "  -e, --execute       Only execute the workflow without setup (default: setup and create command)"
    echo "  -r, --readme        Create an additional README_v2.md with detailed workflow documentation"
    echo "  -m, --model         Specify a model for execution"
    echo "  -h, --help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  sfa config.json            Setup workflow and create command (default)"
    echo "  sfa -e config.json         Execute workflow without setup"
    echo "  sfa -r config.json         Setup workflow and create detailed README"
    exit 1
}

# Default options
EXECUTE_ONLY=false
CREATE_DETAILED_README=false
MODEL=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -e|--execute)
            EXECUTE_ONLY=true
            shift
            ;;
        -r|--readme)
            CREATE_DETAILED_README=true
            shift
            ;;
        -m|--model)
            MODEL="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            ;;
        *)
            # If it's not an option, assume it's the config file
            if [[ -z "$CONFIG_FILE