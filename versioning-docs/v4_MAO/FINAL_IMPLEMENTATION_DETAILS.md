# Remaining Implementation Items Before Product UI Development 
v4 update started on 3 June 2025 --> Today is 29 June 2025

---

## Review For Context And Standards 

- UX/UI Guide `./versioning-docs/v4_MAO/NEW_USER_FLOW.md`
- "MAO File Standardization Rules" `./versioning-docs/technical-documentation/MAO_FILE_STANDARDIZATION_RULES.md` 

---

## After Implementation Requested **Tech Doc Blurbs**
I asked that AI then write up "a blurb of text that can be used to insert what is new into the technical documentation" and this is what was provided. No judgement, just a note. 

- "Task #2 Username > User ID Config Setup" `./versioning-docs/v4_MAO/TASK_2_USERNAME_CONFIG_COMPLETE.md` 
- "Task #3 Workflow Unique ID - COMPLETE WITH FULL INTEGRATION ✅" `./versioning-docs/v4_MAO/TASK_3_WORKFLOW_ID_COMPLETE.md` 
- "Files That Needed Workflow ID Integration" `./versioning-docs/v4_MAO/TASK_3_INTEGRATION_POINTS.md` 
- "Task #4 Workflow Creation - Implementation Complete" `./versioning-docs/v4_MAO/TASK_4_WORKFLOW_CREATION_COMPLETE.md` 

--

## During Implementation Requested **Context Jump Helper Docs**
- "User Configuration & Setup Script Implementation" `./versioning-docs/v4_MAO/NEEDS_UPDATE_CACHE_USER_CONFIG_SETUP.md` 

---

## Task #5 PHASE 1: **CLI Commands** Integration, Standardization, & Implementation

  1. There is only one type of CLI command
  2. Last session, the separation between the "setup scripts" living in the `./scripts/` directory and the 'commands and arguments' living in the `./configs/cli/` directory confused our planning for this task. 
  3. The benefit of this confusion is that we now realize that we have no reason to continue treating the 'setup scripts' as a separate type of CLI command. This happened because in the previous build of SFA, we didn't have any other CLI commands, and we were not building an in-app experience. 

### Regarding The Separation Between `./scripts/` and `./configs/cli/` Commands/Arguments

#### Learn About The 'SCRIPTS' Directory 

  1. We need to identify the touch points used in the codebase for the setup scripts. 
  2. Items that can be ignored in the `./scripts/` directory: 
     - The `./scripts/project_tree/` is a CLI command used manually by me; it was created and is living here simply because I wanted to update the old `tree` command I was using. *E.G. THIS IS NOT A CLI COMMAND THAT WILL BE USED IN THE APP AND DOES NOT NEED TO BE MOVED*
     - The `./scripts/quality_validator/` is a CLI command created specifically for testing the quality of the codebase. There is a `quality_validator_README.md` that should give further details. *E.G. THIS IS NOT A CLI COMMAND THAT WILL BE USED IN THE APP AND DOES NOT NEED TO BE MOVED*
     - The `./scripts/token_counter/` is a CLI command used manually by me; it was created and is living here simply because we moved it from the old directory to easy maintanence access. *E.G. THIS IS NOT A CLI COMMAND THAT WILL BE USED IN THE APP AND DOES NOT NEED TO BE MOVED* 
  3. Items that technically should be in the `./configs/cli/` directory **BUT**... 
     - The `./scripts/unique_id_generator/` is a CLI command that was created to help with the creation of the Workflow ID. The `./scripts/user_id_generator/` is a CLI command that was created to help with the creation of the User ID and use in the workflow. 
       - *Both should have been created in the `./configs/cli/` directory* 
       - They were created in the `./scripts/` directory because it was before we were thinking about the CLI commands and arguments. 
       - While we should move it, it is **IMPORTANT TO NOTE** that implementation of both of them is complete already in the workflow. 
       - If/when we move it, we need to do so in a wholistic way by finding all of its touch points and references and updating them, and then also making sure it works both in the system files, in the app, and as a CLI command generally. 
     - The `./scripts/workflow_setup/` are two CLI commands that are used heavily as entry points for the workflow. 
       - *They should have been created in the `./configs/cli/` directory* 
       - They were created in the `./scripts/` directory because it was before we were thinking about the CLI commands and arguments. 
       - **BUT** then when we created the CLI commands and arguments, we did create `--setup` and `/setup` as well as `--update` and `/update` and `--fix-it` and `/fix-it` as CLI commands and arguments. 
       - Consider that **THESE ARE ALL FUNCTIONAL** and implemented already. 

#### Sean's Current Opinion 

**FIRST:** I think we should first address the 'Integration, Standardization, & Implementation' document, along with all of the other commands that need to be created and properly implemented. 

  1. Make sure we have a clear standardized process that includes how to handle creating all the other CLI flag arguments and their slash commands. 
  2. Make sure we create an implementation plan for that process; then use it for each command, one at a time. 
  3. Make sure we have an AUDIT document that we can use to review the CLI commands and arguments after they are created; then do that separate from implementing them, but directly after each is created. 

