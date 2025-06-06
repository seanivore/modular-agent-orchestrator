#!/bin/bash
# Script to migrate from old workflow scripts to the new unified workflow

echo "Migrating workflow scripts to the new unified system..."

# Get script directory
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
DEPRECATED_DIR="${PARENT_DIR}/deprecated/2025-5-UNIFIED-WORKFLOW"

# Create the deprecated directory if it doesn't exist
mkdir -p "$DEPRECATED_DIR"

# Move old scripts to deprecated directory
echo "Moving old workflow scripts to $DEPRECATED_DIR..."

# Check if files exist before attempting to move them
if [ -f "$SCRIPT_DIR/setup-sfa-workflow.sh" ]; then
    cp "$SCRIPT_DIR/setup-sfa-workflow.sh" "$DEPRECATED_DIR/"
    echo "- Copied setup-sfa-workflow.sh to deprecated directory"
fi

if [ -f "$SCRIPT_DIR/branching_workflow.sh" ]; then
    cp "$SCRIPT_DIR/branching_workflow.sh" "$DEPRECATED_DIR/"
    echo "- Copied branching_workflow.sh to deprecated directory"
fi

# Update the sfa command to use the new script
SFA_COMMAND="$HOME/bin/sfa"
if [ -f "$SFA_COMMAND" ]; then
    echo "Updating sfa command to use the new unified workflow script..."
    # Create backup of original sfa command
    cp "$SFA_COMMAND" "$DEPRECATED_DIR/sfa.orig"
    echo "- Created backup of original sfa command"
    
    # Update the sfa command
    cat > "$SFA_COMMAND" << 'EOF'
#!/bin/bash
# SFA - Single-File Agent Command

# Get this script's path
SFA_COMMAND_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
# Get the Development directory (parent of parent of bin)
DEV_DIR="$(dirname "$(dirname "$SFA_COMMAND_PATH")")"
# Path to SFA directory
SFA_DIR="$DEV_DIR/single-file-agents"

# Default path to workflow script
WORKFLOW_SCRIPT="${SFA_DIR}/setup-scripts/sfa_workflow.sh"

# Check if the workflow script exists
if [ ! -f "$WORKFLOW_SCRIPT" ]; then
    echo "Error: Workflow script not found at $WORKFLOW_SCRIPT"
    echo "Please ensure the path is correct or reinstall SFA"
    exit 1
fi

# Show usage if no arguments provided
if [ $# -lt 1 ]; then
    echo "Usage: sfa [options] <config_file.json>"
    echo ""
    echo "Options:"
    echo "  -e, --execute       Only execute the workflow without setup"
    echo "  -r, --readme        Create an additional README_v2.md with detailed documentation"
    echo "  -h, --help          Show this help message"
    exit 1
fi

# Pass all arguments to the workflow script
exec "$WORKFLOW_SCRIPT" "$@"
EOF
    chmod +x "$SFA_COMMAND"
    echo "sfa command updated successfully"
else
    echo "sfa command not found at $SFA_COMMAND. No updates made."
    echo "To create the sfa command, run:"
    echo "  ln -sf \"${SCRIPT_DIR}/sfa_workflow.sh\" \"$HOME/bin/sfa\""
fi

echo "Migration complete. The new unified workflow script is ready to use."
echo ""
echo "Usage examples:"
echo "  sfa config.json            # Setup workflow and create command (default)"
echo "  sfa -e config.json         # Execute workflow without setup"
echo "  sfa -r config.json         # Setup workflow and create detailed README" 