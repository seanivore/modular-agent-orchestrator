  Files Structure (Following Your Pattern):

  scripts/
  ├── install_mao_command.sh    # Installation script (like
  install_ptree_command.sh)
  └── mao.sh                    # Implementation script (like ptree.sh)

  After Installation:

  ~/bin/
  └── mao                       # Clean command (no .sh extension, like
  ptree)

  Usage (Clean Commands):

  mao           # New user onboarding
  mao mao       # Smart launch (git-inspired)

  Installation Process (Following Your MO):

  # 1. Run the installer
  bash scripts/install_mao_command.sh

  # 2. Use the clean command
  mao mao

  Now it matches exactly how you have ptree set up! No more confusion with
  .sh extensions in the command usage - just clean mao and mao mao
  commands! 🎭✨

  The bug report should now work perfectly with the proper command
  structure and the MCP error handling fixes!


----

I just installed the latest version of Mao, and I'm getting the following error: 

```zsh
> ~/Dev/modular-agent-orchestrator > chmod +x scripts/mao_launch_setup.sh
> ~/Dev/modular-agent-orchestrator > sudo bash scripts/mao_launch_setup.sh
🚀 Setting up Mao command...
✅ MAO command installed successfully!

🎭 You can now use:
   mao mao          # Launch beautiful terminal UI
   mao --login      # Force login screen
   mao --continue   # Continue last session
   mao --config     # Open configuration
   mao --help       # See all options

🚀 Try running: mao mao
> ~/Dev/modular-agent-orchestrator > cd ..                             23:01:13
> ~/Development > mao mao                                              23:01:25
usage: mao_v4.py
mao_v4.py: error: unrecognized arguments: mao
> ~/Development > mao                                                  23:01:28
Initializing MCP Integration Hub...
Mock connecting to aider server...
Warning: Failed to register server aider: 'MemoryMCPManager' object has no attribute 'create_entities'
ERROR:root:Function register_server failed with non-retryable exception: 'MemoryMCPManager' object has no attribute 'create_entities'
ERROR:root:Unexpected error in mcp_connector_register: 'MemoryMCPManager' object has no attribute 'create_entities'
Traceback (most recent call last):
  File "/Users/seanivore/Development/modular-agent-orchestrator/tools/mcp_connector/mcp_connector.py", line 91, in register_server
    self.memory_manager.create_entities([{
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'MemoryMCPManager' object has no attribute 'create_entities'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/seanivore/Development/modular-agent-orchestrator/orchestrator/error_handling.py", line 68, in wrapper
    return func(*args, **kwargs)
  File "/Users/seanivore/Development/modular-agent-orchestrator/orchestrator/error_handling.py", line 208, in wrapper
    return func(*args, **kwargs)
  File "/Users/seanivore/Development/modular-agent-orchestrator/tools/mcp_connector/mcp_connector.py", line 114, in register_server
    self.memory_manager.create_entities([{
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'MemoryMCPManager' object has no attribute 'create_entities'
Mock connecting to filesystem server...
Warning: Failed to register server filesystem: 'MemoryMCPManager' object has no attribute 'create_entities'
ERROR:root:Function register_server failed with non-retryable exception: 'MemoryMCPManager' object has no attribute 'create_entities'
ERROR:root:Unexpected error in mcp_connector_register: 'MemoryMCPManager' object has no attribute 'create_entities'
Traceback (most recent call last):
  File "/Users/seanivore/Development/modular-agent-orchestrator/tools/mcp_connector/mcp_connector.py", line 91, in register_server
    self.memory_manager.create_entities([{
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'MemoryMCPManager' object has no attribute 'create_entities'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/seanivore/Development/modular-agent-orchestrator/orchestrator/error_handling.py", line 68, in wrapper
    return func(*args, **kwargs)
  File "/Users/seanivore/Development/modular-agent-orchestrator/orchestrator/error_handling.py", line 208, in wrapper
    return func(*args, **kwargs)
  File "/Users/seanivore/Development/modular-agent-orchestrator/tools/mcp_connector/mcp_connector.py", line 114, in register_server
    self.memory_manager.create_entities([{
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'MemoryMCPManager' object has no attribute 'create_entities'
Warning: Failed to initialize MCP servers: 'status'
✅ MCP Integration Hub initialized successfully
❌ Could not start the Mao onboarding experience
```