# Context Primer for Complete Codebase Audit

RUN:
    git ls-files 

ACTIVATE: 
    Start the `sequential thinkink` MCP tool and use it to think while you review the following between thoughts. 

LOOKUP: 
    Start the `memory` MCP server and search for the project entity using the exact search term `Mao_v4_Build`. Read recent entries related or given an actual relation to `Full_Codebase_Audit`.

MAINTAIN: 
    Please maintain the `memory` MCP server by creating Project State entries using the same entity `Mao_v4_Build` and creating a relation to tag called `Full_Codebase_Audit`. These are the update times: 

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
    Before starting any batch, query: "What is the current state of Full_Codebase_Audit for Mao_v4_Build?"
    Before each decision point, save: "Decision point [X] reached - [current progress summary]"
    After each stage, save: "Stage [X] completed - [deliverables and next steps]"

READ: 
    - `/Users/seanivore/Development/modular-agent-orchestrator/tests/FULL_CODEBASE_AUDIT/WORKFLOW_README.md`
    - `/Users/seanivore/Development/modular-agent-orchestrator/tests/FULL_CODEBASE_AUDIT/PROGRESS_CHECKLIST.md`
    - `/Users/seanivore/Development/modular-agent-orchestrator/documentation/FILE_STANDARDIZATION_RULES.md`
    - `/Users/seanivore/Development/modular-agent-orchestrator/documentation/CONTENTS.md`

ACCOMPLISH: 
    `/Users/seanivore/Development/modular-agent-orchestrator/tests/FULL_CODEBASE_AUDIT/codebase_audit_spec.md`
    `/Users/seanivore/Development/modular-agent-orchestrator/tests/FULL_CODEBASE_AUDIT/documentation_spec.md`

WORKFLOW: 
    `/Users/seanivore/Development/modular-agent-orchestrator/.claude/commands/codebase_audit_docs.md`