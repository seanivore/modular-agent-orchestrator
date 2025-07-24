# Section III: Setting Up a Project for Mao 
*Walkthrough of a first-time user's experience* 

---

You're ready to automate your life. Advanced agentic orchestration, delegating to subagents working in parallel, fully compatible with any LLM model, it all sounds great. But you know what sounds better? *No learning curve.* Mao is here. Not just to help you, but to totally take over for you ~(=^‥^)

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
```
#     │      │  │
#     │      │  └── Scoped package name  
#     │      └────── Install globally (system-wide)
#     └───────────── Package manager

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
    mao --login # Launches with the Username field available 
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

- The system checks to see if the UserID already exists 
- New user login creates `./configs/user/username/user_username.json` file 
- A UserID will always be the same for a specific Username 
- Subdirectories and files include preference, memories, analytics, and other data 
- Workflows are stored in the `./configs/workflows/` directory and only include the UserID 
- Search for workflows orchestrated Management files 

### `meid` Script Code 

```python 
        # Generate user_id using meid script
        try:
            user_id = generate_user_id(username)
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
  Uses character count, doubled count, and ASCII values
  Applies fibonacci, golden ratio, spiral, mirror, karmic operations
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

### Core Memory Management Components **NOT ACCURATE NEEDS TO BE UPDATED**

```python
# orchestrator/memory_mcp.py - Memory integration hub
class MemoryMCPManager:
    def __init__(self):
        self.memory_client = MemoryMCPClient()
        self.cache = CacheManager()
        
    async def save_workflow_context(self, workflow_id: str, context: Dict[str, Any]):
        """Save complete workflow state to knowledge graph"""
        workflow_entity = {
            "name": f"workflow_{workflow_id}",
            "type": "workflow_context",
            "observations": [
                f"Goal: {context['goal']}",
                f"Status: {context['status']}",
                f"Current Phase: {context['current_phase']}",
                f"Deliverables: {json.dumps(context['deliverables'])}"
            ]
        }
        await self.memory_client.create_entities([workflow_entity])
        
    async def restore_workflow_context(self, workflow_id: str) -> Dict[str, Any]:
        """Restore workflow state from knowledge graph"""
        nodes = await self.memory_client.search_nodes(f"workflow_{workflow_id}")
        return self._parse_workflow_context(nodes)
```

### Session State Persistence

```python
# orchestrator/user_memory_manager.py - User session management
class UserMemoryManager:
    def __init__(self, username: str):
        self.username = username
        self.user_config_path = f"configs/user/{username}/user_{username}.json"
        self.memory_mcp = MemoryMCPManager()
        
    def save_session_state(self, session_data: Dict[str, Any]):
        """Persist current session context"""
        session_entity = {
            "name": f"session_{self.username}_{datetime.now().isoformat()}",
            "type": "user_session",
            "observations": [
                f"Active workflows: {session_data['active_workflows']}",
                f"Current focus: {session_data['current_focus']}",
                f"Preferences: {json.dumps(session_data['preferences'])}"
            ]
        }
        self.memory_mcp.create_entities([session_entity])
        
    def get_user_context(self) -> Dict[str, Any]:
        """Retrieve complete user context for session restoration"""
        user_nodes = self.memory_mcp.search_nodes(f"session_{self.username}")
        return self._compile_user_context(user_nodes)
```

### Workflow ID System Architecture

```python
# orchestrator/workflow_manager.py - Workflow identification and tracking
class WorkflowManager:
    def generate_workflow_id(self) -> str:
        """Generate unique workflow identifier"""
        import uuid
        timestamp = int(time.time())
        unique_id = str(uuid.uuid4())[:8]
        return f"wf-{timestamp}-{unique_id}"
        
    def create_workflow_context(self, goal: str, user_id: str) -> Dict[str, Any]:
        """Create initial workflow context with memory integration"""
        workflow_id = self.generate_workflow_id()
        context = {
            "workflow_id": workflow_id,
            "user_id": user_id,
            "goal": goal,
            "created_at": datetime.now().isoformat(),
            "status": "planning",
            "phases": [],
            "memory_context": {}
        }
        
        # Save to Memory MCP immediately
        self.memory_mcp.save_workflow_context(workflow_id, context)
        return context
```

