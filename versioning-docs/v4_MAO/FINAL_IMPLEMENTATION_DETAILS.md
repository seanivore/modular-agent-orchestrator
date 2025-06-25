# Implementation Items 

---

## 1. Application Configuration Settings Config 

1. Our current list of settings has already been created in a single JSON file 
2. File to breakdown: `./configs/settings/application_settings_schema.json` 
3. Please add this as a rule to the tech documentation 
   - All JSON config files should always be stand-alone files
   - This is what makes them truely modular, easy to add a new one, remove an old one, or update an existing one 
   - System files can pull the contents of the entire directory and dispaly it as a single list 
4. Please breakdown the `application_settings_schema.json` file into individual `setting_name_app_settings.json` files 
5. Place a template copy of the `setting_name_app_settings.json` file in the `./configs/examples/` directory 
6. Create implementation plan for the use, creation, and updating of the application settings pulling from the `./configs/settings/` directory 
7. Implement the plan 
8. Document all  of the above 

---

## 2. Setup User ID Config 

1. Create `./configs/user/` directory 
2. Create `./configs/user/user_username.json` template file and place it in the `./configs/examples/` directory 

**For truely comprehensive workflow, see the `NEW_USER_FLOW.md` document section on User IDs**

#### User Settings Schema (because of additions of new settings, the schema should be updates from this version so that it *ONLY* includes the settings that the user changed away from the default settings) 

```json
{
  "username": "seanivore",
  "user_id": "user-1642", 
  "quick_launch": "always",
  "favorite_model": "claude-sonnet-4",
  "default_provider": "anthropic direct",
  "theme": "dark mode CVD",
  "cat_vibes": "I love it",
  "double_texting": "always",
  "tone_notification": "once, no push"
}
```

### User ID Config Lifespan 

  1. When a new user logs in, they are prompted to choose a Username to always use in the application 
  2. Our `meid` command is a user ID generator that will always create the same user ID for a specific Username
     - It can be found here, python file: `./scripts/user_id_generator/user_id_generator.py`
     - And the install command script: `./scripts/user_id_generator/install_meid_command.sh` 
     - This will need to be integrated into the application 
     - However we also want Users to be aware they can run it as a CLI command if they happen to be creating a JSON without AI help 
  3. The `user_username.json` file is created in the `./configs/user/` directory 
  4. As a new user they are prompted to adjust their configuration settings from defaults 
  5. All the user's settings are saved to the `user_username.json` file 
  6. The application should load these setting in sequential launches unless they logout 
  7. If logged out, entering their username will pull up their `user_username.json` file and load the settings from it (not asking them to adjust settings again)
  8. Help notes around the app or in the /help command screen show using `/config` or launching with `mao --config` let's them adjust settings directly which updates their `user_username.json` file 

### Implementation 

1. Create implementation plan for the use, creation, and updating of the `user_username.json` files 
2. Include logic that the user settings only record changes from the default settings; this will make it easy when we add new settings to the application because all of the User's settings JSON files won't have to be updated until they decide to change a setting 
3. Implement the plan 
4. Discovery system for the user settings 
5. Document all of the above 

---

## 3. Workflow Unique ID 

1. Similar to the User ID except these will give you a different unique ID every single time you run the `uid` command 
2. You can see in the `NEW_USER_FLOW.md` that the workflow ID is one of the first things Mao does in the chat 
3. The workflow ID is on the JSON config workflow objects 
4. Mao uses the same workflow ID to tie together the workflow log, and is the entity used in the Memory MCP that ties everything they do together 
5. Users making a JSON objects on their own should be aware that they can run the command `uid` to get a unique ID to put on the objects  
6. This script will need to be implemented into the application 
   - It can be found here, python file: `./scripts/unique_id_generator/unique_id_generator.py` 
   - And the install command script: `./scripts/unique_id_generator/install_uid_command.sh`
7. Please create this implementation plan 
8. Implement the plan 
9. Document all of the above 

---

## 4. Workflow Creation 

1. The workflow creation is the best way to illustrate building a workflow 
2. Show the Use-Case JSON being built 
3. The logic for the different types of JSON objects to use depending on the use-case and chosen workflow 
4. The fact that the workflow JSON objects are all named using the same custom command naming convention, including the .temp directory 
5. The storage of the workflow JSON objects in the .temp sub-directory until the workflow planning is complete and ready to be setup 
6. The setup script and all of its automations, creating the new directory, making new JSON object copies, deleting the .temp directory, creating the use-case-specific executable script, making the command executable, creating the use-case README 

### Use-Case JSON Object 

1. Collect the three types of JSON objects from the `NEW_USER_FLOW.md` document 
2. Create implementation plan for the use, creation, and updating of the workflow JSON objects 
3. Reference the workflow described in the `NEW_USER_FLOW.md` document 
4. Template copies of each JSON object are alreaday in the `./configs/workflows/json_object_templates/` directory 

