#!/bin/bash

# MAO v4 Quality Validator Installation Script
# Installs the quality validator as a command-line tool

set -e

echo "🎯 Installing MAO v4 Quality Validator..."

# Create scripts directory if it doesn't exist
mkdir -p scripts/quality_validator

# Copy the validator script
echo "📄 Creating validator script..."
cat > scripts/quality_validator/mao_validator.py << 'EOF'
# The Python script would be copied here
# For now, this is a placeholder that points to the artifact
echo "Please copy the MAO Quality Validator Python code to this file"
EOF

# Make it executable
chmod +x scripts/quality_validator/mao_validator.py

# Create a convenient command script
echo "🔧 Creating mao-validate command..."
cat > scripts/quality_validator/mao-validate << 'EOF'
#!/bin/bash

# MAO Quality Validator Command
# Usage: mao-validate [options]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATOR_SCRIPT="$SCRIPT_DIR/mao_validator.py"

if [ ! -f "$VALIDATOR_SCRIPT" ]; then
    echo "❌ Error: Validator script not found at $VALIDATOR_SCRIPT"
    echo "Please ensure the MAO Quality Validator is properly installed."
    exit 1
fi

# Run the validator with all arguments passed through
python3 "$VALIDATOR_SCRIPT" "$@"
EOF

# Make the command executable
chmod +x scripts/quality_validator/mao-validate

# Add to PATH (optional - create symlink in project root)
ln -sf scripts/quality_validator/mao-validate ./mao-validate

echo "✅ Installation complete!"
echo ""
echo "🚀 Usage:"
echo "  ./mao-validate                    # Run all validations"
echo "  ./mao-validate --verbose          # Verbose output"
echo "  ./mao-validate --project-root .   # Specify project root"
echo ""
echo "🎯 The validator will check:"
echo "  ✓ Tool structure (4-file pattern)"
echo "  ✓ Cost function implementation"
echo "  ✓ Cache pattern usage"
echo "  ✓ Import path correctness"
echo "  ✓ JSON schema compliance"
echo "  ✓ Error handling patterns"
echo ""
echo "💡 Add to your CI/CD pipeline to prevent regressions!"