### Cross-Session Data Flow

The memory system creates a continuous data flow that persists across sessions:

1. **Session Start**: System queries Memory MCP for user context and active workflows
2. **Ongoing Work**: All interactions, decisions, and progress automatically saved to knowledge graph
3. **Session End**: Current state persisted with timestamp and context markers
4. **Session Resume**: Previous context restored with full workflow state and user preferences

This architecture enables the "always on the same page" experience that makes Mao feel like a persistent team member rather than a stateless tool.

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
 ❯ 3. Dark mode (CVD)✔
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

- Want to set up new settings for the application? 
- Ask Mao what files are needed, they'll do the rest  
- EXAMPLE: Add a new setting that says "Bark like a dog when workflow is done y/n?" --> Magic. 

---

| **ADD ARCHITECTURE HERE** |
| ------------------------- |

## Login, Theme & Application Settings **ARCHITECTURE** 

| **END ARCHITECTURE SECTION** |
| ---------------------------- |

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
│ > Try "how do we start building?"                 │
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
│ > some rough notes to |                           │
╰───────────────────────────────────────────────────╯
  ?  /variables to see what is needed 
```

### Tell Mao About Your Project 

- Chat is flexible; Mao will chat like any AI model. Treat Mao like an employee. Provide as much or as little detail as you want. 

- Mao is not trained with any scripts; they are simply an expert in turning projects into tasks and then into a workflow 

**A goal is all Mao needs**

- The minimum Mao needs is to know your goal! 
- Mao will get an inital workflow create for you 
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
uid # Creates a new unique Workflow ID 
mao --workflow uid-abc-000 # Shows workflow details 
/uid # Creates a new unique Workflow ID 
/workflow uid-abc-000 # Shows workflow details 
```

### Mao's "One Source of Truth"

Here's how Mao is able to always be on the same page as you. 

**The Memory MCP tool gives Mao a Persistant Vector Graph "memory" for context between sessions**

* The Workflow ID is for you 
  - It identifies your workflow and connects it to your UserID and Username 
  - Every new project, Mao will create a new Workflow ID 
* The Workflow ID is for Mao 
  - Mao tags memory context updates with the Workflow ID, keeping all information about the project together 
  - If you get inturrupted, Mao uses the workflow ID to know exactly where to pick up
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

---

| **ADD ARCHITECTURE HERE** |
| ------------------------- |

## Chatting with Mao, the UI options, Workflow ID, Using Memory MCP **ARCHITECTURE** 

This is the first introductory half of creating a workflow for their project. What the experience will look like. What they will need to do, or how little they'll need to do. We touch on how Mao is able to always be on the same page using the Memory MCP tool as well as Workflow ID. 

| **END ARCHITECTURE SECTION** |
| ---------------------------- |

---

## The Workflow's JSON Config
 
When chatting with Mao, you will be halping them to fill out a JSON config file. This is basically a prompt that has been broken down into variables. Use the `/variables` command to remind yourself what you need to tell Mao. 

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

---

| **ADD ARCHITECTURE HERE** |
| ------------------------- |

## The Workflow's JSON Config **ARCHITECTURE** 

This is the first half of the workflow setup details, specifically about the JSON config file. It should cover everything up to and NOT including the setup script itself. In the section to follow we'll talk about the setup script along with the commands used to create the workflow. 

### **WORKFLOW** JSON Object 

- This is the first JSON object that is created when a workflow is created 
- It contains the workflow's goal, deliverable, description, and other details 
- Each project's workflow has only one workflow JSON object 
- The 'goal', 'deliverable', and 'description' are all items that will be broken down into the phases 
- The objects are tied together by the workflow_id 
- While building the workflow, the temp_directory is used to store the JSON objects, the management of this file is explained later

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

