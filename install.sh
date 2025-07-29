#!/bin/bash

echo "🚀 Installing Mao - Modular Agent Orchestrator..."

# Install TypeScript UI dependencies
echo "📦 Installing UI dependencies..."
cd interfaces/terminal-ui && npm install
cd ../..

# Make Python file executable
chmod +x mao_v4.py

# Create global npm link
echo "🔗 Setting up global npm command..."
npm install -g .

echo "✅ Mao installation complete!"
echo ""
echo "You can now run:"
echo "  mao mao       # Launch TypeScript terminal UI"
echo "  mao --help    # Show available commands"
echo "  mao --setup   # Run setup/onboarding"
echo ""