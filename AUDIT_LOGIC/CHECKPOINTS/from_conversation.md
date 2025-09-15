# Conversation Figuring Out How to Avoid Using Memory MCP 

## Overview 

Anthropic MCP Connector tool requires a non-local "HTTP/SSE" type of MCP transporter. Memory MCP runs on your local machine only; and Users can't access localhost:8080 from their browsers. There wouldn't be a shared memory state between different user sessions. 

We have an implementation plan for a later update to create our own actual Memory tool, but for launch we are going to implement a more manual system that sort of uses the "Memory Fallback". We will not need to use the Files API fallback, because if Mao is present and available in the app, then the Files API is most likely accessible (and the Files API is free). 

### Goal 

We'll instead be implementing a config-driven memory system. The following are the directions that AI last left me with, however while preparing for it I have some slight questions.

---

## Updated Group 3 Final Plan 

### Phase 1+2 WITH CONFIG-DRIVEN MEMORY 

  1. Checkpoint for impromptu or official update JSON 
     - Define for each official checkpoint what exactly Mao should report on 
     - This is started `./AUDIT_LOGIC/CHECKPOINTS/PROJECT_STATE_CHECKPOINTS.md`
  2. Delete `mcp_hub.py` and `memory_mcp.py` entirely
  3. Create config-driven memory point system in `configs/checkpoints/`
  4. Build `Checkpoint` class in `workflow_manager.py` that loads configs dynamically
  5. Gut hardcoded relevance from `manager_tools.py` 

* **Phase 3 BECOMES: Create the 9 memory point JSON configs from MAO_FLOW docs**

### ~~MaoMemory~~ *Checkpoint* Implementation Pattern

* **In `workflow_manager.py`** (I think)

```python 
class MaoMemory:
    def __init__(self):
        self.memory_points = self._load_memory_point_configs()
        
    def trigger_save_point(self, point_id: str, context: Dict):
        """Execute configured memory save point"""
        config = self.memory_points.get(point_id)
        if not config:
            return
            
        # Ask Mao the configured questions with context
        # Save to JSON + Files API backup as configured
``` 

* **In `core.py`** 

```python 
# OFFICIAL MAO MEMORY SAVE POINT 1
self.mao_memory.trigger_save_point("01_workflow_creation", {
    "user_id": user_id,
    "workflow_id": workflow_id,
    "chat_history": chat_history
})
``` 

---

## Accurate Plan Updates Requires 

  1. I'm confused about needing `./configs/checkpoints/...` because all of the files for memory and any project asset data and documents will all be saved in the Files API 

  2. I think we need the details for each official save point in the code, presumably `core.py`, which would be far more robust and normal language like. I've started pulling this gether with other details here: `./AUDIT_LOGIC/CHECKPOINTS/PROJECT_STATE_CHECKPOINTS.md` 

  3. Mao needs to use the Code Execution tool to save to the Files API, and we need to make sure we have that on lock-down because we've never used it before and idk if you can even create directories and subdirectories; though if not, the proposed file naming conventions would keep things in order anyway. 

  ```
  How do we have this set up now? Because it looks like the uploaded file needs to be at a path, which would potentially defeat our intention of using the Files API as a ways to save on tokens, no? Maybe you could review this and see if there is a way to do this like, would we want to put it in a temp. file? I'm also just a bit confused trying to wrap my head around this when thinking about the app being used by a User as a web app ... though I guess anything they'd want to use *would* be on their local computer. But there is a project state JSON that we'll be using for the memory context and I'm curious how that works. I'm guessing we can save it as .temp somehow first? 

  This one isn't that in depth: 

  `https://docs.anthropic.com/en/docs/build-with-claude/files`

  But then the actual Messages API information is in depth, though when I tried to copy it, it said Markdown but came out as YAML. But I'm assuming what is on this page is more helpful. If you want I can gather the python message for each (unless we want cURL, I'm guessing no, but the whole "Code Execution too" thing confuses me a bit). 

  CREATE FILE: `https://docs.anthropic.com/en/api/files-create` 
  LIST FILES: `https://docs.anthropic.com/en/api/files-list` 
  GET FILE METADATA: `https://docs.anthropic.com/en/api/files-metadata` 
  DOWNLOAD A FILE: `https://docs.anthropic.com/en/api/files-content` 
  DELETE A FILE: `https://docs.anthropic.com/en/api/files-delete` 
```
```
4. When we implement this system, we need to set it up so that Mao can create a Project State Update at anytime. I've been calling them Impromptu Checkpoints and Official Checkpoints. All of this probably needs to be explained in the code as well, though the details are all in the `PROJECT_STATE_CHECKPOINTS.md` mentioned before. 

5. I did create a JSON config for the Project State update. It combines adding and files and documents data with the actual written memory entry the same way we would "write" an entry into the Memory MCP. I'm wondering if we want to add a `chat_history` field, and need you to review it in general to see what else could be added or changed. Like it would be great to have chat history, but also that's a lot. HOWEVER, I'm also just now realizing that if someone was to stop working on a project and come back to it, we would need the display to look just like it was. But maybe that is already in the `workflow_manager.py` -- we had a specific "state" workflow manager but it was consolidated into just that one file. Here is the JSON, which was also mentioned in the `PROJECT_STATE_CHECKPOINTS.py` -- `./AUDIT_LOGIC/CHECKPOINTS/project_state_checkpoint.json` 

6. I'm just now seeing that the AI had provided a drafted proposed JSON. Not quite everything, but also some things I didn't have. But I don't think we want to put the questions and this other information ON a prefab config for every checkpoint. It seems more like we should put the specifics in the code for when Mao comes to a checkpoint, and then use the exact same, single, JSON config for everything like I created already. 

```JSON 
{
  "point_id": "01_workflow_creation",
  "trigger_location": "core.py:_create_workflow_from_chat()",
  "save_questions": [
    "What is the user's primary goal for this workflow?",
    "What energy level and mood is the user displaying?",
    "Any specific constraints or preferences mentioned?",
    "Initial complexity assessment of the request?"
  ],
  "context_requirements": [
    "full_chat_history",
    "user_id", 
    "workflow_id"
  ],
  "backup_to_files_api": true,
  "memory_entity_type": "workflow-creation"
}
``` 

7. Once this is all sorted, planning and preparation-wise, the **actual** task at hand to complete this and continue the Logic Audit Review, is to: 
   - In `PROJECT_STATE_CHECKPOINTS.md` at the bottom, list the Official Checkpoints and decide what their questions should be, based on the MAO_FLOW section that it references, showing where in the process the checkpoint is. I broke that MAO_FLOW document down into a bunch of smaller documents and this is the "INDEX" for it: `./AUDIT_LOGIC/MAO_FLOW/00_MAO_FLOW_CHAPTERS.md` 
   - Then we need to actually put the normal language into the code with the checkpoint markers and other directions 
   - Make any other changes to other files that maintain the conversation and display, etc. Way more tokens than I was even thinking about but I guess not that crazy if we can save a temp file to be able to code execute it to the free Files API, which 
   - Figure out how the Files API and the Code Execution works and make sure it is implemented throughout the process. 
   
* **Only then will we be ready to return back to GROUP 3 that we were working on of the Audit Review: `./AUDIT_LOGIC/AUDIT_REVIEW.md` 
