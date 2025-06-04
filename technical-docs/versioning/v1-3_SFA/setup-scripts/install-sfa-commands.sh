#!/bin/bash
# Install SFA command-line tools

# Get the base directory
BASE_DIR="$(dirname "$(readlink -f "$0")")"
WORKFLOW_SCRIPT="$BASE_DIR/sfa_workflow.sh"
BIN_DIR="$(cd ~ && pwd)/bin"

# Check if the script exists
if [ ! -f "$WORKFLOW_SCRIPT" ]; then
    echo "Error: Workflow script not found at $WORKFLOW_SCRIPT"
    exit 1
fi

# Make sure workflow script is executable
chmod +x "$WORKFLOW_SCRIPT"

# Create ~/bin if it doesn't exist
if [ ! -d "$BIN_DIR" ]; then
    echo "Creating $BIN_DIR directory..."
    mkdir -p "$BIN_DIR"
fi

# Add ~/bin to PATH if not already
if ! [[ ":$PATH:" == *":$BIN_DIR:"* ]]; then
    echo "Adding $BIN_DIR to PATH..."
    HOME_DIR="$(cd ~ && pwd)"
    echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME_DIR/.bashrc"
    echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME_DIR/.zshrc"
fi

# Create sfa command
SFA_CMD="$BIN_DIR/sfa"
echo "Installing sfa command..."
cat > "$SFA_CMD" << EOF
#!/bin/bash
# SFA - Single-File Agent Command

# Use the actual SFA directory path from installation
SFA_DIR="$(dirname "$BASE_DIR")"

# Default path to workflow script
WORKFLOW_SCRIPT="\${SFA_DIR}/setup-scripts/sfa_workflow.sh"

# Check if the workflow script exists
if [ ! -f "\$WORKFLOW_SCRIPT" ]; then
    echo "Error: Workflow script not found at \$WORKFLOW_SCRIPT"
    echo "Please ensure the path is correct or reinstall SFA"
    exit 1
fi

# Show usage if no arguments provided
if [ \$# -lt 1 ]; then
    echo "Usage: sfa [options] <config_file.json>"
    echo ""
    echo "Options:"
    echo "  -e, --execute       Only execute the workflow without setup"
    echo "  -r, --readme        Create an additional README_v2.md with detailed documentation"
    echo "  -h, --help          Show this help message"
    exit 1
fi

# Pass all arguments to the workflow script
exec "\$WORKFLOW_SCRIPT" "\$@"
EOF

chmod +x "$SFA_CMD"

echo "SFA commands installed successfully!"
echo ""
echo "Usage:"
echo "  sfa [options] <config_file.json>"
echo ""
echo "Options:"
echo "  -e, --execute       Only execute the workflow without setup"
echo "  -r, --readme        Create an additional README_v2.md with detailed documentation"
echo "  -h, --help          Show this help message"
echo ""
echo "Make sure your shell's PATH includes $BIN_DIR"
echo "You may need to restart your terminal or run 'source ~/.bashrc' (or ~/.zshrc)"