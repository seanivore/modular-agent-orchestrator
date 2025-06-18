# **Walk Through of UX Flow**

  1. Review the walkthrough below for accuracy 
  2. Add in any missing details or steps 
  3. Any notes it reminds you of, add them to the task list in the next session task section or other appropriate place 

## Setting Up A New Project's Workflow 

1. User runs command `mao mao` and the Mao application is launched 
2. Firsts time user gets asked to chose a text color and highlight color (just like in Claude Code)
3. Next screen is the main page which is where the chat and everything is
4. Simple directions sit below the text input field, 'Describe your project or ask Claude to guide you' 
5. Below the title are icons that indicate the necessary variables 
   - They change color when the information is provided
   - They are not detailed at all, meant as a visual progress bar to new users and regular users know what they mean 
6. The User and Claude's conversation 
   - Other than knowing the variables, Claude is not provided any kind of script 
   - The only guidance is that they should try to read what the user's experience level is; anticipate their needs 
   - This will allow for a natural UX flow where users in a rush can be and those who need help can get it 
   - Users could only provide their goal, or a fully prepared JSON config 
7. Claude then 'steps away' for a moment 
   - They detail in the `Workflow Log` what the project is about 
   - If the user gave the workflow, then they record that and use the setup script to create the work flow 
   - Otherwise Claude will plan a workflow based on the user's goal
8. Claude pauses to think and consider potential workflow solutions
   - Claude is knowledgeable of types of agentic workflows 
   - In most cases with creative tasks, Claude will plan a workflow without an end phase 
   - Claude plans multiple potential draft workflows 
9. Claude again pauses to think and considers the options to choose the best one 
10. Claude returns to present the workflow to the User for confirmation 
   - Estimate price, cost, time, etc. is included in what is sent to the user to review 
   - The User has the chance to ask questions, make changes, etc. 
   - Claude works with the User until they are satisfied 
11. Claude then 'steps away' to record things and set the workflow up 
   - Claude updates the `Workflow Log` with the final workflow plan 
   - Claude creates the `memory.py` file for the workflow 
   - Claude runs the setup script to create the workflow 
12. Options and behavior for the setup script
    - If outside the app in the terminal they can run the command `mao --setup` 
    - If inside the app they can either run `!mao --setup` or `/setup` 
    - The setup script will create the custom command for the workflow 
    - Custom commands always have spaces not hyphens, and start with the main command name, then args 
    - The setup script will create a USE_CASE_README.md in the use-case's directory 
    - This README will include the custom command, the workflow plan, and the estimated cost, time, etc. 
    - The setup script will include a unique ID of scrambled characters for the workflow 
    - The actual script is also saved in the use-case's directory
13. Claude renames the `memory.py` file to append `_` and then the unique ID of the workflow 
    - Claude updates the `Workflow Log` 
    - Claude details what will be needed for each agent in the workflow so they are prepared when it is activated 
14. Claude returns to the User and presents their command and the path where they can find the workflow directory 
15. Claude adds last entry to the `Workflow Log` and the `memory.py` file 
    - They must the save the documents to the Files API using the code execution tool so it is able to be downloaded later 
    - Claude then signs off 

## Activating A Project's Workflow 

1. User has a few options to activate the workflow --> In all cases they will end up in the application 
   - They can simply run the custom command as it is in the terminal 
   - User can run `mao mao` to start the application 
   - In the application they can run the custom command but `!` must be before it to run a command 'outside' the application 
   - User could also run the command `/workflows` to see all workflows and their status, find their flow, and select it to activate 
   - The could have also started the application using `mao --workflows` and jumped to the workflow selection screen 
   - Finally, user could simple message Claude in the chat and ask them to activate the workflow  
2.  Workflow is activated and Claude is called to orchestrate 
   - Part of the workflow activation script includes the unique ID of the workflow for Claude 
   - They pull the `memory.py` and the `Workflow Log` from the Files API using the unique ID  
   - The `memory.py` file give them back the context of the workflow starting from setup 
   - The `Workflow Log` gives them the plan of the workflow 
   - Claude updates them both noting that they are activating the workflow 
3.  Claude prepares materials for the agents in the workflow 
   - Claude creates a button snippet for each agent in the first phase of the workflow 
   - They create one snippet for the tools and another for calling Claude when they're done 
   - The snippet includes the workflow's unique ID, as Claude will need it later 
4. Claude hands off the materials to the agents that start the workflow 
   - This includes a clearly defined deliverable for each agent; description of their task, motivation, etc. 
   - A note includes the token context length max, created either for the use case or by the user 
   - The note also reminds them that their doc tool has auto-save and to call Claude when they're done or need help 
5. Claude adds last entry to the `Workflow Log` and the `memory.py` file 
   - Claude saves all working drafts in the Files API 
   - Claude then signs off 

## Agent Task Phase 

1. Agent(s) go(es) off and works to complete their task 
   - They have a live token counter just like we have in the IDE when I'm typing up a document 
   - They have a button snippet for each tool they're using 
   - If they need help, they can call Claude directly
   - There can be parallel agents work on various or the same tasks 
2. This entire time, there is a live tracking UI for the User 
   - They can watch everything that is happening 
   - There is also a bell tone when the agent is done so that the User can do other things if they want 
3. Agent completes their task 
   - They call Orchestrator Claude using the button snippet
   - Button snippet includes the workflow's unique ID for Claude 
4. Claude arrives
   - They use the unique ID to pull the `memory.py` file 
   - They also pull the `Workflow Log` from the Files API 
   - They review the `memory.py` file to see what has been done so far 
   - They immediately update them that they are about to register the completion of an agent or agents task(s)