### The Setup Script 

1. Collect the details from the `NEW_USER_FLOW.md` document 
2. Create implementation plan for the use, creation, and updating of the workflow JSON objects 
3. Remember the pre-planned commands for setup, update, and fix-up scripts 
4. Use the SFA scripts as a reference for creating the scripts 
   - One script to setup the ability to run the setup script from anywhere simple commands like `/setup use_case_config.json` or `mao --setup use_case_config.json`
   - The second script is what the first script activates; it runs and creates all the automations mentioned above 
5. Pay special attention to the protocol for create custom commands 
6. The biggest change to the setup script is that there are 3 types of JSON objects, and that the User/Orchestrator may need to change the workflow mid-workflow; all of this is outlined in the `NEW_USER_FLOW.md` document 
7. Please create this implementation plan 
8. Implement the plan 
9. Document all of the above, including the JSON objects use and the setup script 

---

## 5. Leftover From Integration Plan Notes 

These were held over because of their relevance to the remaining implementation items that were detailed on the `NEW_USER_FLOW.md` document. 

### Confirm 'Orchestrator Integration' Re:
  - Connect `goal()` method to real `WorkflowOrchestrator` --> cannot find this term in codebase so must not be done 
  - Implement workflow state management for continue/review
  - Add real cost tracking and progress monitoring 

### Confirm 'File System Integration' Re:
  - Connect setup/update commands to actual JSON workflow processing
  - Implement workspace management for deliverable organization --> explain? 
  - Add file validation and error handling --> for? the CLI arguments and slach commands? 

### Confirm 'Real-Time Features' Re:
  - Connect stats to actual system metrics
  - Implement live workflow monitoring
  - Add progress bars and execution tracking 
    --> Probably do not need progress bars for execution tracking specifically, as we should leave these UI items to actual development of the UI, however we definitely still need the live stats and system metrics coming through for whatever the UI that is developed. 

---

## 6. Updating Any / All Config Collections 

  1. Making our system truely 'plug-and-play' is a big deal 
  2. All config collections should be well documented 
  3. All config JSON objects should have templates easily avaialable 

### PROBLEM 

  - Configs can be updated in real-time 
  - We need the application to always display accurate config lists if a User pulls up the tools or help to see the arguments, etc. 
  - We need our documentation to be updated as well.
  - This must be done automatically, agentically 

### SOLUTION 

  - Claude Code TIP from today
  - Run /install-github-app to tag @claude right from your Github issues and PRs
  - We need to learn how to use this 
  - It will inevitably be beneficial FAR beyond this one use case 
  - But it will perfectly solve our needs for documentation 
  - Digitally, the application will need to populate the list of config collection objects live, ever time it is called 

### Implementation 

1. Create implementation plan for the use, creation, and updating of the config collection objects 
2. Implement the plan 
3. Document all of the above 

---

## 7. Technical Documentation 

### Notable Gaps 

1. On `2_MAO_SYSTEM_FILES.md` at LINE 159 "### ORCHESTRATION: Epic Memory `orchestrator/memory_mcp.py` Recall" needs details from implementation 

2. On `3_MAO_ARCHITECTURE.md` at LINE 270 "# interfaces/terminal/conversation_interface.py" is not a file that exists 

3. On `3_MAO_ARCHITECTURE.md` at LINE 509 "Setup script processes config and creates executable command" needs to be updated with the real setup script (see `NEW_USER_FLOW.md` to finalize this an JSON), 618 the JSON can be placed 

### Full Documentation Audit 

After all items are implemented, I'd like to do a full documentation audit. All documents should be reviewed carefully, first one at a time, then all together. There are currently many overlaps and, reading them straight through is a bit of a challenge. This should be our end goal: that they can be read straight through without confusion. 

---

## 8. Revamp the Claude Code Foundation UI Specs  

1. Given the detailed, thorough, and visual `NEW_USER_FLOW.md` document 
2. Because we also have everything else implemented now 

**I'm hoping that the vibe of the visuals and even the copywriting will speak through the `NEW_USER_FLOW.md` document** 
  - Do we include this file itself in the Claude Code SPEC.md files? 
  - Do we try to integrate it into the SPEC.md files? 

**FOR REFERENCE** 

  - We're using a double SPEC.md approach for Claude Code; each is an $ARGUMENT 
    - FOUNDATION: `./versioning-docs/v4_MAO/foundation_spec.md`
    - ADVANCED: `./versioning-docs/v4_MAO/advanced_spec.md`
  - Created a new executable commmand for the workflow: `./.claude/commands/dual_spec.md`
  - Full plan details: `./versioning-docs/v4_MAO/MAO_APP_UI_IMPLEMENTATION.md`

**ENHANCED IMPLEMENTATION DETAILS FOR CONTEXT JUMPING**

### NEW_USER_FLOW.md Integration Strategy
**Sean's Vision**: "I'm hoping that the vibe of the visuals and even the copywriting will speak through the NEW_USER_FLOW.md document"