### **PHASE** JSON Object 

- This is the second JSON object that is created when a workflow is created 
- It contains a task needed to be completed to achieve the workflow's goal 
- Just like the workflow, each phase has a goal, deliverable, description, and specific details for the agent 
- The objects are tied together by the workflow_id 
- Phases are numbered sequentially, starting with 01, 02, 03, etc. 
- If there are agents running in parallel, they will share the same phase_number, appended with an underscore and a letter, a, b, c, etc. 

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

### **HANDOFF** JSON Object 

- This is the third type of JSON object that is created when a workflow is created 
- This is created while building the workflow as part of the creative process 
- When the assessment is being discussed, it is important to get it written down in real time 
- This object also helps provide important indicators to the orchestrator or the User watching the workflow 
- For example, if there is a human in the loop, the orchestrator will need to know when to get human feedback 
- Additionally, the handoff object is important when the subsequent phases have been left open-ended, where the handoff object is used as a placeholder and indicator that the Orchestrator needs to make a decision and then build the rest of the workflow accordingly 
- Note that there might be more than one phase created after a handoff, there is no hard rule 

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

| **END ARCHITECTURE SECTION** |
| ---------------------------- |

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
     - This makes it extrememly memorable 
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

### Setup Script Automations 

When the workflow is created, you need to run the JSON config file(s) through the setup script. This will create the following: 

1. Create a new directory in the `configs/workflows/command_use_case/` directory 
2. Place a new JSON config file in the new directory 
   - Built from the .temp directory 
   - Then deletes the .temp directory 
3. Produces a README.md file in the new directory 
   - Describes the workflow
   - Reminds the user how to activate the workflow 
   - Also creates categorical tags about the workflow project to be used in analytics 
4. Creates executable script with all the details of the workflow 
   - This is the script that will be used to run the workflow 
   - Finally, we have a script that is specific and not generic 
5. Make the script executable using the custom command 
   - Creates it using the tool `chmod +x` 
   - Script runs `chmod +x ./configs/workflows/command_use_case/command_use_case.sh` 
   - Saves the command to your ~/bin directory 
6. Creates new sub-directories for 
   - Deliverables 
   - Metadata 
   - **This is all automated**

**NOTE:** It is important to remember that the drafting documents used in the workflow are kept in the Files API and not passed along with the deliverables. If you NEED draft documents, you will need to list them as deliverables. 

#### Workflow Directory Structure

  - Automatically created by the setup script 
  - Command naming structure across files 

```
configs/workflows/command_use_case/
├── config-files/                                 # Directory for JSON config files 
│   ├── command_use_case_workflow_config.json     # Workflow JSON config file 
│   ├── command_use_case_phase_config.json        # Phase JSON config file 
│   └── command_use_case_handoff_config.json      # Handoff JSON config file 
├── README_command_use_case.md                    # Auto-generated usage guide
├── command_use_case.sh                           # Auto-generated use-case specific script that your command activates 
├── metadata/                                     # Workflow tracking details  
│   ├── command_use_case_memory.json              # Workflow Memory MCP File  
│   └── command_use_case_log.json                 # Workflow log file 
└── deliverables/                                 # Final outputs; this is where the deliverables are stored 
    └── command_use_case_report.md                # This is the final deliverable; it is the report 
```

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

---

| **ADD ARCHITECTURE HERE** |
| ------------------------- |

The Setup Script 
Workflow Updates 

*Details about how the setup script works, referencing:*
- `./scripts/workflow_setup`
- `./versioning/v4/v4_0_0/implemented-workflow-setup/TASK_4_WORKFLOW_CREATION_COMPLETE.md`
*Reference: `./archive/OGDOCS_7_USER_GUIDE.md` contains additional details*

| **END ARCHITECTURE SECTION** |
| ---------------------------- |

