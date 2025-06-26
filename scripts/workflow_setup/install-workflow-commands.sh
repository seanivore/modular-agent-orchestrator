#!/bin/bash
# Install workflow command-line tools

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

# Create update command for workflow modifications
UPDATE_CMD="$BIN_DIR/update"
echo "Installing update command..."
cat > "$UPDATE_CMD" << EOF
#!/bin/bash
# Mao Workflow Update Command

echo "🚧 Workflow update functionality coming soon!"
echo "This will allow dynamic workflow modification during execution"
echo ""
echo "Planned usage: update ./phase.json"
echo "Planned usage: mao --update ./phase.json"
echo "Planned usage: /update ./phase.json"
EOF

chmod +x "$UPDATE_CMD"

# Create fix-it command for deliverable improvements
FIXIT_CMD="$BIN_DIR/fix-it"
echo "Installing fix-it command..."
cat > "$FIXIT_CMD" << EOF
#!/bin/bash
# Mao Workflow Fix-It Command

echo "🚧 Workflow fix-it functionality coming soon!"
echo "This will allow fixing subpar deliverables during workflow execution"
echo ""
echo "Planned usage: fix-it ./fix.json"
echo "Planned usage: mao --fix-it ./fix.json"
echo "Planned usage: /fix-it ./fix.json"
EOF

chmod +x "$FIXIT_CMD"

echo "Mao workflow commands installed successfully!"
echo ""
echo "Available commands:"
echo "  setup <temp_directory_path>    - Create workflow from temp JSON files"
echo "  update <phase.json>           - Update workflow during execution (coming soon)"
echo "  fix-it <fix.json>             - Fix deliverables during workflow (coming soon)"
echo ""
echo "Examples:"
echo "  setup ./configs/workflows/.temp/market-research/"
echo "  update ./new-phase.json"
echo "  fix-it ./fix-deliverable.json"
echo ""
echo "Make sure your shell's PATH includes $BIN_DIR"
echo "You may need to restart your terminal or run 'source ~/.bashrc' (or ~/.zshrc)"
