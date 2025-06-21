#!/bin/bash
# Install script for the enhanced project tree command

# Set paths
BIN_DIR="${HOME}/bin"

# Create bin directory if it doesn't exist
mkdir -p "$BIN_DIR"

# Backup existing ptree if it exists
if [ -f "${BIN_DIR}/ptree" ]; then
    echo "Backing up existing ptree to ptree.backup..."
    cp "${BIN_DIR}/ptree" "${BIN_DIR}/ptree.backup"
fi

# Save the enhanced ptree script to bin directory
echo "Creating enhanced ptree command in ${BIN_DIR}..."
cat > "${BIN_DIR}/ptree" << 'EOF'
#!/bin/bash
# Enhanced project tree with hidden file control
# Usage: ptree [options]

show_help() {
    echo "ptree - Enhanced project tree viewer"
    echo ""
    echo "Usage:"
    echo "  ptree           Show normal tree (default behavior)"
    echo "  ptree -a        Show ALL hidden files and directories"
    echo "  ptree -s        Show SELECT hidden files (.claude, .cursor, .notes, etc.)"
    echo "  ptree -h        Show this help"
    echo ""
    echo "Examples:"
    echo "  ptree           # Normal tree, no hidden files"
    echo "  ptree -a        # Include all hidden files"
    echo "  ptree -s        # Show only important hidden files"
}

show_normal_tree() {
    echo "Project Structure (excluding hidden files):"
    echo "=========================================="
    tree -C -I "node_modules|target|venv|.git|.*" --prune
}

show_selective_hidden() {
    echo "Project Structure (with select hidden files):"
    echo "============================================="
    
    # Show integrated tree with select hidden directories included
    # Exclude common junk but include important hidden dirs
    tree -C -I "node_modules|target|venv|.git|.DS_Store|.cache|.npm|.yarn|.pytest_cache|.mypy_cache|.tox|.coverage|.nyc_output|.env.local|.env.*.local|*.log|.parcel-cache" --prune -a | \
    grep -v -E "^\.[^/.]*$|^\.[^/]*\..*$" | \
    grep -E -v "^\.(bash_|zsh_|ssh|aws|docker|gem|npm|pip|conda|cargo|rustup)" || \
    
    # Fallback: show normal tree plus important hidden items
    {
        tree -C -I "node_modules|target|venv|.git|.*" --prune
        
        # Add important hidden directories inline-style
        for dir in .claude .cursor .vscode .idea .notes .drafts .planning .ai.dev-resources; do
            if [ -d "$dir" ]; then
                echo ""
                echo "├── $dir/"
                tree -C "$dir" | sed 's/^/│   /'
            fi
        done
        
        # Add important hidden files
        for file in .gitignore .env .env.example .aider.conf.yml .cursorrules .claude_context; do
            if [ -f "$file" ]; then
                echo "├── $file"
            fi
        done
    }
}

show_all_hidden() {
    echo "Project Structure (including ALL hidden files):"
    echo "==============================================="
    tree -C -I "node_modules|target|venv" --prune -a
}

# Parse command line arguments
case "${1:-}" in
    -h|--help|help)
        show_help
        ;;
    -a|--all)
        show_all_hidden
        ;;
    -s|--select)
        show_selective_hidden
        ;;
    "")
        show_normal_tree
        ;;
    *)
        echo "Unknown option: $1"
        echo "Use 'ptree -h' for help"
        exit 1
        ;;
esac
EOF

# Make the ptree command executable
chmod +x "${BIN_DIR}/ptree"

# Success message
echo "Enhanced ptree installed!"
echo "- 'ptree' command updated in ${BIN_DIR}"
echo "- Previous version backed up as ptree.backup"
echo ""
echo "You can now use the enhanced ptree command:"
echo "  ptree           Show normal tree (no hidden files)"
echo "  ptree -a        Show ALL hidden files"
echo "  ptree -s        Show SELECT hidden files (.claude, .cursor, etc.)"
echo "  ptree -h        Show help"
echo ""
echo "Perfect for viewing .claude directories without manual unhiding!" 