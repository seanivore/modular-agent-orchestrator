#!/bin/bash

# MAO v4 Quality Validator Installation Script
# Installs the quality validator as a command-line tool

set -e

echo "🎯 Installing MAO v4 Quality Validator..."

# Change to project root to avoid nested directories
cd "$(dirname "$0")/../.."

# Create scripts directory if it doesn't exist
mkdir -p scripts/quality_validator

# Copy the validator script
echo "📄 Validator script already exists..."
if [ ! -f "scripts/quality_validator/mao_validator.py" ]; then
    echo "❌ Error: mao_validator.py not found!"
    echo "Please ensure the Python validator script exists before running install."
    exit 1
fi

# Make it executable
chmod +x scripts/quality_validator/mao_validator.py

# Create command using Sean's standard pattern
echo "🔧 Creating mao-validate command instructions..."
echo ""
echo "To create the mao-validate command, run these commands:"
echo ""
echo "# Create the command file:"
echo "cat > ~/bin/mao-validate << 'EOF'"
echo "#!/bin/bash"
echo ""
echo "# MAO Quality Validator Command"
echo "# Usage: mao-validate [options]"
echo ""
echo "# Direct path to the validator script"
echo "VALIDATOR_SCRIPT=\"$(pwd)/scripts/quality_validator/mao_validator.py\""
echo ""
echo "if [ ! -f \"\$VALIDATOR_SCRIPT\" ]; then"
echo "    echo \"❌ Error: Validator script not found at \$VALIDATOR_SCRIPT\""
echo "    echo \"Please ensure the MAO Quality Validator is properly installed.\""
echo "    exit 1"
echo "fi"
echo ""
echo "# Run the validator with all arguments passed through"
echo "python3 \"\$VALIDATOR_SCRIPT\" \"\$@\""
echo "EOF"
echo ""
echo "# Make the command executable:"
echo "chmod +x ~/bin/mao-validate"
echo ""
echo "Then you can run: mao-validate from anywhere!"

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