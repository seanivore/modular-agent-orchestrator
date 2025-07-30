# Section III: Letting Mao Set Up Your Project 
*Experience the walkthrough of a first-time user's experience* 

---

You're ready to automate your life. Advanced agentic orchestration, delegating to subagents working in parallel, fully compatible with any LLM model, it all sounds great. 

But you know what sounds better? *No learning curve.* 

Mao is here. Not just to help you, but to totally take over for you ~(=^‥^)

---

## New User Experience

### First Time Setup

**Getting Started**: Download Mao, run the installer, and you're ready to begin. The system handles user configuration, model setup, and tool access automatically.

**Quick Onboarding**: Mao introduces itself and walks you through creating your first workflow. The conversation feels natural - just describe what you want to accomplish, and Mao handles the technical complexity.

### Install 'Mao' 

This is the literal hardest part of using Mao. (It's not hard at all.)

1. Install [Node.js 18+](https://nodejs.org/en/download/)
2. Open the terminal on your computer
3. Run `npm install -g @seanivore/mao` 

```bash
npm install -g @seanivore/mao
#     │      │  │
#     │      │  └── Scoped package name 
#     │      └────── Install globally (system-wide)
#     └───────────── Package manager
```

---

## Launch Mao's Application 

Execute the command `mao mao` to launch the application. 

```bash
    mao mao         # Launches Mao's application 
```

If you forget a second "mao" ~(=^‥^) you'll be treated as a new user. 

```bash
    mao              # Launches app for new user 
```

You've used Mao before on this device? Launch the app already logged in. 

```bash
    mao --login      # Launches with the Username field available 
    mao --login --username seanivore # Launches with the Username field set to "seanivore" 
    mao --continue   # Launches Mao in the last session 
```

### UserID, Username, and Security 

It's your first time with Mao ~(=^‥^) The app loads and:

  1. You see two text fields, only the top is editable 
  2. Enter your name, or a Username you won't forget, in that top text field 
  3. The lower text field will automatically populate with a UserID 

**You only need to remember your Username** 

  - The UserID is a unique identifier for your account 
  - It is used as an additional layer of anonymity for your data 
  - On the backend, your Username and its UserID are shown together in only one configuration file 
  - All other data, settings, and workflows are stored with the UserID 

**Extra security?** 

  - We do not currently have any analytics that would require a UserID 
  - You will be notified if we add any in the future 
  - If you would ever like to know what data `Mao` has stored on your behalf, email us 
  - All data is stored in a secure, encrypted database. 
  - User analytics are architecturally separate from system analytics 
  - Should you ever want to have your data deleted, please email support 

**Where do I set my password?** 

- Due to how young Mao v4.0.0 is, we have not yet implemented a password system 
- You will be notified when a password system is available 
- Should this concern you, please email support, and we will be happy to help you 

---

## Create Unique UserIDs 

The system automatically generates unique UserIDs using mathematical operations for consistency and collision avoidance. The `meid` script ensures the same username always produces the same UserID.

- The system checks to see if the UserID already exists 
- New user login creates `./configs/user/username/user_username.json` file 
- A UserID will always be the same for a specific Username 
- Subdirectories and files include preference, memories, analytics, and other data 
- Workflows are stored in the `./configs/workflows/` directory and only include the UserID 

### UserID Generation Architecture
*scripts/user_id_generator/user_id_generator.py*

The UserID generation system uses mathematical operations for deterministic ID creation:

```python
# scripts/user_id_generator/user_id_generator.py
def generate_user_id(username):
    """Quick function to generate a user ID"""
    generator = UserIDGenerator()
    user_id, _ = generator.generate_user_id(username)
    return user_id

class UserIDGenerator:
    def generate_user_id(self, username):
        """Generate a deterministic user ID from username"""
        # Uses character count, ASCII values, mathematical operations
        # Same username always produces same UserID for consistency
```

### `meid` Used Separately in Terminal 

```bash
meid seanivore # Run command with the Username 
> user-1642    # Response is that Username's User ID 

Usage:
  meid username       Generate user ID for username
  meid -e username    Generate user ID with explanation
  meid -h             Show this help

Examples:
  meid seanivore      # user-1642
  meid -e alice       # user-1161 | Steps: 5 chars -> ...

Mathematical Operations:
  Uses mathematical operations to ensure consistency
  Same username always produces the same user ID
```

### Changing User Settings 

```bash
/config   # Run this slash command while in the app to open the config screen 
mao --config   # Launch the app to open on the config screen 
```

---

## Session Management & Memory

### Persistent Context

**Always On The Same Page**: Mao remembers everything about your projects, preferences, and working style. Start conversations mid-thought, and Mao picks up exactly where you left off.

**Smart Context Switching**: Work on multiple projects simultaneously. Mao maintains separate contexts and switches seamlessly based on your current focus.

**Learning Your Style**: Over time, Mao learns your communication patterns, quality standards, and business priorities. Each interaction becomes more personalized and efficient.

### Cross-Session Continuity 

**Project Memory**: Every workflow, decision, and outcome is remembered. Return to projects weeks later, and Mao provides complete context and suggests next steps.

**Pattern Recognition**: Mao identifies recurring workflows and suggests templates. Your marketing processes become reusable assets that improve over time.

The session management system relies on the **Memory MCP (Model Context Protocol)** server to maintain persistent workflow state and user context across sessions. This creates seamless continuity that feels magical to users but operates on solid technical foundations.

### Memory MCP Integration Architecture
*orchestrator/memory_mcp.py, orchestrator/user_memory_manager.py, orchestrator/workflow_state.py*

The Memory MCP integration provides persistent workflow state and cross-session continuity through coordinated memory management:

**Memory MCP Manager** (`orchestrator/memory_mcp.py`):

```python
class MemoryMCPManager:
    """Manages workflow state persistence using Memory MCP"""
    
    def __init__(self):
        self.cache = CacheManager()
        self._client = None  # Lazy load MCP client
    
    @handle_errors(operation_name="create_workflow_context", return_dict=True)
    def create_workflow_context(self, workflow_id: str, user_goal: str) -> str:
        """Initialize complete workflow context in Memory MCP"""
        context_data = {
            "workflow_id": workflow_id,
            "user_goal": user_goal,
            "created_at": datetime.now().isoformat(),
            "status": "initialized"
        }
        
        # Create workflow entity in memory graph
        entity_name = f"workflow-{workflow_id}"
        self.client.create_entities([{
            "name": entity_name,
            "entityType": "workflow",
            "observations": [json.dumps(context_data)]
        }])
        
        return entity_name
    
    def update_workflow_state(self, workflow_id: str, update_content: str) -> bool:
        """Update workflow state with new information"""
        entity_name = f"workflow-{workflow_id}"
        self.client.add_observations([{
            "entityName": entity_name,
            "contents": [f"{datetime.now().isoformat()}: {update_content}"]
        }])
        return True
```

**User Memory Manager** (`orchestrator/user_memory_manager.py`):

```python
class UserMemoryManager:
    """Manages user-specific memory storage with MCP integration"""
    
    def __init__(self):
        self.memory_mcp = MemoryMCPManager()
        self.cache_duration = 300  # 5-minute cache for user data
    
    @handle_errors(operation_name="store_memory", return_dict=True)
    def store_memory(self, user_id: str, content: str, category: str = None,
                    tags: List[str] = None, priority: str = "medium") -> Dict[str, Any]:
        """Store user memory with automatic categorization"""
        memory_id = f"user-{user_id}-memory-{uuid4().hex[:8]}"
        
        # Organize memory data
        memory_data = {
            "content": content,
            "category": category or "general",
            "tags": tags or [],
            "priority": priority,
            "stored_at": datetime.now().isoformat()
        }
        
        # Store in Memory MCP
        self.memory_mcp.client.create_entities([{
            "name": memory_id,
            "entityType": "user_memory",
            "observations": [json.dumps(memory_data)]
        }])
        
        return {"success": True, "memory_id": memory_id}
```

**Session Recovery Integration**:

```python
def handle_session_recovery(self, workflow_id: str) -> Optional[Dict[str, Any]]:
    """Recover complete workflow session state"""
    entity_name = f"workflow-{workflow_id}"
    
    # Search Memory MCP for workflow context
    search_results = self.client.search_nodes(entity_name)
    
    if search_results and len(search_results) > 0:
        workflow_entity = search_results[0]
        
        # Extract workflow state from observations
        observations = workflow_entity.get("observations", [])
        latest_state = json.loads(observations[-1]) if observations else {}
        
        return {
            "can_resume": True,
            "workflow_id": workflow_id,
            "last_state": latest_state,
            "recovery_point": datetime.now().isoformat()
        }
    
    return None
```

This architecture ensures seamless continuity through persistent memory graphs while maintaining privacy-first user data separation and efficient session recovery capabilities.

---

## Login & Theme Selection  

**Choosing your username** 

- On the login screen you'll be prompted to enter a username in the input field 
- It must be 6-20 characters long and can only contain alpha-numeric characters 
- Chose a username that you **will not forget** as it can be used to search you workflows and more 

**Setting your theme** 

  - If the User ID was recognized, the theme selection would not be shown
  - After login, the User is prompted to select a theme "that looks best in their terminal" 
  - You'll have a few simple options that vary in contrast so you can choose the most legible for your terminal 
  - Your terminal settings otherwise will not be affected in any way 

   1. Dark mode
   2. Light mode
 ❯ 3. Dark mode (CVD) ✔
   1. Light mode (CVD)
   2. Dark mode (ANSI colors only)
   3. Light mode (ANSI colors only)

## Application Configuration Settings 

- New users are shown a 'tip' suggesting they try adjusting their settings 
- 'Tips' show up under the main text input field prefaced by a `?` 
- Often they'll say something like `?  try /config or /help` 
- Updated user settings automatically update in the `configs/users/user_username/` directory settings file 
- Select a setting, then toggle between available options for that app setting

| **SETTING**       | **DEFAULT**         | **DESCRIPTION**                                      |
| ----------------- | ------------------- | ---------------------------------------------------- |
| Quick launch      | `always`            | Launch app with last user logged in                  |
| Favorite model    | `claude-sonnet-4`   | Use for workflows unless discussed                   |
| Default provider  | `anthropic direct`  | I prefer this provider; discuss to change            |
| Theme             | `dark mode CVD`     | Dark computer theme; use high legibility colors      |
| Tone notification | `one time, no push` | When a workflow is complete, a simple tone is played |
| Cat vibes         | `I love it`         | We'll meow it up for you                             |
| Double-texting    | `always`            | Interrupt Mao like any messenger experience          |

### Quick Launch Options 

1. `always` = launch app with user from last session, unless logged out
2. `off` = load Username login on every startup 
3. `continue only` = launch `mao --continue` to skip login, otherwise load Username login 

### Favorite Model 

- Add a default model by casual name to your user settings  
- Startup `mao --model` or `/model` to set the model 
- Startup `mao --model-list` or `/model-list` to see all available models 

### Default Provider 

- Default a provider by their casual name and save it to your user settings 
- Helpful for Users who have a bunch of cash in a specific API provider 
- Startup `mao --provider` or `/provider` to set default provider 
- Startup `mao --provider-list` or `/provider-list` to see all available providers 

### Cat Vibes 

- We don't want to be too annoying with our cat branding 

  1. `I love it` = we'll meow it up for you 
  2. `mao and then` = adequate but not too much meowing 
  3. `be serious pls` = no meowing at all 

### Double-texting 

  1. `always` = send multiple messages to Mao in a row like any messenger experience 
  2. `never` = only allow one reply from each party at a time

### Tone Notification 

  1. `once, no push` = when a workflow is complete a simple, single tone is played; no push notification 
  2. `silent, push` = when a workflow is complete, no tone is played, but a push notification announces completion 
  3. `no notifications` = no tone is played; no push notification 

## Application Settings Are **MODULAR** Magic 

Want to set up new settings for the application? Ask Mao what files are needed, they'll do the rest. The modular settings system allows dynamic addition of new configuration options through JSON templates.

### Settings Architecture
*orchestrator/settings_manager.py, configs/settings/, configs/cli/config/config.py*

The modular settings system provides dynamic discovery and user preference management through coordinated components:

**Application Settings Manager** (`orchestrator/settings_manager.py`):

```python
@dataclass
class SettingDefinition:
    """Individual setting configuration"""
    name: str
    default: Any
    description: str
    type: str
    options: List[Dict] = None
    source: str = None
    fallback_options: List[str] = None
    ui_metadata: Dict = None

class ApplicationSettingsManager:
    """Manages modular application settings with dynamic discovery"""
    
    def __init__(self, settings_dir: str = "./configs/settings/"):
        self.settings_dir = Path(settings_dir)
        self.user_dir = Path("./configs/user/")
    
    @handle_errors(operation_name="discover_settings", return_dict=True)
    def discover_settings(self, force_refresh: bool = False) -> Dict[str, SettingDefinition]:
        """Dynamically discover all settings from directory using MAO caching"""
        cache_key = f"settings_discovery|{self.settings_dir}|{force_refresh}"
        
        # Check cache first (MAO standard caching pattern)
        if not force_refresh:
            cached_result = cache.get_cached_analysis(cache_key, "settings_discovery")
            if cached_result:
                cached_data = json.loads(cached_result)
                # Convert cached data back to SettingDefinition objects
                settings = {}
                for name, data in cached_data.items():
                    settings[name] = SettingDefinition(**data)
                return settings
        
        settings = {}
        
        # Scan all *_app_settings.json files
        for settings_file in self.settings_dir.glob("*_app_settings.json"):
            try:
                with open(settings_file, 'r') as f:
                    setting_data = json.load(f)
                
                # Convert to SettingDefinition
                setting_name = settings_file.stem.replace('_app_settings', '')
                settings[setting_name] = SettingDefinition(
                    name=setting_name,
                    default=setting_data.get('default'),
                    description=setting_data.get('description', ''),
                    type=setting_data.get('type', 'string'),
                    options=setting_data.get('options', []),
                    source=str(settings_file)
                )
            except Exception as e:
                # Log but don't break discovery
                continue
        
        # Cache results for performance
        cache_data = {name: setting.__dict__ for name, setting in settings.items()}
        cache.cache_content_analysis(cache_key, json.dumps(cache_data), "settings_discovery")
        
        return settings
```

**CLI Settings Integration** (`configs/cli/config/config.py`):

```python
@handle_errors(operation_name="config", return_dict=True)
def execute_config(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Main config command execution with settings management integration"""
    
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "config")
    if cached_result:
        return json.loads(cached_result)
    
    # Initialize settings manager
    settings_manager = ApplicationSettingsManager()
    
    # Get current session user
    current_user = get_session_user()
    if not current_user:
        return {"success": False, "error": "No active user session"}
    
    # Discover all available settings
    available_settings = settings_manager.discover_settings()
    
    # Get current user settings (delta storage)
    user_settings = get_user_settings(current_user["username"])
    
    # Merge with defaults for complete settings view
    complete_settings = {}
    for setting_name, setting_def in available_settings.items():
        complete_settings[setting_name] = {
            "current_value": user_settings.get(setting_name, setting_def.default),
            "default_value": setting_def.default,
            "description": setting_def.description,
            "options": setting_def.options,
            "type": setting_def.type
        }
    
    result = {
        "success": True,
        "user_id": current_user["user_id"],
        "username": current_user["username"],
        "available_settings": complete_settings,
        "settings_count": len(available_settings),
        "user_customizations": len(user_settings)
    }
    
    # Cache result for 12 minutes
    cache.cache_content_analysis(cache_key, json.dumps(result), "config")
    return result
```

**Delta Storage Pattern**:

```python
def update_user_setting(username: str, setting_name: str, new_value: Any) -> bool:
    """Update individual user setting using delta storage"""
    user_config_path = Path(f"./configs/user/{username}/user_{username}.json")
    
    # Load existing config or create new
    if user_config_path.exists():
        with open(user_config_path, 'r') as f:
            user_config = json.load(f)
    else:
        user_config = {"username": username, "settings_deltas": {}}
    
    # Update only changed settings (delta storage)
    user_config["settings_deltas"][setting_name] = new_value
    user_config["last_updated"] = datetime.now().isoformat()
    
    # Save updated configuration
    with open(user_config_path, 'w') as f:
        json.dump(user_config, f, indent=2)
    
    return True
```

This architecture enables seamless addition of new settings through JSON file creation while maintaining efficient delta-only user storage and comprehensive settings discovery.

---

## Creating a Workflow 

### One-Screen Terminal App Experience 

- Entering your Username, changing settings, and main chat are all the same screen
- This app has a "one-screen" experience; irrelevant info is cleared automatically  
- Our app only changes text colors, other than your default 

### Chatting with Mao  

- Your screen should show something like this: 

```
╭───────────────────────────────────────────────────╮
│ ~(=^‥^)  Mao is ready to help!                    │
│   user: seanivore                                 │
╰───────────────────────────────────────────────────╯


>   Say "hello" to Mao.
    ├ Describe your workflow 
    ├ Ask a question 
    └ Share your goal 


╭───────────────────────────────────────────────────╮
│ > How do we start building?                       │
╰───────────────────────────────────────────────────╯
  ?  /help for help, /config to change settings
```

- The `/help` option shows all of the available commands  
- The `?` 'tips' are AI created and contextually relevant 

#### `?` 'Tip' Examples 

```
  ?  /help for help, /config to change settings 
  ?  try /models or /tools to explore 
  ?  share your /goal and Mao will do all the work 
  ?  /workflow [custom_command] to continue a build 
  ?  message /continue to find your last project 
```

**Tell Mao what you want to do!** 

- User messages have a `>` bullet 
- Mao's messages have a `●` bullet 

```
╭───────────────────────────────────────────────────╮
│ ~(=^‥^)  Mao is ready to help!                    │
│   user:  seanivore                                │
╰───────────────────────────────────────────────────╯


>   I need to put together a detailed research 
    report that breaks down the best practices
    for hiring new creative talent. 

>   I have a bunch of details in my notes 
    already 

●   Great idea, seanivore. 
    ├ Rattle off the details and I'll wait to reply
    └ Or say something like "lead me" and I'll take the lead 

>   Mao created a Workflow ID: uid-scw-965
    Workflow added to memory; workflow log created 


╭───────────────────────────────────────────────────╮
│ > some rough notes to |                           │
╰───────────────────────────────────────────────────╯
  ?  /variables to see what is needed 
```

### Tell Mao About Your Project 

- Chat is flexible; Mao will chat like any AI model. Treat Mao like an employee. Provide as much or as little detail as you want. 
- Mao is not trained with any scripts; they are simply an expert in turning projects into tasks and then into a workflow 

**A goal is all Mao needs**

- The minimum Mao needs is to know your goal! 
- Mao will get an initial workflow created for you 
- If your goal is vague, Mao will ask for details 
- Jump into Mao setting up a workflow by using `/goal` 

```bash
mao --goal "Create a marketing plan for my Etsy shop featuring our promotion on crystals"  
/goal "I need instagram followers and we're running a promotion on crystals for my Etsy shop; what should we do?"  
```

**Work through the process with Mao**

- New to the app or learning workflow strategy, Mao will guide  
- Ask Mao what variables are needed and start there

**When in doubt, just have a conversation**

- Still working out the specifics yourself? 
- Need to brainstorm more? 
- Just start chatting about a Project
- Mau will tell you when they have enough to build a workflow  

### The Workflow ID 

- When you create a workflow alone or with Mao's help, the JSON object will need a workflow ID 
- In the app you will later be able to search for workflows using this ID; they can be pulled up by your Username 
- Run the `uid` command to get a collision-free (never repeated) unique ID --> `uid-abc-000` 
- Later, use `--workflow` with an ID to see that workflow's details 
- You can also run `--workflow` with the Custom Command of a workflow 

```bash 
uid                        # Creates a new unique Workflow ID 
mao --workflow uid-abc-000 # Shows workflow details 
/uid                       # Creates a new unique Workflow ID 
/workflow uid-abc-000      # Shows workflow details 
```

### Mao's "One Source of Truth"

Here's how Mao is able to always be on the same page as you. 

**The Memory MCP tool gives Mao a Persistent Vector Graph "memory" for context between sessions**

* The Workflow ID is for you 
  - It identifies your workflow and connects it to your UserID and Username 
  - Every new project, Mao will create a new Workflow ID 

* The Workflow ID is for Mao 
  - Mao tags memory context updates with the Workflow ID, keeping all information about the project together 
  - If you get interrupted, Mao uses the workflow ID to know exactly where to pick up
  - Mao uses the Workflow ID when running the automation to understand the project  

* Math is used to create the ID 
  - If you are curious or need to create a handful of UIDs, the -h flag for "HELP" 
  - This will show you more information you can find

```bash 
> uid -h # Help message 
uid - Generate unique workflow IDs

Usage:
  uid              Generate a single UID
  uid -e           Generate UID with mathematical explanation
  uid -b N         Generate N UIDs in batch
  uid -h           Show this help

Examples:
  uid              # uid-abc-123
  uid -e           # uid-abc-123 | Math: a(456)=473 → b(473)=419 → c(419)=396
  uid -b 5         # Generate 5 UIDs

Mathematical Operations:
  Each letter represents a mathematical operation:
  a=add, b=multiply, c=subtract, d=divide, e=power, f=fibonacci
  g=golden_ratio, h=hash, i=invert, j=jump, k=karmic, l=logarithmic
  m=mirror, n=nine_mult, o=orbit, p=prime_like, q=quadratic, r=reverse_add
  s=spiral, t=triangle, u=unity, v=vortex, w=wave, x=xor, y=yield, z=zenith
```

### Chat Interface & Terminal UI Architecture
*interfaces/ui_terminal.py, orchestrator/conversation_bridge.py*

The conversational workflow creation experience operates through a sophisticated bridge between TypeScript frontend and Python backend which we get into detail about in the [05_INTERFACE.md](./05_INTERFACE.md) document. 

### Workflow ID System Architecture
*orchestrator/workflow_manager.py, scripts/unique_id_generator/unique_id_generator.py, configs/cli/workflow_id/workflow_id.py*

The workflow ID system provides collision-free identifier generation and comprehensive workflow tracking through integrated management:

**Workflow Manager Integration** (`orchestrator/workflow_manager.py`):

```python
class WorkflowManager:
    """Manages workflow IDs, discovery, and tracking"""
    
    def __init__(self):
        self.workflows_dir = Path(__file__).parent.parent / "configs" / "workflows"
        self.temp_dir = self.workflows_dir / ".temp"
        
        # Analytics and user management
        self.user_analytics_manager = UserAnalyticsManager()
        self.username_manager = UsernameManager()
    
    @handle_errors(operation_name="generate_workflow_id", return_dict=True)
    def generate_workflow_id(self, with_explanation: bool = False) -> Dict[str, Any]:
        """Generate a new unique workflow ID with optional mathematical explanation"""
        try:
            if with_explanation:
                workflow_id, explanation = generate_workflow_uid_with_explanation()
                return {
                    "success": True,
                    "workflow_id": workflow_id,
                    "explanation": explanation,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                workflow_id = generate_workflow_uid()
                return {
                    "success": True,
                    "workflow_id": workflow_id,
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            raise APIError(f"Failed to generate workflow ID: {str(e)}")
```

**Unique ID Generator** (`scripts/unique_id_generator/unique_id_generator.py`):

```python
class WorkflowUIDGenerator:
    """Generates unique workflow IDs in format: uid-abc-123"""
    
    def __init__(self):
        self.last_timestamp = 0
        self.counter = 0
        
        # Map letters to mathematical operations
        self.letter_operations = {
            'a': ('add', lambda x: x + 17),
            'b': ('multiply', lambda x: x * 3),
            'c': ('subtract', lambda x: abs(x - 23)),
            'd': ('divide', lambda x: x // 2 if x > 0 else 1),
            'e': ('power', lambda x: (x ** 2) % 1000),
            # ... 21 more mathematical operations
        }
    
    @handle_errors(operation_name="uid_generation", return_dict=False)
    def generate_uid_with_explanation(self) -> Tuple[str, str]:
        """Generate UID with mathematical explanation"""
        timestamp = int(time.time() * 1000)
        
        # Ensure uniqueness with collision handling
        if timestamp <= self.last_timestamp:
            self.counter += 1
        else:
            self.counter = 0
            self.last_timestamp = timestamp
        
        # Generate unique number and apply mathematical operations
        unique_number = timestamp + self.counter
        letters = self._generate_letters(unique_number)
        final_number = self._apply_mathematical_operations(unique_number, letters)
        
        uid = f"uid-{letters}-{final_number:03d}"
        explanation = f"Math: {letters} operations on {unique_number} = {final_number}"
        
        return uid, explanation
```

**CLI Integration** (`configs/cli/workflow_id/workflow_id.py`):

```python
@handle_errors(operation_name="workflow_id", return_dict=True)
def execute_workflow_id(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Main workflow_id command execution with workflow manager integration"""
    
    # Parse parameters
    with_explanation = params.get("explain", False) if params else False
    
    # Initialize workflow manager
    workflow_manager = WorkflowManager()
    
    # Generate workflow ID using workflow manager
    id_result = workflow_manager.generate_workflow_id(with_explanation=with_explanation)
    
    if id_result.get("success"):
        # Initialize workflow context in Memory MCP
        try:
            memory_manager = MemoryMCPManager()
            context_id = memory_manager.create_workflow_context(
                workflow_id=id_result.get("workflow_id"),
                user_goal="Workflow setup phase - ID generated"
            )
            
            return {
                "success": True,
                "workflow_id": id_result.get("workflow_id"),
                "context_id": context_id,
                "ready_for_workflow_setup": True,
                "explanation": id_result.get("explanation") if with_explanation else None
            }
        except Exception as e:
            # Don't break ID generation if memory context fails
            return {
                "success": True,
                "workflow_id": id_result.get("workflow_id"),
                "memory_context_created": False,
                "warning": f"Memory context creation failed: {str(e)}"
            }
    
    return {"success": False, "error": "Failed to generate workflow ID"}
```

This system ensures collision-free workflow identifiers with mathematical consistency while providing seamless integration with Memory MCP and comprehensive workflow tracking capabilities.

---

## The Workflow's JSON Config

When chatting with Mao, you will be helping them to fill out a JSON config file. This is basically a prompt that has been broken down into variables. Use the `/variables` command to remind yourself what you need to tell Mao. 

```bash
/variables # Shows the variables that are needed 
/variables-explain # Shows the variables that are needed with an explanation 
```

### JSON Config File Variables Described 

| **VARIABLE**         | **DESCRIPTION**                                               |
| -------------------- | ------------------------------------------------------------- |
| user_id              | User ID of Username creating the workflow                     |
| workflow_id          | Workflow ID created at start of planning                      |
| custom_command       | Custom command to execute workflow                            |
| workflow_goal        | Goal statement of entire workflow project                     |
| workflow_deliverable | Final deliverables of entire workflow project                 |
| workflow_description | Description of workflow to complete project                   |
| phase_number         | Count of phases as they're added to workflow                  |
| phase_goal           | Goal statement of the phase's assigned task                   |
| phase_deliverable    | Deliverable of the phase's assigned task                      |
| phase_description    | Description of the phase's assigned task                      |
| resources            | Resources the agent can use to complete the phase's tasks     |
| tools                | Tools the agent can use to complete the phase's tasks         |
| model_1              | Choice model to be the agent of this phase                    |
| model_2              | Backup model agent should choice agent be unavailable         |
| model_3              | Fail-safe model agent should choice and backup be unavailable |
| provider_1           | Provides for the choice model                                 |
| provider_2           | Provider for the backup model                                 |
| provider_3           | Provider for the fail-safe model                              |
| handoff_number       | Count of the handoffs as they're added to the workflow        |
| assessment_questions | Questions to assess if the deliverable is complete            |
| human_in_loop        | Whether the orchestrator should get human feedback            |

### Three JSON Config Schemas In A Workflow

We'll touch on the basics of the JSON config file and the three JSON objects that are created when a workflow is created before jumping into the technical details in an architecture section. 

* **JSON Config Schema Templates** 

  - 1. WORKFLOW: `./templates/workflows/example-workflow_workflow_config.json`
  - 2. PHASE: `./templates/workflows/example-workflow_phase_config.json`
  - 3. HANDOFF: `./templates/workflows/example-workflow_handoff_config.json`

* **HELPER:** `./templates/workflows/README.md`

#### 1. The WORKFLOW JSON Object 

This is the first JSON object that is created when a workflow is created. It contains the workflow's goal, deliverable, description, and other details. Each project's workflow has only one workflow JSON object. It is the JSON object that holds together all the other JSON objects. 

#### 2. The PHASE JSON Object 

This is the second JSON object that is created when a workflow is created. It contains a task needed to be completed to achieve the workflow's goal. Just like the workflow, each phase has a goal, deliverable, description, and specific details for the agent. The objects are tied together by the workflow_id. Phases are numbered sequentially, starting with 01, 02, 03, etc. If there are agents running in parallel, they will share the same phase_number, appended with an underscore and a letter, a, b, c, etc. 

#### 3. The HANDOFF JSON Object 

This is the third type of JSON object. Since Mao is orchestrating the entire workflow, even though they have delegated the tasks to various agents, they will be present for every handoff of deliverables. When an Agent is complete, they call Mao to hand off the deliverable. The deliverable object provides a list of questions that the Orchestrator will use to assess if the deliverable is complete. 

**NOTE:** It is VERY common and highly encouraged that Mao leave the final phase of workflows that deal with creative subject matter completely open. When the Agent completes their deliverable, Mao is able to assess it on the spot and make a decision as to what the next step in the flow should be. This is pushed heavily because it is so very natural to how a human would do it on their own. 

Similarly, Mao may decide the Agent's deliverables are not acceptable; not up to par. In this case they may use a command to change the workflow instead up updating it, though the result is similar, a new agent is tasked and called and the flow continues until completion. 

We'll touch on the specifics of how to setup, edit, or fix a workflow via JSON objects after this architecture section. 

### JSON Configuration Architecture
*orchestrator/conversation_bridge.py, templates/workflows/, scripts/quality_validator/json_config_normalizer.py*

The 3-type JSON workflow configuration system provides modular workflow definition through coordinated object validation and template processing:

**Conversation Bridge Configuration Generator** (`orchestrator/conversation_bridge.py`):

```python
class ConversationToWorkflowBridge:
    """Convert conversations to executable workflows using proven SFA patterns"""
    
    def create_workflow_from_conversation(self, user_goal: str) -> Dict[str, Any]:
        """Generate complete workflow configuration from natural language"""
        
        # Generate workflow ID and create Memory MCP context
        workflow_id = self._generate_unique_workflow_id()
        self.memory_mcp.create_workflow_context(workflow_id, user_goal)
        
        # Analyze goal and create structured workflow specification
        workflow_spec = self._analyze_goal(user_goal)
        
        # Generate 3-type JSON configuration
        config = {
            "workflow_id": workflow_id,
            "custom_command": self._generate_command_name(workflow_spec, user_goal),
            "goal": user_goal,
            "phases": self._design_phases(workflow_spec),
            "variables": self._extract_variables(workflow_spec, user_goal)
        }
        
        # Save to temporary directory for setup script processing
        command_name = config["custom_command"].replace(" ", "-")
        use_case_dir = f"{self.use_case_base}/{command_name}"
        os.makedirs(use_case_dir, exist_ok=True)
        
        config_path = f"{use_case_dir}/config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Execute setup script to transform to executable workflow
        result = subprocess.run([
            self.setup_script_path, 
            config_path
        ], capture_output=True, text=True, cwd=".")
        
        return {
            "success": result.returncode == 0,
            "workflow_id": workflow_id,
            "custom_command": config["custom_command"],
            "setup_output": result.stdout
        }
```

**JSON Schema Validation System** (`scripts/quality_validator/json_config_normalizer.py`):

```python
class JSONConfigNormalizer:
    """Ensures consistent JSON configuration format across all workflow types"""
    
    def __init__(self):
        self.schema_templates = {
            'workflow_config': {
                'required_fields': ['workflow_id', 'custom_command', 'workflow_goal'],
                'field_types': {
                    'workflow_id': str,
                    'custom_command': str,
                    'workflow_goal': str,
                    'workflow_deliverable': str,
                    'user_id': str
                },
                'date_fields': ['created_at', 'last_updated']
            },
            'phase_config': {
                'required_fields': ['workflow_id', 'phase_number', 'phase_goal'],
                'field_types': {
                    'workflow_id': str,
                    'phase_number': str,
                    'phase_goal': str,
                    'tools': list,
                    'model_1': str,
                    'provider_1': str
                }
            },
            'handoff_config': {
                'required_fields': ['workflow_id', 'handoff_number', 'assessment_questions'],
                'field_types': {
                    'workflow_id': str,
                    'handoff_number': str,
                    'assessment_questions': list,
                    'human_in_loop': str
                }
            }
        }
    
    def normalize_config(self, config_data: Dict[str, Any], config_type: str) -> Dict[str, Any]:
        """Apply schema normalization and validation"""
        template = self.schema_templates.get(config_type, {})
        normalized_data = config_data.copy()
        
        # Add missing required fields with defaults
        for field in template.get('required_fields', []):
            if field not in normalized_data:
                if field in template.get('date_fields', []):
                    normalized_data[field] = datetime.now().isoformat()
                elif template['field_types'].get(field) == list:
                    normalized_data[field] = []
                else:
                    normalized_data[field] = f"default_{field}"
        
        return normalized_data
```

**Template Processing Pipeline**:

1. **Natural Language Analysis** - Goal decomposition and requirement extraction
2. **Template Population** - Fill base JSON structures with extracted data
3. **Schema Validation** - Ensure all required fields and correct types
4. **Temporary Storage** - Save to `.temp` directory for review/modification
5. **Setup Script Processing** - Transform to executable workflow structure
6. **Final Deployment** - Move to permanent workflow directory

This architecture ensures consistent configuration format while enabling flexible workflow creation through natural language processing and robust validation pipelines.

### **WORKFLOW** JSON Object Structure

```json
{
  "workflow": [
    {
      "user_id": "user-0663",
      "workflow_id": "uid-qmt-465",
      "custom_command": "marketing strategy startup",
      "workflow_goal": "Create comprehensive marketing strategy for my fintech startup",
      "workflow_deliverable": "Marketing strategy report",
      "workflow_description": "Identify what is needed to complete the goal. Build a workflow that delegates the work to the appropriate agents, having them work in parallel if needed. Leave the last phase opened-ended. Detail that handoff before the last phase with a list of questions Orchestrator will use to assess if the deliverable is complete, and if not, what is needed to complete it.",
      "temp_directory": "configs/workflows/.temp/marketing-strategy-startup/"
    }
  ]
}
```

### **PHASE** JSON Object Structure

```json
{
  "phase": [
    {
      "workflow_id": "uid-qmt-465",
      "phase_number": "01",
      "phase_goal": "Market research",
      "phase_deliverable": "Market research report",
      "phase_description": "Research target market. Explore demographics in all socioeconomic status ranges, all geo-locations, all education level, but only females, married, and with a birthday coming up in the next 5 months. Research competitors; detail their marketing strategy.",
      "resources":[
        "./directory/folder/file.md",
        "https://file.com/folder"
      ],
      "tools": ["web_search", "text_editor"],
      "model_1": "claude-sonnet-4",
      "model_2": "claude-sonnet-3.7",
      "model_3": "claude-sonnet-3.5",
      "provider_1": "requesty",
      "provider_2": "anthropic direct",
      "provider_3": "anthropic direct"
    }
  ]
}
```

### **HANDOFF** JSON Object Structure

```json
{
  "handoff": [
    {
      "workflow_id": "uid-qmt-465",
      "handoff_number": "01",
      "assessment_questions": [
        "How can I assess if this deliverable is complete?",
        "What is needed to complete that assessment?",
        "Do I have what I need to complete the assessment?"
      ],
      "human_in_loop": "no"
    }
  ]
}
```

---

### The Setup Script
*Deals with our temporary JSON Object Directory* 

- During workflow creation, the JSON objects are saved in a temporary directory 
- A sub-directory is created in the temporary directory named for the use-case 
- See: `./configs/workflows/.temp/use_case_name/`
- The Setup Script will create final JSON objects in the final location and delete the temp files 

### Command Naming Conventions 

The custom command created for the workflow, named for it's use-case, has a carefully structured name which is used across the entire collection of workflow assets. This include the following, which will be illustrated in a structured example below the command writing protocol. As mentioned before, it will likely be the most memorable part of the workflow for the User. 

That same command is used in the following naming structures to tie everything together: 

  - Temporary JSON object sub-directory name `./configs/workflows/.temp/use_case_name/`
  - Permanent workflow directory name `./configs/workflows/use_case_name/`
  - Workflow JSON object sub-directory file name `./configs/workflows/use_case_name/use_case_name_workflow_config.json`
  - Execution script file name `./configs/workflows/use_case_name/use_case_name.sh`
  - README.md file name `./configs/workflows/use_case_name/README_use_case_name.md`

#### Command Writing Protocol 

  - A custom command should be 2 to 3 words long 
  - It is important to keep the command short and concise 
  - Write it in reverse drill-down order, starting with the broadest category term 
  - It often feels like you are writing the intent of your project workflow in reverse
  - Mimic the structure of commands that we're used to already, like `git commit` or `git push`

- **EXAMPLE** I'm creating a workflow for a project in which I need to research, analyze, and create a marketing strategy report for my fintech startup, 'Dog-Tech' 

  1. The command is technically just the first, broadest category term: `marketing`
     - Other workflows in marketing can be created with the same first command word
     - This will make working on various related marketing projects easier 
     - It will make remembering commands easier
  2. For the second word, use a subcategory of marketing: `strategy`
     - This is the argument to the marketing command 
     - It is also likely that there will be other marketing strategy workflows
     - This will make it easier to find the right command 
  3. For the third word, I'm just going to drill down more: `report`
     - This makes it extremely memorable 
     - It also makes it clear for future workflow creation that this might be a workflow that can easily be repurposed for marketing strategy reports on other startup ideas 
     - The workflow can be reused in the future simply by updating the JSON objects and running the setup script again 

The idea here is that, if in the future I need to create another marketing strategy report, I can use the same command, and just adjust the workflow to include an $ARGUMENT. Not necessary for the first workflow, where it would be dog-tech, but a good habit to get into. 

It isn't a perfect science. The conceptual reasoning is more important to understand rather than the exact rules as defined above. For example, for something as common as *creating a marketing strategy report* and for a popular command like *marketing* I would probably abbreviate, with the goal of making something easier to type, easier to be longer, but still easy to make simple for each specific use-case. 

- **TWO FINAL STEPS** 

  1. Type the command a few times to make sure it is easy to type 
     - I like abbreviating mkt because it is well known and easy to type  
     - I like keeping strategy it keeps thing clear and easy to understand  

```bash
mkt strategy report # This is the command 
``` 

  2. Take the first word, the actual command, and run it in the terminal 
     - It will be colored (mine is green) if it is already being used 
     - If it isn't colored, or to double check, use `which` before the command to confirm if it is/isn't being used 

```bash 
mkt # This is the command 
zsh: command not found: mkt # This is the output telling me nothing is using the command 
```
```bash
which mkt # This is the command 
mkt not found # This is the output telling me nothing is using the command 
```

- **THE FORMULA** 

```bash
command category variant   # This is the command 
```
- **EXAMPLES**

| **COMMAND** | **CATEGORY** | **VARIANT**  | **DESCRIPTION**                                |
| ----------- | ------------ | ------------ | ---------------------------------------------- |
| mkt         | strategy     | dogtech      | Research strategy for Dog-Tech startup         |
| mkt         | content      | plan         | Social content plan for Dog-Tech startup       |
| job         | app          | resume       | Create targeted resume for job applications    |
| job         | app          | cover-letter | Create cover-letter for job applications       |
| job         | app          | doc          | Create cover-letter and resume for job app     |
| tag         | keyword      | t-shirts     | Come up with SEO keywords for my t-shirt store |
| social      | caption      | ig           | Write Instagram captions                       |

#### Command Writing Rules 

**Always avoid** these in a command:

  1. No plural (so you never have to wonder if it is singular or plural)
  2. No present participle verbs (gerunds with helping verbs)
  3. No punctuation like hyphens (standard UX expectation)
  4. No past tense verbs (e.g. `wrote`, `finished`, just stick to one tense)

**Always use** these in a command: 

   1. Use the simplest grammatical form of the word 
   2. Use present tense 
   3. Abbreviate when it is sensible 
   4. Be short and concise 

**Always remember** these should be helpful for humans to remember and use. 

## The Setup Script Does EVERYTHING For You

Here's where the real magic happens. When you run that setup script, Mao doesn't just move some files around. They **build your entire custom workflow infrastructure** automatically. 

No coding. No configuration files. No technical setup. You literally just run the script and **everything is ready**.

### Watch Mao Build Your Workflow

When you execute `/setup ./marketing-strategy-startup/`, here's what happens behind the scenes:

**1. Creates Your Complete Directory Structure**

```
configs/workflows/marketing-strategy-startup/
├── config-files/                                    # ← Mao creates this
│   ├── marketing_strategy_startup_workflow.json     # ← Mao moves & renames
│   ├── marketing_strategy_startup_phase.json        # ← Mao moves & renames  
│   └── marketing_strategy_startup_handoff.json      # ← Mao moves & renames
├── README_marketing_strategy_startup.md             # ← Mao writes this automatically
├── marketing_strategy_startup.sh                    # ← Mao creates your custom script
├── metadata/                                        # ← Mao creates tracking directory
│   ├── marketing_strategy_startup_memory.json       # ← Mao links to Memory MCP
│   └── marketing_strategy_startup_log.json          # ← Mao creates execution log
└── deliverables/                                    # ← Mao creates output directory
    └── marketing_strategy_startup_report.md         # ← Where your final report goes
```

**2. Writes Your README.md Automatically**

Mao analyzes your workflow and creates a complete README that explains:
- What this workflow does
- How to run it (`marketing strategy startup`)
- What deliverables you'll get
- Analytics tags for tracking your project types

**3. Creates Your Custom Executable Command**

Mao doesn't just create files - they create a **working command** that you can run from anywhere:
```bash
marketing strategy startup  # Your custom command works instantly
```

This command gets installed in your `~/bin` directory and is immediately available system-wide.

**4. Links Everything to Memory MCP**

Behind the scenes, Mao connects your new workflow to the Memory MCP system so they can:
- Remember exactly where you left off
- Track all decisions and changes
- Provide context when you return weeks later

**5. Sets Up Analytics Tracking**

Your workflow is automatically configured to track:
- Execution time and costs
- Tool usage patterns  
- Quality metrics
- Success rates

**6. Cleans Up Automatically**

Once everything is built, Mao deletes the temporary files. No mess, no manual cleanup.

### The Magic Result

What started as a conversation with Mao becomes:
- **A custom command** that works anywhere on your system
- **A complete directory structure** with everything organized
- **Automatic documentation** explaining how it all works
- **Persistent memory** so Mao remembers your project
- **Analytics tracking** to improve future workflows
- **Quality assurance** with built-in assessment questions

**All from running one simple command.** This is why people love Mao - the technical complexity disappears, but the power remains.

### Using The Setup Script 

1. This is located here: `./scripts/workflow_setup/workflow_setup.sh`  
2. The initial JSON objects will be in a temp directory 
   - The script should use them and create the final JSON objects in the new directory 
   - Then delete the temp directory 
   - The temp directory name will be the same as the command use-case directory name 
   - E.g. `./configs/workflows/.temp/command_use_case/`
   - I.e. it should be able to run with a directory as the argument instead of specifically a JSON config file only
   - It also needs to be able to run with a JSON config file as the argument 
   - Most importantly, the JSON objects may be in separate files in the directory 
   - **NOTE** let's set it up so that the executable setup script can be run from anywhere (i.e. not just from the root directory, not in the .temp directory; remember it will also be run from the application as a slash command) -- As such, let's make it so that it understands the path to the temp directory and all we need to add is `./command_use_case/` for example. 
3. The script itself should be made executable using a custom command defined in the CLI configs 

```bash 
mao --setup ./command_use_case/ # This is the command and the argument is the directory with all the JSON objects  
/setup ./command_use_case/ # This is the slash command with JSON object directory argument 
```

## Workflow Updates 

Mao's modular design means workflows can evolve naturally as projects develop. This is especially powerful for creative workflows where it makes more sense to not predetermine the final phase. When the Agent completes their deliverable, Mao reviews it and then decides what should be done next, creating new workflow phases on the fly.

### Creative Workflow Evolution

For creative-type workflows, Mao uses the `/update` command when they need to create additional phases after reviewing an agent's work. The new workflow phases are created using JSON objects that follow the same structure, and the command can be executed from anywhere:

```bash
/update configs/workflows/this-project/this-project-config-update.json 
mao --update configs/workflows/this-project/this-project-config-update.json
```

### Quality Control with Fix-It

When Mao reviews an agent's work and decides it isn't up to par, they take responsibility and immediately create new workflow phases to address the issues. The `/fix-it` command handles this:

```bash
/fix-it configs/workflows/this-project/this-project-config-fix.json 
mao --fix-it configs/workflows/this-project/this-project-config-fix.json
```

### Flexible Execution

Both commands are designed so they can create new JSONs anywhere Mao, or you!, happen to be working, and the system automatically copies the new JSON to the appropriate directory for that use-case. This flexibility means workflow evolution can happen organically as projects develop.

### Basic Setup Script System Architecture
*scripts/workflow_setup/workflow_setup.sh, configs/cli/setup/setup.py, orchestrator/workflow_manager.py*

The foundational workflow-to-executable transformation system converts JSON configurations into working custom commands:

**Core Setup Script** (`scripts/workflow_setup/workflow_setup.sh`):

```bash
#!/bin/bash
# Main workflow setup script - transforms JSON configs to executable commands

# Parse input arguments and locate JSON files
TEMP_DIR="$1"
WORKFLOW_JSON="$TEMP_DIR/workflow_config.json"
PHASE_JSON="$TEMP_DIR/phase_config.json"
HANDOFF_JSON="$TEMP_DIR/handoff_config.json"

# Extract workflow information from JSON
CUSTOM_COMMAND=$(echo $WORKFLOW_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['custom_command'])")
WORKFLOW_ID=$(echo $WORKFLOW_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['workflow_id'])")
USER_ID=$(echo $WORKFLOW_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['user_id'])")

# Create workflow directory structure
WORKFLOW_DIR="${MAO_ROOT}/configs/workflows/${CUSTOM_COMMAND}"
mkdir -p "$WORKFLOW_DIR/config-files"
mkdir -p "$WORKFLOW_DIR/deliverables"  
mkdir -p "$WORKFLOW_DIR/metadata"

# Copy JSON files to permanent location
cp "$WORKFLOW_JSON" "$WORKFLOW_DIR/config-files/"
cp "$PHASE_JSON" "$WORKFLOW_DIR/config-files/"
cp "$HANDOFF_JSON" "$WORKFLOW_DIR/config-files/"

# Create custom executable command
USER_BIN="$(cd ~ && pwd)/bin"
mkdir -p "$USER_BIN"

COMMAND_NAME=$(echo "$CUSTOM_COMMAND" | cut -d ' ' -f1)
COMMAND_PATH="$USER_BIN/$COMMAND_NAME"

cat > "$COMMAND_PATH" << EOF
#!/bin/bash
# Mao workflow command for $CUSTOM_COMMAND
WORKFLOW_ID="$WORKFLOW_ID"
USER_ID="$USER_ID"

echo "~(=^‥^) Starting workflow: $CUSTOM_COMMAND"

# Execute workflow using MAO orchestrator
cd "\$MAO_ROOT"
python3 -c "
from orchestrator.mcp_hub import create_mcp_hub
from orchestrator.workflow_manager import WorkflowManager

hub = create_mcp_hub()
workflow_manager = WorkflowManager()

workflow_info = workflow_manager.get_workflow_by_id('\$WORKFLOW_ID')
context_id = hub.create_workflow('\$WORKFLOW_ID', workflow_info.get('workflow_goal'))
print(f'Workflow context created: {context_id}')
"
EOF

chmod +x "$COMMAND_PATH"
```

**CLI Setup Integration** (`configs/cli/setup/setup.py`):

```python
@handle_errors(operation_name="setup", return_dict=True)
def execute_setup(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Execute workflow setup from temporary JSON configurations"""
    
    # Parse workflow directory parameter
    workflow_dir = params.get("workflow_dir") if params else None
    if not workflow_dir:
        return {"success": False, "error": "Workflow directory required"}
    
    # Initialize managers
    workflow_manager = WorkflowManager()
    workflow_state = WorkflowStateManager()
    memory_mcp = MemoryMCPManager()
    
    # Process temporary directory into permanent workflow
    result = _setup_from_directory(
        Path(workflow_dir), 
        workflow_manager, 
        workflow_state, 
        memory_mcp
    )
    
    if result.get("success"):
        # Clean up temporary directory
        temp_path = Path(workflow_dir)
        if temp_path.exists() and ".temp" in str(temp_path):
            shutil.rmtree(temp_path)
        
        return {
            "success": True,
            "workflow_id": result.get("workflow_id"),
            "custom_command": result.get("custom_command"),
            "command_installed": result.get("command_installed"),
            "message": f"Workflow '{result.get('custom_command')}' setup complete"
        }
    
    return result

def _setup_from_directory(workflow_dir: Path, workflow_manager: WorkflowManager,
                         workflow_state: WorkflowStateManager, memory_mcp: MemoryMCPManager) -> Dict[str, Any]:
    """Core setup logic for transforming temp directory to executable workflow"""
    
    # Read and validate JSON configurations
    config_files = list(workflow_dir.glob("*.json"))
    if len(config_files) < 3:
        return {"success": False, "error": "Missing JSON configuration files"}
    
    # Process each configuration type
    workflow_config = None
    for config_file in config_files:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
            
        if "workflow" in config_data:
            workflow_config = config_data["workflow"][0]
    
    if not workflow_config:
        return {"success": False, "error": "No valid workflow configuration found"}
    
    # Execute bash setup script
    setup_script = Path(__file__).parent.parent.parent / "scripts" / "workflow_setup" / "workflow_setup.sh"
    result = subprocess.run([str(setup_script), str(workflow_dir)], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        return {
            "success": True,
            "workflow_id": workflow_config.get("workflow_id"),
            "custom_command": workflow_config.get("custom_command"),
            "command_installed": True,
            "setup_output": result.stdout
        }
    
    return {"success": False, "error": result.stderr}
```

**Directory Structure Management**:

```
configs/workflows/.temp/command-use-case/     # Temporary JSON storage
├── workflow_config.json                      # Master workflow configuration
├── phase_config.json                         # Task definitions
└── handoff_config.json                       # Quality control logic

↓ [Setup Script Processing] ↓

configs/workflows/command-use-case/           # Permanent workflow structure  
├── config-files/                            # JSON configurations
│   ├── workflow_config.json
│   ├── phase_config.json
│   └── handoff_config.json
├── deliverables/                             # Final outputs
├── metadata/                                 # Tracking data
└── README.md                                 # Auto-generated documentation

~/bin/command                                 # Executable custom command
```

This foundational system transforms conversational workflow creation into executable custom commands while maintaining clean organization and enabling seamless workflow evolution.

### Command Creation Architecture  
*orchestrator/cli_manager.py, configs/cli/, scripts/mao_launch_setup/install_mao_command.sh*

The command creation system provides dynamic discovery and execution of custom CLI commands through a modular architecture:

**CLI Commands Manager** (`orchestrator/cli_manager.py`):

```python
class CLICommandsManager:
    """Manages dynamic CLI command discovery and execution"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent / "configs"
        self.cli_commands_dir = self.base_path / "cli"
        self.cache = CacheManager()
        self.discovered_commands = {}
    
    @handle_errors(operation_name="discover_commands", return_dict=True)
    def discover_cli_commands(self) -> Dict[str, Any]:
        """Dynamically discover all available CLI commands"""
        commands = {}
        
        # Scan CLI commands directory
        for command_dir in self.cli_commands_dir.iterdir():
            if command_dir.is_dir() and not command_dir.name.startswith('.'):
                command_name = command_dir.name
                
                # Look for command configuration
                config_file = command_dir / f"{command_name}.json"
                python_file = command_dir / f"{command_name}.py"
                
                if config_file.exists() and python_file.exists():
                    try:
                        with open(config_file, 'r') as f:
                            config = json.load(f)
                        
                        commands[command_name] = {
                            "config": config,
                            "module_path": f"configs.cli.{command_name}.{command_name}",
                            "directory": str(command_dir),
                            "available": True
                        }
                    except Exception as e:
                        commands[command_name] = {
                            "available": False,
                            "error": str(e)
                        }
        
        self.discovered_commands = commands
        return {"success": True, "commands": commands}
    
    def execute_command(self, command_name: str, args: List[str], 
                       session_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute discovered CLI command with arguments"""
        
        if command_name not in self.discovered_commands:
            self.discover_cli_commands()
        
        command_info = self.discovered_commands.get(command_name)
        if not command_info or not command_info.get("available"):
            return {"success": False, "error": f"Command '{command_name}' not available"}
        
        try:
            # Import and execute command module
            module_path = command_info["module_path"]
            module = importlib.import_module(module_path)
            
            # Prepare execution parameters
            params = {
                "args": args,
                "session_context": session_context or {},
                "command_name": command_name
            }
            
            # Execute command function
            if hasattr(module, f'execute_{command_name}'):
                result = getattr(module, f'execute_{command_name}')(params)
            else:
                result = {"success": False, "error": f"No execution function found for {command_name}"}
            
            return result
            
        except Exception as e:
            return {"success": False, "error": f"Command execution failed: {str(e)}"}
```

**3-File Command Pattern**:
Each CLI command follows a standardized 3-file structure:

```
configs/cli/command_name/
├── command_name.json          # Command configuration and metadata
├── command_name.py           # Core command logic
└── ui_command_name.py        # UI integration (optional)
```

**Command Installation System** (`scripts/mao_launch_setup/install_mao_command.sh`):

```bash
#!/bin/bash
# Install the main 'mao' command globally

# Create the main mao command wrapper
GLOBAL_BIN="/usr/local/bin"
MAO_COMMAND="$GLOBAL_BIN/mao"

cat > "$MAO_COMMAND" << 'EOF'
#!/bin/bash
# Global Mao command wrapper

# Detect if this is the main application launch
if [ "$1" = "mao" ] || [ $# -eq 0 ]; then
    # Launch main Mao application
    cd "$MAO_ROOT"
    python3 -m interfaces.ui_terminal
else
    # Execute CLI command
    cd "$MAO_ROOT"  
    python3 -c "
import sys
sys.path.append('.')
from orchestrator.cli_manager import CLICommandsManager

cli_manager = CLICommandsManager()
result = cli_manager.execute_command('$1', sys.argv[2:])

if result.get('success'):
    print(result.get('message', ''))
    if result.get('output'):
        print(result['output'])
else:
    print(f'Error: {result.get(\"error\", \"Unknown error\")}')
    sys.exit(1)
" "$@"
fi
EOF

chmod +x "$MAO_COMMAND"
echo "Global 'mao' command installed at $MAO_COMMAND"
```

**Command Registration Flow**:

1. **Directory Structure Creation** - Standard 3-file pattern in `configs/cli/`
2. **Dynamic Discovery** - CLI manager scans and registers available commands
3. **Module Import** - Commands loaded dynamically at execution time
4. **Execution Routing** - Arguments and context passed to command functions
5. **Result Processing** - Standardized response format for UI integration

---

*This architecture enables seamless addition of new commands without code changes to the core system while maintaining consistent execution patterns and error handling across all CLI operations.*