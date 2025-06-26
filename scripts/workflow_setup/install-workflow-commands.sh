#!/bin/bash
# Install Mao workflow command-line tools

# Get the base directory
BASE_DIR="$(dirname "$(readlink -f "$0")")"
WORKFLOW_SCRIPT="$BASE_DIR/workflow_setup.sh"
BIN_DIR="$(cd ~ && pwd)/bin"

# Check if the script exists
if [ ! -f "$WORKFLOW_SCRIPT" ]; then
    echo "Error: Workflow setup script not found at $WORKFLOW_SCRIPT"
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

# Create setup command
SETUP_CMD="$BIN_DIR/setup"
echo "Installing setup command..."
cat > "$SETUP_CMD" << EOF
#!/bin/bash
# Mao Workflow Setup Command

# Use the actual Mao directory path from installation
MAO_DIR="$(dirname "$(dirname "$BASE_DIR")")"

# Default path to workflow setup script
WORKFLOW_SCRIPT="\${MAO_DIR}/scripts/workflow_setup/workflow_setup.sh"

# Check if the workflow setup script exists
if [ ! -f "\$WORKFLOW_SCRIPT" ]; then
    echo "Error: Workflow setup script not found at \$WORKFLOW_SCRIPT"
    echo "Please ensure the path is correct or reinstall Mao workflow tools"
    exit 1
fi

# Show usage if no arguments provided
if [ \$# -lt 1 ]; then
    echo "Usage: setup <temp_directory_path>"
    echo ""
    echo "Examples:"
    echo "  setup ./configs/workflows/.temp/market-research/"
    echo "  setup /absolute/path/to/.temp/workflow-name/"
    echo ""
    echo "The temp directory should contain workflow, phase, and handoff JSON files"
    exit 1
fi

# Pass all arguments to the workflow setup script
exec "\$WORKFLOW_SCRIPT" "\$@"
EOF

chmod +x "$SETUP_CMD"

echo "Mao workflow commands installed successfully!"
echo ""
echo "Usage:"
echo "  setup <temp_directory_path>"
echo ""
echo "Examples:"
echo "  setup ./configs/workflows/.temp/market-research/"
echo "  setup /absolute/path/to/.temp/workflow-name/"
echo ""
echo "Make sure your shell's PATH includes $BIN_DIR"
echo "You may need to restart your terminal or run 'source ~/.bashrc' (or ~/.zshrc)"