#### Visual Design Elements from NEW_USER_FLOW.md
- **Cat Mascot Integration**: "~(=^‥^) Mao welcomes you!" branding throughout
- **Terminal UI Patterns**: Tree structures, progress indicators, conversation flows
- **Color Schemes**: Theme selection examples (Dark mode, Light mode, CVD variants)
- **Interactive Elements**: Arrow navigation, selection confirmations, preview displays
- **Typography Hierarchy**: Bullet patterns, indentation, contextual help text

#### Copywriting Style Elements
- **Conversational Tone**: "Mao, seanivore!", "We won't ask you again, mao"
- **Helpful Guidance**: Context-sensitive tips and explanations
- **Progressive Disclosure**: Information revealed as needed, not overwhelming
- **Personal Touch**: Username integration, welcoming language
- **Technical Clarity**: Complex concepts explained simply

### Integration Decision Points

#### Option A: Include NEW_USER_FLOW.md Directly
- **Pros**: Complete visual and UX context preserved
- **Cons**: Large file inclusion, potential redundancy
- **Use Case**: Reference document for UI developers

#### Option B: Extract and Integrate Elements
- **Pros**: Streamlined specs with essential elements
- **Cons**: Risk of losing visual context and nuance
- **Use Case**: Focused development specifications

#### Option C: Hybrid Approach (RECOMMENDED)
- **Implementation**: Core elements integrated, full document referenced
- **Structure**: Visual patterns in Foundation spec, complete flow in Advanced spec
- **Benefit**: Best of both approaches - focused and comprehensive

### Claude Code Spec Enhancement Strategy

#### Foundation Spec Enhancement
- **UI Patterns**: Extract core interface patterns from NEW_USER_FLOW.md
- **Visual Identity**: Integrate Mao cat branding and terminal aesthetics
- **Interaction Models**: Progressive onboarding, theme selection, settings management
- **Component Library**: Reusable UI elements identified in NEW_USER_FLOW.md

#### Advanced Spec Enhancement  
- **Complete Workflows**: Full user journey from NEW_USER_FLOW.md
- **Complex Interactions**: Multi-step processes, workflow creation, agent coordination
- **Advanced Features**: Real-time monitoring, progress tracking, system integration
- **Professional Polish**: Deployment-ready specifications with comprehensive detail

### Implementation Dependencies
- **All Systems Implemented**: Specs reflect actual working functionality
- **UI/UX Patterns Validated**: NEW_USER_FLOW.md patterns tested and refined
- **Visual Identity Finalized**: Consistent branding and design language
- **User Testing**: Interface patterns validated with real usage

### Implementation Plan
1. **Pattern Extraction**: Identify reusable UI/UX patterns from NEW_USER_FLOW.md
2. **Visual Integration**: Incorporate cat branding and terminal aesthetics
3. **Copywriting Style**: Extract and systematize writing patterns and tone
4. **Foundation Enhancement**: Update foundation spec with core patterns
5. **Advanced Enhancement**: Integrate complete workflows and advanced features
6. **Validation**: Ensure enhanced specs enable superior UI development
7. **Documentation**: Update MAO_APP_UI_IMPLEMENTATION.md with final approach

---

## CONTEXT JUMP SUCCESS CRITERIA

**For Future Claude Sessions**: This enhanced document provides comprehensive technical details for seamless implementation continuation across context windows.

### Implementation Readiness Checklist
- ✅ **Tool Standardization Complete**: 51 files standardized, professional quality
- ✅ **Real Data Integration**: No mock data, live metrics providers available
- ✅ **Architecture Established**: 4-file tool structure, modular JSON configs
- ✅ **Dependencies Mapped**: Clear task ordering with technical requirements
- ✅ **Templates Available**: JSON templates in ./configs/workflows/json_object_templates/
- ✅ **Reference Documents**: NEW_USER_FLOW.md comprehensive UI/UX guidance
- ✅ **Memory MCP Ready**: Context tracking with Mao_v4_Tool_Standardization_Phase entity

### Development Approach Standards
- **Systematic**: Work H2-by-H2 through numbered implementation tasks
- **Communicative**: Frequent Memory MCP updates and progress reporting
- **Quality-Focused**: Filesystem tools over artifacts for accuracy
- **Dependency-Aware**: Maintain task prerequisites and integration points
- **Context-Jump Ready**: Enhanced documentation for seamless session transitions

### Success Metrics
- **Task Completion**: Each H2 fully implemented with documentation
- **Integration Verification**: Systems work together seamlessly
- **Quality Assurance**: Professional-grade code and configuration
- **Context Continuity**: Future Claude sessions can immediately continue work
- **User Experience**: All interfaces functional and intuitive

**READY TO BEGIN WITH #1 APPLICATION CONFIGURATION SETTINGS CONFIG** 🚀 