# Context Primer Every Session

ACTIVATE: 
    Start the `sequential_thinking` MCP tool and use it to think while you review the following between thoughts. 

LOOKUP: 
    Run the `memory` MCP tool and search the EXACT term `MAO_UI_Context_Priming_Strategy` in MCP memory and then read these docs in full:**

READ: 
    `./CLAUDE.md` --> Complete development rules including new UI Development Guidelines section
    `./documentation/10_AI_DEV_INDEX.md` --> Complete Python backend architecture understanding
    `./versioning/v4_0_0/IMPL_UI/UI_CURRENT_STATE.md`--> Current working UI implementation state

UNDERSTAND: 
    Architecture Flow: User Input → ChatInterface.tsx → PythonBridge.ts → ui_terminal.py → orchestrator/ → Response
    Current Working: interfaces/mao/ with Ink 6.1+, React 19.1+, subprocess communication