# Remaining Implementation Items Before Product UI Development 

---

## Task #4: Workflow Creation 

1. The workflow creation is the best way to illustrate building a workflow 
2. Show the Use-Case JSON being built 

**For truely comprehensive workflow, see the `NEW_USER_FLOW.md` document section on User IDs**

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
8. Create any necessary additional files, scripts, or automations 
9. Audit the new files using the `MAO_FILE_STANDARDIZATION_RULES.md` document 
10. Implement the plan 
11. Document all of the above, including the JSON objects use and the setup script; okay to do it in a small file to be added to the docs later 

---

## Task #5: Leftover From Integration Plan Notes 

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

--> Audit files using the `MAO_FILE_STANDARDIZATION_RULES.md` document 

---

## Task #6: Updating Any / All Config Collections 

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
3. create any necessary files 
4. Audit the new files using the `MAO_FILE_STANDARDIZATION_RULES.md` document 
5. Document all of the above; okay to do it in a small file to be added to the docs later 

---

## Task #7: Technical Documentation 

### Notable Gaps 

1. On `2_MAO_SYSTEM_FILES.md` at LINE 159 "### ORCHESTRATION: Epic Memory `orchestrator/memory_mcp.py` Recall" needs details from implementation 

2. On `3_MAO_ARCHITECTURE.md` at LINE 270 "# interfaces/terminal/conversation_interface.py" is not a file that exists 

3. On `3_MAO_ARCHITECTURE.md` at LINE 509 "Setup script processes config and creates executable command" needs to be updated with the real setup script (see `NEW_USER_FLOW.md` to finalize this an JSON), 618 the JSON can be placed 

### Full Documentation Audit 

After all items are implemented, I'd like to do a full documentation audit. All documents should be reviewed carefully, first one at a time, then all together. There are currently many overlaps and, reading them straight through is a bit of a challenge. This should be our end goal: that they can be read straight through without confusion. 

---

## Task #8: Revamp the Claude Code Dual SPEC.md Files 

Update and enhance them with all that we have completed. 

  1. Detailed, thorough, visual UX/UI in `NEW_USER_FLOW.md` document 
  2. `NEW_USER_FLOW.md` evokes vibe of visuals and even copywriting should speak through the document
  3. Very carefully detailed typography visuals in `6_MAO_VISUAL_IDENTITY.md` document 

### Previous SPEC.md File Implementation 

This was a double SPEC.md approach for Claude Code, using one at a time, sequentially, and provided as $ARGUMENTS. 

   - FOUNDATION: `./versioning-docs/v4_MAO/foundation_spec.md`  <-- Update based on new details 
   - ADVANCED: `./versioning-docs/v4_MAO/advanced_spec.md`  <-- Update based on new details 

We can entertain the idea of using a third SPEC.md file since we have a lot of polish now. 

We created a new executable command workflow. 

   - `./versioning-docs/v4_MAO/dual_spec.md`

Detailed our implementation plan for running the SPEC.md files. 

   - `./versioning-docs/v4_MAO/MAO_APP_UI_IMPLEMENTATION.md`  <-- Needs update based on details below 

### Implementation Plan 

1. Create implementation plan for the use, creation, and updating of the Claude Code SPEC.md files 
2. Implement the plan 
3. Document all of the above; okay to do it in a small file to be added to the docs later 

### Claude Code SPEC.md Enhancement 

1. Pull from the `NEW_USER_FLOW.md` document 
   - Extract core interface UI patterns 
   - Interaction models progressive onboarding, theme selection, settings management
   - Idenitfy reusable UI elements for component library
   - Stay true to the simple, clean visual brand identity; Mao cat branding, terminal aesthetics 
2. Review full user journey from NEW_USER_FLOW.md
   - See complex interactions, multi-step processes, workflow creation, agent coordination
   - System integration of real-time monitoring and progress tracking, user stats over time
   - Ensure deployment ready professional polish and comprehensive detail 
3. Implementation dependencies 
   - All systems are implemented; SPEC.md reflect working functionality 
   - Stay true to validated UI/UX tested and refined NEW_USER_FLOW.md patterns 
   - Stay true to finalized visual identity design language 
   - Validate interface patterns with real usage 

### Copywritign Style Guide Tips 

   - Tip and explaination UI is context-sensitive and has abundant examples 
   - 'Conversational' but technically simplier than conversational 
   - Claude Code was our inspiration for the UI/UX; let it be yours 
   - Progressive disclosure information is revealed as needed and only for as long as needed 
   - Information removal as well, it goes both ways, maintaining avoidance of overwhelm
   - Name, username integration; use in conversation for personalization 
   - No complex concepts at all, only clarity, especially if remotely techincal 

