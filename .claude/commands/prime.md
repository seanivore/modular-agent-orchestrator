# Context Primer for Complete Codebase Audit

RUN:
    git ls-files 

ACTIVATE: 
    Start the `sequential thinkink` MCP tool and use it to think while you review the following between thoughts. 

LOOKUP: 
    Start the `memory` MCP server and search for the project entity using the exact search for `Mao_v4_Build` as well as `Full_Codebase_Audit_Mao_v4_Build` to find STATE RECOVERY updates from our final full codebase audit session. 

MAINTAIN: 
    Please maintain the `memory` MCP server by creating Project State entries using the entity 

    1. A batch of next steps for a session's tasks are planned 
    2. Mid-task if something changes or something notable comes up. 
    3. After each batch of steps within the sessions larger tasks.  
    4. At each decision point checkpoint for session recovery
    5. After each stage completion with detailed progress state
    6. When architectural discoveries or violation patterns are found

STATE RECOVERY:
    For session resumption, query Memory MCP for:
    - Current batch completion status (which of 24 batches are complete)
    - Current stage progress (which of 7 stages are complete)  
    - Decision point approvals (which quality gates have been passed)
    - Violation inventory progress (critical issues discovered so far)
    - Documentation updates written (architectural discoveries made)
    - Cross-file dependency mappings (integration touchpoints found)

CHECKPOINT QUERIES:
    Before starting any batch, query: "What is the current state of the task at hand?"
    Before each decision point, save: "Decision point [X] reached: PROGRESS SUMMARY HERE."
    After each stage, save: "Stage [X] completed: PROGRESS SUMMARY HERE."
