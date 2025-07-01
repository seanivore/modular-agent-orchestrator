# 🚀 Launch Your Beautiful MAO Terminal UI!

## 🎯 **Quick Start (30 seconds)**

### **Step 1: Setup the Command**
```bash
# Make the setup script executable and run it
chmod +x setup_mao_command.sh
sudo bash setup_mao_command.sh
```

### **Step 2: Launch MAO!**
```bash
# Launch the beautiful terminal UI
mao mao
```

**That's it!** Your beautiful MAO terminal will launch with:
- Claude Code-style interface
- CLI auto-complete with fuzzy search
- MAO visual protocol (colors, shapes, trees)
- User onboarding flow
- Workflow creation interface

---

## 🎭 **Available Commands**

### **Main Commands**
```bash
mao mao              # Launch beautiful terminal UI
mao --login          # Force login screen  
mao --continue       # Continue last session
mao --config         # Open configuration settings
mao --help           # Show all options
```

### **Quick Commands** 
```bash
mao --model gpt4     # Set favorite model
mao --provider openai # Set default provider
mao --model-list     # List available models
mao --provider-list  # List available providers
mao --workflow uid-abc-123  # Show workflow details
mao --setup ./my_workflow/  # Setup workflow from directory
```

---

## 🎨 **What You'll See**

### **First Launch (New User)**
1. **Welcome Screen** with MAO cat logo
2. **Username Entry** with validation
3. **Theme Selection** with live previews
4. **Main Interface** with conversation area

### **Returning User**
1. **Quick Launch** directly to main interface
2. **Personal Greeting** with your username
3. **Recent Workflows** in context
4. **Smart Auto-Complete** based on your usage

### **Main Interface Features**
- **Unified Input** - Single text field for everything
- **Auto-Complete Dropdown** - Type `/` to see commands
- **Workflow Visualization** - See orchestration trees
- **Live Status Updates** - Real-time progress cycling
- **Beautiful Colors** - MAO semantic visual protocol

---

## 🔧 **Troubleshooting**

### **"Command not found: mao"**
```bash
# Re-run the setup script with sudo
sudo bash setup_mao_command.sh

# Or manually check if /usr/local/bin is in your PATH
echo $PATH | grep "/usr/local/bin"
```

### **"Permission denied"**
```bash
# Fix permissions
sudo chmod +x /usr/local/bin/mao
sudo chmod +x mao_launcher.py
```

### **"Python module not found"**
```bash
# Install missing dependencies
pip install textual rich watchdog

# Or if using conda
conda install textual rich watchdog
```

### **"Textual not working"**
```bash
# Update textual to latest version
pip install --upgrade textual

# Test textual works
python -c "from textual.app import App; print('Textual OK')"
```

---

## 🎉 **Cool Things to Try**

### **Auto-Complete Magic**
1. Type `/` and watch commands appear
2. Type `/too` and see fuzzy search find `tools`
3. Use arrow keys to navigate suggestions
4. Press Enter to select

### **Workflow Creation**
1. Type something like "Create a marketing strategy"
2. Watch MAO create workflow visualization
3. See orchestration trees with triangles/circles
4. Experience live status cycling

### **Theme Switching**
1. Launch with `mao --config`
2. Change theme and see immediate updates
3. Preview different color schemes

### **Command History**
1. Use previous commands with Up/Down arrows
2. See contextual suggestions based on workflow state
3. Notice how auto-complete learns your patterns

---

## 🚀 **Next Steps**

### **After Your First Launch:**
1. **Create a test workflow** - Try "Help me organize my tasks"
2. **Explore commands** - Type `/help` to see everything
3. **Customize settings** - Run `mao --config`
4. **Add your tools** - Drop configs in `configs/tools/`

### **Advanced Usage:**
1. **Create custom workflows** using the templates
2. **Set up GitHub integration** for auto-documentation
3. **Build your tool library** with plug-and-play configs
4. **Share configs** with your team

---

## 🎭 **The MAO Experience**

When you run `mao mao`, you're not just launching a terminal app - you're entering a **complete AI workflow orchestration environment** that:

✨ **Looks beautiful** - Claude Code-quality interface  
🧠 **Thinks contextually** - Smart suggestions based on state  
🎯 **Stays simple** - Complex workflows made easy  
🚀 **Grows with you** - Add capabilities by dropping in configs  
🤖 **Partners with AI** - Claude Code integration throughout  

**Welcome to the future of AI workflow orchestration!** 🎭✨

---

## 💡 **Pro Tips**

1. **Learn the shortcuts** - `/` for commands, `Ctrl+C` to quit
2. **Use the visual cues** - Colors and shapes have meaning
3. **Trust the auto-complete** - It gets smarter as you use it
4. **Think in workflows** - Describe goals, not steps
5. **Leverage the templates** - Everything is plug-and-play

**Now go launch that beautiful interface and create something amazing!** 🚀