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

SEE IMPLEMENTATION PLAN: `./versioning-docs/v4_MAO/CLI_IMPLEMENTATION_PLAN_NOTES.md`

### Understanding the Scope of This Task 

  1. GOAL: Clear up our convoluted language usage (we've been callin everything, just, "a command")
  2. INTENTION: Make clear the unintended separation of the `./scripts/` and `./configs/cli/` directories 
  3. INTENTION: Show the different use-cases and functionality of commands and arguments so that we can create a proper update to the `CLI_COMMAND_STANDARDIZATION_PLAN.md` document (revisions have been started but only a partial simplification)
  4. INTENTION: Then use that plan to create each command, one at a time 
  5. INTENTION: Make sure we have an AUDIT document that we can use to review the CLI commands and arguments after they are created; then do that separate from implementing them, but directly after each is created -- notably, I'm not sure that every command will have the same touch points, or maybe there are a few touch points that are in all cases, but then, depeneding on the command function, each might have other files to should be audited as well after implementation. 

### Understanding the Types of Commands, Flag Arguments, and Slash Commands 

--> **FUNCTIONAL: GROUP A** -- Commands that don't use `mao` as a prefix, and do not have a slash command. Are currently not used in the app. 
    - `./scripts/project_tree/` 
    - `./scripts/token_counter/` 

    These are in the project directory because I happened to ask for them to be created while working on this project. Perhaps we should move them to a completely new directory that isn't tied to any project; ~/Development/custom-cli-tools/ if that makes the most sense. Up to now, they have helped being in here because I was able to use them as an example of what was working created previously (specifically regarding the way in which custom commands are created particuarly). 

    The `ptree` command is a .sh shell script and then another .sh shell script to install it as a custom command. 

    The `token_counter` command is a .py python script, and then a .sh shell script to install it as a custom command. 

--> **FUNCTIONAL: GROUP B** -- Commands that don't use `mao` as a prefix, but have a slash command, are currently used in the app, and are in the `./scripts/` directory. However, the commands have JSON files that are stored in the `./configs/cli/` directory. 
    - `./scripts/unique_id_generator/` 
    - `./configs/cli/workflow_id/`
    - `./scripts/user_id_generator/` 
    - `./configs/cli/user_id/`

    The first two were created on the fly, before we finished building out the CLI commands and arguments, to solve a problem while developing the projects workflow. They've been implemented into system files. 

    The third one is a custom command that is how we've been activating use-case workflows since the beginning with the SFA. It resides here for that reason. In the SFA, there was no application it just ran in the terminal, and we didn't have any CLI commands and arguments. 

    While they are all actual CLI commands, not techincally flag arguments, they all also have an in-app slash command planned. 

    The `unique_id_generator` and the `user_id_generator` are both .py python scripts that have a .sh shell script to install them as custom commands. 

--> **FUNCTIONAL: GROUP C** -- Command that does not use `mao` as a prefix, can be run as a slash command in the app, but is stored with the use-case's files in `./configs/workflows/USE-CASE/` created for that specific use-case. 

    These are created using the .sh shell script for the workflow which is the next command directly below this one. 

--> **FUNCTIONAL: GROUP D** -- Commands that do use `mao` as a prefix, have a slash command, but are currently in the `./scripts/` directory. However the three commands have JSON files that are stored in the `./configs/cli/` directory. 
    - `./scripts/workflow_setup/`
    - `./configs/cli/setup/`
    - `./configs/cli/update/`
    - `./configs/cli/fix_it/`

    This is techincally two scripts. The one is primary, and is what you run with the JSON file to create a workflow; running it creates the 'custom command' mentioned above. The other is secondary and is primarily used to give the primary script a way to run in the terminal using a custom command. 

    The `workflow_setup` script is a .sh shell script that uses the JSON file to create the workflow's .sh shell script which is stored with the JSON file and other files for that use case in a `./configs/workflows/USE-CASE/` directory. In addition, it sets up that actual directory and writes a README.md file about the use-case's workflow. It also runs the `install-workflow-commands.sh` script to install the custom command for the use-case. 

    The `install-workflow-commands.sh` script is a .sh shell script that installs the custom command for the use-case. It is run by the `workflow_setup` script. 

--> **TO SET UP: GROUP E** --Commands that do use `mao` as a prefix, have a slash command, and are currently in the `./configs/cli/` directory. We will need to chat about each, one at a time as we go, to understand the full functionality of each. 
    - `./configs/cli/chat/`
    - `./configs/cli/config/`
    - `./configs/cli/continue/`
    - `./configs/cli/doctor/`
    - `./configs/cli/dry_run/`
    - `./configs/cli/free_only/`
    - `./configs/cli/goal/`
    - `./configs/cli/help/`
    - `./configs/cli/list_tools/`
    - `./configs/cli/login/`
    - `./configs/cli/logout/`
    - `./configs/cli/logs/`
    - `./configs/cli/model/`
    - `./configs/cli/model_list/`
    - `./configs/cli/output_directory/`
    - `./configs/cli/privacy/`
    - `./configs/cli/provider/`
    - `./configs/cli/provider_list/`
    - `./configs/cli/review/`
    - `./configs/cli/stats/`
    - `./configs/cli/variables/`
    - `./configs/cli/variables_explain/`
    - `./configs/cli/verbose/`
    - `./configs/cli/workflows/`

--> **TO SET UP: GROUP F** -- Commands that are in-app slash commands only, are currently in the `./configs/cli/` directory. 
    - `./configs/cli/exit/`
    - `./configs/cli/restart/`

#### Table of Commands, Flag Arguments, and Slash Commands for Clarity 

| **FUNCTION**           | **TERMINAL COMMAND**           | **IN-APP COMMAND**            |
| ---------------------- | ------------------------------ | ----------------------------- |
| **Start Application**  | `mao mao`                      | -                             |
| **Run Your Workflow**  | `custom command`               | `/custom command`             |
| Create Workflow ID     | `uid`                          | `/uid` or `! uid`             |
| Create User ID         | `meid username`                | `/meid username`              |
| Restart application    | -                              | `/restart` or `! mao restart` |
| Exit application       | -                              | `/exit` or `! mao exit`       |
| *Setup from JSON*      | `mao --setup ./config.json`    | `/setup ./config.json`        |
| *Update Workflow*      | `mao --update ./phase.json`    | `/update ./phase.json`        |
| *Fix Deliverable*      | `mao --fix-it ./fix.json`      | `/fix-it ./fix.json`          |
| Login User ID          | `mao --login`                  | `/login`                      |
| Logout User ID         | `mao --logout`                 | `/logout`                     |
| Open app config        | `mao --config`                 | `/config`                     |
| Resume last workflow   | `mao --continue`               | `/continue`                   |
| First message to AI    | `mao --chat message`           | `/chat message`               |
| Create entire workflow | `mao --goal project goal`      | `/goal project goal`          |
| System Statistics      | `mao --stats`                  | `/stats`                      |
| List Workflows         | `mao --workflows`              | `/workflows`                  |
| Review Workflow        | `mao --review custom command`  | `/review custom command`      |
| Set output directory   | `mao --output ~/downloads`     | `/output ~/downloads`         |
| Verbose Debug Mode     | `mao --verbose`                | `/verbose`                    |
| View workflow logs     | `mao --logs`                   | `/logs`                       |
| Show workflow stats    | `mao --stats`                  | `/stats`                      |
| Check Health           | `mao --doctor`                 | `/doctor`                     |
| View help messages     | `mao --help`                   | `/help`                       |
| Simulate Workflow      | `mao --dry-run`                | `/dry-run`                    |
| Set favorite model     | `mao --model model-name`       | `/model model-name`           |
| Set default provider   | `mao --provider provider-name` | `/provider provider-name`     |
| List models            | `mao --model-list`             | `/model-list`                 |
| List providers         | `mao --provider-list`          | `/provider-list`              |
| List tools             | `mao --list-tools`             | `/list-tools`                 |
| List variables         | `mao --variables`              | `/variables`                  |
| Explain variables      | `mao --variables-explain`      | `/variables-explain`          |
| Terminal Commands      | -                              | `! ls -la` (any bash/zsh)     |

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

---

## CREATING A PRIVACY SETTING FOR THE USER  
| Privacy models only    | `mao --privacy`                | `/privacy`                    |
The "Providers" such as Requesty and LiteLM that have multiple providers to choose from within themselves need to be broken down into separate JSON files for each sub-provider. 

configs/providers/requesty.json
etc. 