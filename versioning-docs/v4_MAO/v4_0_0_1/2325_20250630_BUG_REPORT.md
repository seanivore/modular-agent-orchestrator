Mao application loaded. I typed nothing exect a '/' (no single quotes) and got the following error: 

```zsh
│ /Users/seanivore/Development/modular-agent-orchestrator/interfaces/terminal/c │
│ omponents/autocomplete_system.py:288 in show_suggestions                      │
│                                                                               │
│   285 │   │   │   │   await self.dropdown.remove()                            │
│   286 │   │   │                                                               │
│   287 │   │   │   self.dropdown = AutoCompleteDropdown(suggestions)           │
│ ❱ 288 │   │   │   await self.mount(self.dropdown)                             │
│   289 │   │   else:                                                           │
│   290 │   │   │   await self.hide_suggestions()                               │
│   291                                                                         │
│                                                                               │
│ ╭───────────────────────────────── locals ──────────────────────────────────╮ │
│ │       query = ''                                                          │ │
│ │        self = CLIAutoCompleteSystem()                                     │ │
│ │ suggestions = [                                                           │ │
│ │               │   {                                                       │ │
│ │               │   │   'name': 'mao',                                      │ │
│ │               │   │   'command': 'mao',                                   │ │
│ │               │   │   'terminal_flag': '--mao',                           │ │
│ │               │   │   'type': 'standalone',                               │ │
│ │               │   │   'interface_method': 'launch_terminal_ui_smart',     │ │
│ │               │   │   'help': 'Launch the beautiful Mao terminal          │ │
│ │               interface with smart user detection',                       │ │
│ │               │   │   'description': 'Start the main Mao terminal         │ │
│ │               application. Detects returning users for quick launc'+43,   │ │
│ │               │   │   'category': 'OTHER',                                │ │
│ │               │   │   'examples': [                                       │ │
│ │               │   │   │   {                                               │ │
│ │               │   │   │   │   'usage': 'mao --mao',                       │ │
│ │               │   │   │   │   'description': 'Smart launch - quick for    │ │
│ │               returning users, onboarding for new users'                  │ │
│ │               │   │   │   }                                               │ │
│ │               │   │   ]                                                   │ │
│ │               │   },                                                      │ │
│ │               │   {                                                       │ │
│ │               │   │   'command': 'dry_run',                               │ │
│ │               │   │   'type': 'standalone',                               │ │
│ │               │   │   'terminal_flag': '--dry-run',                       │ │
│ │               │   │   'app_command': '/dry-run',                          │ │
│ │               │   │   'interface_method': 'dry_run',                      │ │
│ │               │   │   'help': 'Simulate workflow execution without        │ │
│ │               actually running',                                          │ │
│ │               │   │   'cost_estimate': 0.008,                             │ │
│ │               │   │   'logic_file': 'configs/cli/dry_run/dry_run.py',     │ │
│ │               │   │   'ui_file': 'configs/cli/dry_run/ui_dry_run.py',     │ │
│ │               │   │   'operations': {                                     │ │
│ │               │   │   │   'execute': {                                    │ │
│ │               │   │   │   │   'description': 'Simulate workflow execution │ │
│ │               and validate configuration',                                │ │
│ │               │   │   │   │   'required_params': [],                      │ │
│ │               │   │   │   │   'optional_params': [                        │ │
│ │               │   │   │   │   │   'workflow',                             │ │
│ │               │   │   │   │   │   'detailed_validation',                  │ │
│ │               │   │   │   │   │   'execution_plan'                        │ │
│ │               │   │   │   │   ]                                           │ │
│ │               │   │   │   }                                               │ │
│ │               │   │   },                                                  │ │
│ │               │   │   ... +3                                              │ │
│ │               │   },                                                      │ │
│ │               │   {                                                       │ │
│ │               │   │   'command': 'tools',                                 │ │
│ │               │   │   'type': 'standalone',                               │ │
│ │               │   │   'terminal_flag': '--tools',                         │ │
│ │               │   │   'app_command': '/tools',                            │ │
│ │               │   │   'interface_method': 'list_tools',                   │ │
│ │               │   │   'help': 'List all available tools',                 │ │
│ │               │   │   'cost_estimate': 0.001,                             │ │
│ │               │   │   'logic_file': 'configs/cli/tools/tools.py',         │ │
│ │               │   │   'ui_file': 'configs/cli/tools/ui_tools.py',         │ │
│ │               │   │   'operations': {                                     │ │
│ │               │   │   │   'execute': {                                    │ │
│ │               │   │   │   │   'description': 'Display categorized list of │ │
│ │               all available tools with capabilities',                     │ │
│ │               │   │   │   │   'required_params': [],                      │ │
│ │               │   │   │   │   'optional_params': []                       │ │
│ │               │   │   │   }                                               │ │
│ │               │   │   },                                                  │ │
│ │               │   │   ... +3                                              │ │
│ │               │   },                                                      │ │
│ │               │   {                                                       │ │
│ │               │   │   'command': 'privacy',                               │ │
│ │               │   │   'type': 'standalone',                               │ │
│ │               │   │   'terminal_flag': '--privacy',                       │ │
│ │               │   │   'app_command': '/privacy',                          │ │
│ │               │   │   'interface_method': 'enable_privacy_mode',          │ │
│ │               │   │   'help': 'Use privacy-focused models and providers   │ │
│ │               only',                                                      │ │
│ │               │   │   'category': 'OTHER'                                 │ │
│ │               │   },                                                      │ │
│ │               │   {                                                       │ │
│ │               │   │   'command': 'update',                                │ │
│ │               │   │   'type': 'needs_file_or_directory',                  │ │
│ │               │   │   'terminal_flag': '--update',                        │ │
│ │               │   │   'app_command': '/update',                           │ │
│ │               │   │   'interface_method': 'update_workflow',              │ │
│ │               │   │   'help': 'Update workflow with multi-path support    │ │
│ │               and secondary flags',                                       │ │
│ │               │   │   'cost_estimate': 0.005,                             │ │
│ │               │   │   'logic_file': 'configs/cli/update/update.py',       │ │
│ │               │   │   'ui_file': 'configs/cli/update/ui_update.py',       │ │
│ │               │   │   'operations': {                                     │ │
│ │               │   │   │   'execute': {                                    │ │
│ │               │   │   │   │   'description': 'Execute workflow update     │ │
│ │               with JSON file',                                            │ │
│ │               │   │   │   │   'required_params': ['json_file'],           │ │
│ │               │   │   │   │   'optional_params': [                        │ │
│ │               │   │   │   │   │   'target_directory',                     │ │
│ │               │   │   │   │   │   'add',                                  │ │
│ │               │   │   │   │   │   'remove',                               │ │
│ │               │   │   │   │   │   'replace',                              │ │
│ │               │   │   │   │   │   'rename',                               │ │
│ │               │   │   │   │   │   'chat'                                  │ │
│ │               │   │   │   │   ]                                           │ │
│ │               │   │   │   }                                               │ │
│ │               │   │   },                                                  │ │
│ │               │   │   ... +5                                              │ │
│ │               │   },                                                      │ │
│ │               │   {                                                       │ │
│ │               │   │   'command': 'chat',                                  │ │
│ │               │   │   'type': 'needs_input',                              │ │
│ │               │   │   'terminal_flag': '--chat',                          │ │
│ │               │   │   'app_command': '/chat',                             │ │
│ │               │   │   'interface_method': 'chat',                         │ │
│ │               │   │   'help': 'Jump into application and send first       │ │
│ │               message to AI',                                             │ │
│ │               │   │   'cost_estimate': 0.002,                             │ │
│ │               │   │   'logic_file': 'configs/cli/chat/chat.py',           │ │
│ │               │   │   'ui_file': 'configs/cli/chat/ui_chat.py',           │ │
│ │               │   │   'operations': {                                     │ │
│ │               │   │   │   'execute': {                                    │ │
│ │               │   │   │   │   'description': 'Process message through     │ │
│ │               conversation bridge to create workflow',                    │ │
│ │               │   │   │   │   'required_params': ['message'],             │ │
│ │               │   │   │   │   'optional_params': []                       │ │
│ │               │   │   │   }                                               │ │
│ │               │   │   },                                                  │ │
│ │               │   │   ... +3                                              │ │
│ │               │   },                                                      │ │
│ │               │   {                                                       │ │
│ │               │   │   'name': 'config',                                   │ │
│ │               │   │   'command': 'config',                                │ │
│ │               │   │   'type': 'manager_integration',                      │ │
│ │               │   │   'complexity': 'medium',                             │ │
│ │               │   │   'terminal_flag': '--config',                        │ │
│ │               │   │   'app_command': '/config',                           │ │
│ │               │   │   'interface_method': 'open_config_management',       │ │
│ │               │   │   'help': 'Application settings management with user  │ │
│ │               configuration persistence',                                 │ │
│ │               │   │   'file_path': 'configs/cli/config/config.py',        │ │
│ │               │   │   'ui_path': 'configs/cli/config/ui_config.py',       │ │
│ │               │   │   ... +8                                              │ │
│ │               │   },                                                      │ │
│ │               │   {                                                       │ │
│ │               │   │   'command': 'set_model',                             │ │
│ │               │   │   'type': 'standalone',                               │ │
│ │               │   │   'terminal_flag': '--set-model',                     │ │
│ │               │   │   'app_command': '/set-model',                        │ │
│ │               │   │   'interface_method': 'set_model',                    │ │
│ │               │   │   'help': 'Set favorite model via                     │ │
│ │               settings_manager.py',                                       │ │
│ │               │   │   'cost_estimate': 0.001,                             │ │
│ │               │   │   'logic_file': 'configs/cli/set_model/set_model.py', │ │
│ │               │   │   'ui_file': 'configs/cli/set_model/ui_set_model.py', │ │
│ │               │   │   'operations': {                                     │ │
│ │               │   │   │   'execute': {                                    │ │
│ │               │   │   │   │   'description': "Set user's favorite model   │ │
│ │               preference",                                                │ │
│ │               │   │   │   │   'required_params': [                        │ │
│ │               │   │   │   │   │   'model_name',                           │ │
│ │               │   │   │   │   │   'username'                              │ │
│ │               │   │   │   │   ],                                          │ │
│ │               │   │   │   │   'optional_params': []                       │ │
│ │               │   │   │   }                                               │ │
│ │               │   │   },                                                  │ │
│ │               │   │   ... +3                                              │ │
│ │               │   },                                                      │ │
│ │               │   {                                                       │ │
│ │               │   │   'command': 'free_only',                             │ │
│ │               │   │   'type': 'standalone',                               │ │
│ │               │   │   'terminal_flag': '--free',                          │ │
│ │               │   │   'app_command': '/free',                             │ │
│ │               │   │   'interface_method': 'enable_free_only',             │ │
│ │               │   │   'help': 'Use only free AI models for cost           │ │
│ │               optimization',                                              │ │
│ │               │   │   'category': 'OTHER'                                 │ │
│ │               │   },                                                      │ │
│ │               │   {                                                       │ │
│ │               │   │   'name': 'providers',                                │ │
│ │               │   │   'command': 'providers',                             │ │
│ │               │   │   'type': 'standalone',                               │ │
│ │               │   │   'terminal_flag': '--providers',                     │ │
│ │               │   │   'app_command': '/providers',                        │ │
│ │               │   │   'interface_method': 'list_providers',               │ │
│ │               │   │   'help': 'List all available providers with metadata │ │
│ │               and capabilities',                                          │ │
│ │               │   │   'cost_estimate': 0.001,                             │ │
│ │               │   │   'file_path': 'configs/cli/providers/providers.py',  │ │
│ │               │   │   'ui_path': 'configs/cli/providers/ui_providers.py', │ │
│ │               │   │   ... +4                                              │ │
│ │               │   }                                                       │ │
│ │               ]                                                           │ │
│ ╰───────────────────────────────────────────────────────────────────────────╯ │
│                                                                               │
│ /Users/seanivore/.pyenv/versions/3.13.3/lib/python3.13/site-packages/textual/ │
│ widget.py:1299 in mount                                                       │
│                                                                               │
│   1296 │   │   if self._closing or self._pruning:                             │
│   1297 │   │   │   return AwaitMount(self, [])                                │
│   1298 │   │   if not self.is_attached:                                       │
│ ❱ 1299 │   │   │   raise MountError(f"Can't mount widget(s) before {self!r} i │
│   1300 │   │   # Check for duplicate IDs in the incoming widgets              │
│   1301 │   │   ids_to_mount = [                                               │
│   1302 │   │   │   widget_id for widget in widgets if (widget_id := widget.id │
│                                                                               │
│ ╭────────────── locals ───────────────╮                                       │
│ │   after = None                      │                                       │
│ │  before = None                      │                                       │
│ │    self = CLIAutoCompleteSystem()   │                                       │
│ │ widgets = (AutoCompleteDropdown(),) │                                       │
│ ╰─────────────────────────────────────╯                                       │
╰───────────────────────────────────────────────────────────────────────────────╯
MountError: Can't mount widget(s) before CLIAutoCompleteSystem() is mounted
🎭 Terminal UI launched successfully
> ~/Dev/modular-agent-orchestrator >                                    23:25:12
```