### Visual Brand Identity Guide Tips 

   - Mao cat is only shown on initial headers in corner and no where else 
   - See `6_MAO_VISUAL_IDENTITY.md` for more full details on UI patterns 
   - Handful of methods of showing informational hierachy 
   - Tree structures, very select colors, generous indentation with unique bullets 
   - Conversational flow has decent line spacing because the messages are so concise 
   - Interactive elements include arrow naviation when eneded, selection confirmation, preview displays, modals 
   - Typographical hierachy *IS* the visual design 
   - Incredibly carefully planned bullet patterns, indentation, contextual help text 

### Implementation Plan 

   - Identify reusable UI/UX patterns from NEW_USER_FLOW.md
   - Incorporate terminal aesthetics with minimal cat branding 
   - Recreate copy style by extracting and systematizing writing patterns and tone 
   - Update foundation SPEC.md with core patterns 
   - Update advanced SPEC.md with complete workflows and features 
   - Validate that enhanced SPEC.md files enable superior UI development 
   - Document final approach by updating MAO_APP_UI_IMPLEMENTATION.md 

### Handoff 

   - Include the `NEW_USER_FLOW.md` document in the handoff 
   - Simplify the `NEW_USER_FLOW.md` document to be more concise and focused on the UI/UX aspects 
   - Elaborate on design language and visual identity 
   - Include `6_MAO_VISUAL_IDENTITY.md` document; simplified 

### Deliverables 

   - Detailed overview of how to make simple edits and enhancements to UI foundation 
   - Explain what needs integration and include the code snippets 

---

NOTE: ✅ Dependency Issue = Just missing Anthropic Package
Not a code problem, just need pip install Anthropic for full orchestrator (not critical for our workflow ID functionality)

UPDATE: I tried and it says it is already installed. Does "...for full orchestrator" mean something other than just in the terminal? Like it needs the Anthropic imports? Do all files? Which? 

```bash
> ~/Dev/modular-agent-orchestrator > pip install anthropic             07:07:45
Requirement already satisfied: anthropic in /Users/seanivore/.pyenv/versions/3.13.3/lib/python3.13/site-packages (0.49.0)
Requirement already satisfied: anyio<5,>=3.5.0 in /Users/seanivore/.pyenv/versions/3.13.3/lib/python3.13/site-packages (from anthropic) (4.9.0)
Requirement already satisfied: distro<2,>=1.7.0 in /Users/seanivore/.pyenv/versions/3.13.3/lib/python3.13/site-packages (from anthropic) (1.9.0)
Requirement already satisfied: httpx<1,>=0.23.0 in /Users/seanivore/.pyenv/versions/3.13.3/lib/python3.13/site-packages (from anthropic) (0.28.1)
Requirement already satisfied: jiter<1,>=0.4.0 in /Users/seanivore/.pyenv/versions/3.13.3/lib/python3.13/site-packages (from anthropic) (0.9.0)
Requirement already satisfied: pydantic<3,>=1.9.0 in /Users/seanivore/.pyenv/versions/3.13.3/lib/python3.13/site-packages (from anthropic) (2.11.3)
Requirement already satisfied: sniffio in /Users/seanivore/.pyenv/versions/3.13.3/lib/python3.13/site-packages (from anthropic) (1.3.1)
Requirement already satisfied: typing-extensions<5,>=4.10 in /Users/seanivore/.pyenv/versions/3.13.3/lib/python3.13/site-packages (from anthropic) (4.13.2)
Requirement already satisfied: idna>=2.8 in /Users/seanivore/.pyenv/versions/3.13.3/lib/python3.13/site-packages (from anyio<5,>=3.5.0->anthropic) (3.10)
Requirement already satisfied: certifi in /Users/seanivore/.pyenv/versions/3.13.3/lib/python3.13/site-packages (from httpx<1,>=0.23.0->anthropic) (2025.1.31)
Requirement already satisfied: httpcore==1.* in /Users/seanivore/.pyenv/versions/3.13.3/lib/python3.13/site-packages (from httpx<1,>=0.23.0->anthropic) (1.0.7)
Requirement already satisfied: h11<0.15,>=0.13 in /Users/seanivore/.pyenv/versions/3.13.3/lib/python3.13/site-packages (from httpcore==1.*->httpx<1,>=0.23.0->anthropic) (0.14.0)
Requirement already satisfied: annotated-types>=0.6.0 in /Users/seanivore/.pyenv/versions/3.13.3/lib/python3.13/site-packages (from pydantic<3,>=1.9.0->anthropic) (0.7.0)
Requirement already satisfied: pydantic-core==2.33.1 in /Users/seanivore/.pyenv/versions/3.13.3/lib/python3.13/site-packages (from pydantic<3,>=1.9.0->anthropic) (2.33.1)
Requirement already satisfied: typing-inspection>=0.4.0 in /Users/seanivore/.pyenv/versions/3.13.3/lib/python3.13/site-packages (from pydantic<3,>=1.9.0->anthropic) (0.4.0)
```