5. The agent and Claude meet and talk directly 
   - This ensures Claude gets exactly the amount of clarity they need 
   - Or it ensures that Claude doesn't get an overwhelm of unnecessary information 
6. Agent passes the deliverables, within token limit, directly to Claude 
7. Agent provides Claude a task report 
   - Depending on the workflow this might also include information needed for the next task 
   - No matter what it is, Claude records it in their `Workflow Log` and updates the `memory.py` file 

## The Claude Orchestrator Interlude 

1. Claude always reviews the deliverables to ensure they are complete 
2. Claude reports on the status of the deliverables in the `Workflow Log` and `memory.py` file 

### A. **Claude Plans The Next Task According To The Deliverables**

3. Claude plans the next task 
   - This is common for most workflows to ensure the best possible results and encourage creativity 
   - It is especially helpful for creative tasks or if there was a planned, open-ended decision to be made 
   - The `Workflow Log` is updated with the plan 
   - The `memory.py` file is updated with the plan 
4. Claude Prepares An Addendum Config JSON Workflow File 
   - This would include the workflows unique ID 
   - It would be stored in the use-case's directory 
   - The file names are the same but numbered to keep them sorted in the directory 
5. If there is a human in the loop checkpoint, Claude would ask that they review much like the setup phase 
6. Claude runs the command `mao --update` with the new JSON config file 
   - As in, they need to "update" the workflow 
   - NOTE: There might be more than one unplanned task, so update might be used more than once 
   - This script creates an addendum `WORKFLOW_PT_2_README.md` in the use-case's directory 
   - They update the `Workflow Log` with the plan and update the `memory.py` file 
7. Claude saves all working drafts in the Files API 
8.  Claude prepares materials for the agents in the workflow 
   - Claude creates a button snippet for each agent in the first phase of the workflow 
   - They create one snippet for the tools and another for calling Claude when they're done 
   - The snippet includes the workflow's unique ID, as Claude will need it later 
9. Claude hands off the materials to the agents that start the workflow 
   - This includes a clearly defined deliverable for each agent; description of their task, motivation, etc. 
   - A note includes the token context length max, created either for the use case or by the user 
   - The note also reminds them that their doc tool has auto-save and to call Claude when they're done or need help 
10. Claude adds last entry to the `Workflow Log` and the `memory.py` file 
   - Claude saves all working drafts in the Files API 
   - Claude then signs off 

### B. **Claude Changes The Next Task Because The Deliverable Needs More Work**

3. Claude plans how to fix the file
   - The `Workflow Log` is updated with the plan 
   - The `memory.py` file is updated with the plan 
4. Claude Prepares An Do-Over Config JSON Workflow File 
   - This would include the workflows unique ID 
   - It would be stored in the use-case's directory 
   - The file names are the same but numbered to keep them sorted in the directory 
5. If there is a human in the loop checkpoint, Claude would ask that they review much like the setup phase 
6. Claude runs the command `mao --fix-it` with the new JSON config file 
   - As in, they need to "fix" a deliverable and therefore are going to do the same phase again 
   - They update the `Workflow Log` with the plan and update the `memory.py` file 
7. Claude saves all working drafts in the Files API 
8.  Claude prepares materials for the agents in the workflow 
   - Claude creates a button snippet for each agent in the first phase of the workflow 
   - They create one snippet for the tools and another for calling Claude when they're done 
   - The snippet includes the workflow's unique ID, as Claude will need it later 
9. Claude hands off the materials to the agents that start the workflow 
   - This includes a clearly defined deliverable for each agent; description of their task, motivation, etc. 
   - A note includes the token context length max, created either for the use case or by the user 
   - The note also reminds them that their doc tool has auto-save and to call Claude when they're done or need help 
10.  Claude adds last entry to the `Workflow Log` and the `memory.py` file 
   - Claude saves all working drafts in the Files API 
   - Claude then signs off 

### C. **Claude Calls The Next Agent As Already Planned In The Workflow**

3. Claude saves all working drafts in the Files API 
4.  Claude prepares materials for the agents in the workflow 
   - Claude creates a button snippet for each agent in the first phase of the workflow 
   - They create one snippet for the tools and another for calling Claude when they're done 
   - The snippet includes the workflow's unique ID, as Claude will need it later 
5. Claude hands off the materials to the agents that start the workflow 
   - This includes a clearly defined deliverable for each agent; description of their task, motivation, etc. 
   - A note includes the token context length max, created either for the use case or by the user 
   - The note also reminds them that their doc tool has auto-save and to call Claude when they're done or need help 
6.  Claude adds last entry to the `Workflow Log` and the `memory.py` file 
   - Claude saves all working drafts in the Files API 
   - Claude then signs off 

### D. **Claude Concludes The Workflow If This Was The Last Task**

3. Claude removes all draft files from the Files API 
   - They are usually not needed and can be deleted 
   - Any important information can be passed along with the final deliverables 
4. Claude saves the final deliverables to the output directory from the JSON config
   - They enter a final entry to the `Workflow Log` and the `memory.py` file 
   - An addendum of `_1` and counting up for each time the workflow is run needs to be added to the `Workflow Log` 
   - I'm not sure we need to do that for the `memory.py` file 
   - If we don't for the `memory.py` file we need to include that Claude has to wipe the file before each time the workflow is run again 
   - The `Workflow Log` and `memory.py` file are saved to final output directory for the project use case as well 
5.  Claude then signs off 