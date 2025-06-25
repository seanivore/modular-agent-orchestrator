# Final Implementation Items 

## Leftover From Integration Plan Notes 

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

## Technical Documentation 

### Notable Gaps 

1. On `2_MAO_SYSTEM_FILES.md` at LINE 159 "### ORCHESTRATION: Epic Memory `orchestrator/memory_mcp.py` Recall" needs details from implementation 

2. On `3_MAO_ARCHITECTURE.md` at LINE 270 "# interfaces/terminal/conversation_interface.py" is not a file that exists 

3. On `3_MAO_ARCHITECTURE.md` at LINE 509 "Setup script processes config and creates executable command" needs to be updated with the real setup script (see `NEW_USER_FLOW.md` to finalize this an JSON), 618 the JSON can be placed 

## Tasks, Re: `NEW_USER_FLOW.md` 

1. Error with `meid` command 
   - When you run just `meid` it shows the help message 
   - When you run `meid -h` it has an error response 
2. Alter the CLI-configs `"type": "needs_file"` to `"type": "needs_file_or_directory"` (or something shorter)
3. CLI-config JSONs 
   - Template is here: `./configs/examples/cli_command.json`
   - Create a new JSON for each command 
     - `--login` 
     - `--logout` 
     - `--model` 
     - `--provider` 
     - `--model-list` 
     - `--provider-list` 
     - `--list-tools` 
     - `--variables` 
     - `--variables-explain` 
   - Add to UI doc if needed; cache, error handling, etc.?
4. Created `./versioning-docs/v4_MAO/NEW_USER_FLOW.md` 
   - **Review entire document** 
     - Look for gaps, inaccuracies, areas for clarifications, opportunities for extrapolating, etc.  
   - **Review the new JSON objects and their new workflow** 
     - Re: temp files, directory in setup script, and multiple objects 
     - Throughout the document I added "*App UI/UX*" notation 
   - **See if we can add more**
     - Help build the visual expectations for the application 
     - Make it easier to construct the application we want 
5. As defined in the `NEW_USER_FLOW.md` document, saving User ID application configuration settings
   - **Identify** and then **implement** all details needed 
   - When a new User ID logs in, the application will prompt them to adjust their configuration settings 
   - The application will create a new `user_username.json` file in the `configs/user` directory, and save the adjusted settings to it 
   - The application will load these settings on subsequent launches 
   - The application will allow users to adjust these settings at any time using `/config` or launching with `mao --config` which updates their `user_username.json` file 
   - Default behavior is to launch with settings from the last session user; this and other defaults are items able to be adjusted on the application setting configuration screen 

## Updating our config collections to be a true 'plug-and-play' feature

1. Mao will be our updater 
   - We won't set this up yet, but we need to build in preparation for it 
   - At this stage, we'll just be handing over all the necessary details to Mao
   - Mao will create the appropriate JSON config file and place it in the proper directory 
   - This is the case for models, providers, tools, CLI-commands, etc. 
   - Same goes for having them deleted when we need
2. Current problem, if they're so easily updated, is instant, universal updating 
   - We need to make sure that in-app displays are updated as well 
   - We need a way to make sure that every place a config collection is displayed in documentation is up-to-date 
3. This needs to be automated; a user could run the command to see all the tools at any time 
   - In app it could technically pull what is in the file live 
   - For written documents, we'll need to have a way to update them 
4. Claude Code TIP from today was `※ Tip: Run /install-github-app to tag @claude right from your Github issues and PRs`
   - I think this will work but I need confirmation 
   - Then we need to detail the steps for how to use it, e.g. the command to post a PR, what it should say, how specific, etc. 
   - For updating these plug-and-play config collections, we should have a template for a PR post that can be executed with a custom command 
   - Unless there is a way to trigger the PR post just from it noticing that a specific directory was changed 
   - Good introduction to this tool