**REASONING:** This will leave us with a clear-cut understanding of setting up CLI commands. We can then decide if we want to update the `./scripts/` directory or not. While in retrospect it seems like they should all be together, clearly they hold some kind of mental separation from the CLI commands and arguments. Let's give that, whatever it might be, time to consider it. 

#### Actual Task (Understanding All The Above)

  - Understanding the misunderstanding with which the first attempt at this task was made, we should now review that plan, and edit it to handle the standard CLI commands and arguments. 
  - Afterwards, we should also create a new plan for the 'SCRIPTS' directory. 

**DOCUMENT TO REVISE ACCORDINGLY, REVISIONS HAVE BEEN STARTED BUT MUST BE CONFIRMED:** 
`./versioning-docs/v4_MAO/CLI_COMMAND_STANDARDIZATION_PLAN.md`

---

## Task #5 PHASE 2: Confirm 'Orchestrator Integration' for CLI Related Features 

The first two notes are regarding the CLI commands and arguments for commands that are potentially a bit more complicated than the standard CLI commands and arguments. However, I write this before starting the standard CLI commands and arguments. It is completely possible that every single CLI command/argument will be its own unique thing. 

### **Workflow state management for `continue/review**`
  - 'Continue' as in, if a User or their workflow was inturrupted and they use the `--continue` flag or `/continue` slash command, then the workflow should resume from the last phase that was completed. 
  - Originally the "continue" feature was intended for workflow setup, and had a limitation that it could only be used if you were trying to continue a workflow that happens to also be the most recent operation. 
  - However, since we have User IDs and Workflow IDs, we can now continue any workflow that was interrupted, regardless of how long ago it was, and regardless if it was just during workflow setup or during a phase of the workflow. 
  - That is the reason that `--review` flag or `/review` slash command was added to this implementation note; because "review" is a command that allows the User to pull up any workflow, inturrupted or not, by the Workflow ID, by the workflow's custom command if it had been created yet, or by the User ID/Username and then scrolling through their workflows. 
  - It makes sense to lump these together because they both could push the usability of the other's features. 'Review' could be used as a way to continue a workflow, and continue could be a way to jump into a workflow and look over it. 
  - The `workflow_state.py` file is the file that will need to be updated to support this feature. 
  - It is important that the 'continue' feature still work in the minimalistic way that was originally intended as well; remember that when exiting the app, the User ID and state is saved unless the User logs out and unless the next user starts using the `--login` flag. Knowing this, it seems like perhaps there is a "continue" screen that shows the most recent workflow(s) at the top and shows if they were/weren't inturrupted. 
  - I'm feeling a little like, well, 'continue' has to be more robust, as described above, but that the quick and easy jump back into the inturrupted workflow is a bit missing; we should counter this feeling my making sure that when 'continue' is used, the the most recent inturrupted workflow is prominent at the top so that it is only one additional click to get back to that simple UX. 

### **Connect `goal()` method to real `WorkflowOrchestrator`**
  - The `goal()` method is refering to the `--goal` flag or `/goal` slash command, which User can use to have Mao instantly create a new workflow, from that first message with the goal, and nothing more. 
  - It's very much a "quick start" feature, and ideally, will work no matter the complexity of the goal's resulting workflow. That is to say that, just because the UX of using 'goal' is simple, it doesn't mean the workflow will be simple. 

## Task #5 PHASE 3: Confirm 'Orchestrator Integration' for 'Real-Time Features'

### Re: **Add real cost tracking and progress monitoring** 
  - In a recent audit I remember that we wanted to make sure that every file had the properly estimated cost naming in the codebase. I do not know how much further it went than that. 
  - However, we need to make sure that the real cost tracking is being calculated using a variable that allows for the proper LLM model to be implemented. 
  - Note that Sonnet 4 will be Mao reading the messages and replies whenver working with Mao; equally NOTE that this is a clear area of concern to watch out for. It might end up being hardcoded, which is should not be. Who knows, we might decide we want to use Opus instead in the future, OR we might decide we want to have the option of either as Mao's default, perhaps a setting that can be changed in the app. 
  - But for every other task that an agent is doing, we need to be able to make sure that the chosen LLM model is being used to calculate the cost by pulling it in from the JSON object that created the workflow, and then its other details from the actual model JSON object. 

### Re: **Confirm stats ready to connect to actual system metrics** 
  - We actually want to prepare this in a specific open-ended way for UI design 
    - Make it clear where the endpoints are for stats and metrics, describe what the stats and metrics are, provide ideas for what they could help display, as well as visual data visualization recommendations 
  - Implement live workflow monitoring 
    - Again, this should be prepared in a way that is easily provided to the UI build team, giving creative design freedom to them; we just need to ensure the functionality is prepared 
  - Re: notes about "Add progress bars and execution tracking" 
    - This is unnecessary because we're describing UI that is not yet decided on; we need only make sure that these kinds of functionality is possible and everything needed has been prepared and clearly provided to the UI build team 

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
