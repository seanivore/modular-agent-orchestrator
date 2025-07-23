#!/bin/bash
# MAO Import Tools Installation Script
# Installs audit and fixer tools as global commands

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Installing MAO Import Tools...${NC}"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Make scripts executable
chmod +x "$SCRIPT_DIR/import_audit.py"
chmod +x "$SCRIPT_DIR/import_fixer.py"

echo -e "${GREEN}✅ Made scripts executable${NC}"

# Create wrapper scripts in a bin directory
BIN_DIR="$PROJECT_ROOT/bin"
mkdir -p "$BIN_DIR"

# Create audit wrapper
cat > "$BIN_DIR/mao-audit-imports" << EOF
#!/bin/bash
# MAO Import Audit Tool
cd "$PROJECT_ROOT"
python "$SCRIPT_DIR/import_audit.py" "\$@"
EOF

# Create fixer wrapper  
cat > "$BIN_DIR/mao-fix-imports" << EOF
#!/bin/bash
# MAO Import Fixer Tool
cd "$PROJECT_ROOT"
python "$SCRIPT_DIR/import_fixer.py" "\$@"
EOF

# Make wrappers executable
chmod +x "$BIN_DIR/mao-audit-imports"
chmod +x "$BIN_DIR/mao-fix-imports"

echo -e "${GREEN}✅ Created command wrappers in $BIN_DIR${NC}"

# Add to PATH if not already there
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "${YELLOW}💡 To use globally, add this to your ~/.bashrc or ~/.zshrc:${NC}"
    echo -e "${BLUE}export PATH=\"$BIN_DIR:\$PATH\"${NC}"
    echo ""
fi

echo -e "${GREEN}🎉 Installation complete!${NC}"
echo ""
echo -e "${BLUE}Usage:${NC}"
echo -e "  ${GREEN}mao-audit-imports${NC}  - Run import audit"
echo -e "  ${GREEN}mao-fix-imports${NC}   - Run automated fixer"
echo ""
echo -e "${BLUE}Or run directly:${NC}"
echo -e "  ${GREEN}python $SCRIPT_DIR/import_audit.py${NC}"
echo -e "  ${GREEN}python $SCRIPT_DIR/import_fixer.py${NC}"
echo ""
echo -e "${YELLOW}⚠️  Always commit your changes before running the fixer!${NC}" 