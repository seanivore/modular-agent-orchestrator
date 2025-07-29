# Phase 1: Terminal-Native UI Enhancements 🎨

## Implementation Protocol 📋

**CRITICAL**: This guide requires **live tracking** during implementation. Update status indicators as you progress:
- ❌ **Not Started** - Section not yet begun
- ⚡ **In Progress** - Currently implementing
- ✅ **Complete** - Fully implemented and tested
- 🔍 **Testing** - Ready for testing phase
- ⚠️ **Issues** - Implementation problems found

**Deviation Documentation**: If you must deviate from specs, document the change and reason in the section.

## Design Reality Check ✅

**Foundation**: We're building **for the terminal**, not recreating web app patterns  
**Our Control**: Text choice, contextual semantic color-coding, white space  
**Terminal Handles**: Scrolling, history, keyboard shortcuts, visual indicators --> the terminal is basically the app 
**Core Experience**: Single-screen chat interface with intelligent message blocks

**Critical Design Principle**: "We hold very little and thus very careful control over all possible (few opportunities) for UX"

---

## 1. Message Block Behavior System 📜 ❌

### Current State *(Screenshots confirmed: formatting needs fixes)*
- ✅ Basic chat working with real backend connection
- ⚠️ Each message needs Claude Code-style formatting fixes  
- ⚠️ No intelligent text management or courteous behavior
- ⚠️ Messages don't "take care of themselves" with space optimization

### Implementation Status
- ❌ Dynamic Theme System (6 adaptive color modes)
- ❌ Message Block Components 
- ❌ Courteous Behavior Logic
- ❌ Semantic Color Assignment
- ❌ Testing Protocol

### Enhancement Plan
**A. Implement "Courteous" Message Blocks**
- **Core Behavior**: Every message block constantly re-evaluated and re-written in real-time
- **Space Management**: Only use as much space as absolutely necessary
- **Auto-Hide Logic**: All 'no longer needed' text is hidden first (updates on progress presumed already seen)
- **Truncation Rules**: Long form text truncated to first line + second line
- **Expansion Method**: Hidden text shows: `... +37 lines (ctrl+r to expand)`
- **Paragraph Hiding**: Faded, less legible color: `... +37 lines (press ctrl-w to expand)`

**B. Action Lists Management**
- **List Types**: Action lists (project todos) OR List of Actions (master todo)
- **Space Courtesy**: Both "take care of themselves" using only necessary space
- **Real-time Updates**: Constantly re-evaluated for accuracy and conciseness

**C. Message Block Types**
1. **Conversational Text Messages**
   - Bullet points most common from AI
   - **MAIN HIGHLIGHT COLOR** (pink/bold) for key info (first few words)
   - Paragraphs concise, separated by line breaks
   - User text: **LIGHT GRAY TEXT** with `>` bullet point
   - Numbered lists: **SYSTEM TEXT COLOR** throughout
   - URLs highlighted in **SUPER LIGHT BLUE ALMOST WHITE COLOR**

2. **Pasted Text Blocks**
   - Paste indicator avoids chaotic chat history
   - Format: `[289 tokens of pasted text]` or inline `[653 tokens of pasted text]`
   - **Threshold Logic**: Show full text under 100 tokens (≈3 long sentences)
   - Over threshold: Convert to token count indicator

**Files to Create:**
- `MessageBlock.tsx` - Core message block component with courteous behavior
- `ActionList.tsx` - Action list management with real-time updates
- `TextBehavior.ts` - Text truncation, expansion, and auto-hide logic
- `PastedTextHandler.ts` - Token counting and paste formatting

### Testing Protocol for Message Blocks 🧪
**MUST TEST each message type before proceeding:**

**Test 1: User Messages**
```bash
# Send regular user message - should show:
> Hello mao
# Expected: Gray `>` bullet, gray text
```

**Test 2: AI Conversational**
```bash
# Ask for explanation - should show:
● Here are 3 ideas for improving...
# Expected: White `●` bullet, yellow text, pink bold for key words
```

**Test 3: Action Lists**
```bash
# Trigger workflow - should generate:
○ Task (Analytics report generation)
  └── ▶︎ Download monthly data...
# Expected: Empty circle `○` bullet, active sub-tasks with triangles
```

**Test 4: Pasted Text (>100 tokens)**
```bash
# Paste large content - should show:
> [289 tokens of pasted text]
# Expected: Token count indicator, not full text
```

**Test 5: Courteous Behavior**
```bash
# Generate long response - should auto-truncate with:
● First line of response...
  └── ... +37 lines (ctrl+r to expand)
# Expected: Automatic truncation with expansion hint
```

### **E. Dynamic Theme System** *(6 Adaptive Color Modes)*

**Core Philosophy:** Colors adapt to user's terminal settings for native feel

**6-Color System:**
1. **MAIN HIGHLIGHT COLOR** - From user's terminal bold/accent (your pink `#ff49ff`)
2. **SYSTEM TEXT COLOR** - From user's terminal default text (your yellow `#f1d771`)  
3. **FADED SYSTEM TEXT COLOR** - Dimmed version of #2 for secondary info
4. **LIGHT GRAY TEXT** - Neutral secondary information (`#bbbcbb`)
5. **SUPER LIGHT BLUE ALMOST WHITE** - Subtle accents (`#f0f8ff`)
6. **BABY BLUE DARKER VERSION** - Stronger blue accents (`#82d0ff`)

**Theme Modes:**
- **Dark Mode** - Standard dark terminal (current implementation)
- **Light Mode** - Light terminal adaptation  
- **Dark Mode Colorblind-Friendly** - Enhanced contrast with color differentiation
- **Light Mode Colorblind-Friendly** - Light version with accessibility
- **Dark Mode ANSI Colors Only** - Limited color palette compatibility
- **Light Mode ANSI Colors Only** - Light version with basic colors

**Implementation Strategy:**
- Colors 1 & 2 detect from user's terminal settings when possible
- Fallback to theme-specific defaults when detection unavailable
- Same semantic meaning across all 6 modes (pink=attention, etc.)
- Visual theme selection panel (like your config screenshot)

---

## 2. "Thinking" AI Behavior Word 🧠 ❌

### Current State
- No indication when backend is processing
- Static responses without personality
- **Existing Design**: Triangle indicators in `_DESIGN_RULES.md` (`▲ Mao thinking and planning`)

### Implementation Status
- ❌ Context-aware thinking words
- ❌ Display rules (show/hide logic)
- ❌ Token/time tracking
- ❌ ESC interrupt capability

### Enhancement Plan
**A. Implement AI Improv Word System** *(Links to existing welcome logic)*
- **Context-aware words**: `+ Organizing...`, `+ Sparkling...`, `+ Flibbergitting...`
- **Display format**: `(107s • 2.9k tokens • esc to interrupt)`
- **AI-generated**: Based on conversation context, not pre-written
- **Emotional Intelligence UX**: Target "audible noise like gasp or LOL" response
- **Example contexts**: "budgeting" after API cost discussion, "celebrating" after audit completion

**B. Strategic Display Rules** *(From TEXT_HISTORY_MANAGEMENT.md)*
- **Show when**: Established back-and-forth (after 4+ message volleys)
- **Hide when**: General responses, first responses, initial messages
- **Visual indicator**: Existing pulsing triangle `▲ Mao thinking and planning`
- **Timing focus**: When app could use more "movement" during planning/wrapping up
- **Conversation flow**: Only when there's established dialogue rhythm

**C. Technical Implementation**
- **Token tracking**: Count actual tokens used during thinking
- **Time tracking**: Real-time elapsed seconds display
- **Interrupt capability**: ESC key cancellation (like Claude Code)
- **Context analysis**: Determine appropriate thinking word from conversation state

**D. Integration with Welcome Text Logic**
- Same contextual word generation system used in welcome screen
- Consistent emotional intelligence approach across all UI states
- Link to existing triangle/circle indicator system from `_DESIGN_RULES.md`

**Files to Modify:**
- `ChatInterface.tsx` - Add thinking state management with display rules
- `PythonBridge.ts` - Add timing, token tracking, and interrupt handling
- `ui_terminal.py` - Generate contextual thinking words (link to welcome logic)
- `ThinkingWordGenerator.ts` - AI-driven contextual word creation
- **Reference**: `_DESIGN_RULES.md` lines 875-885 for visual indicators

---

## 3. Terminal-Native Slash Commands 💻 ⚡

### Current State *(Screenshots confirmed working!)*
- ✅ `/config` slash command triggers configuration panel  
- ✅ Beautiful terminal-native theme selection with live preview
- ✅ Real Mao backend connection working (`Real Mao received: meow`)
- ⚠️ Need autocomplete integration with existing `discover_cli_commands()` function
- ✅ Found: `orchestrator/cli_manager.py` has dynamic command discovery infrastructure

### Implementation Status
- ✅ Basic `/config` panel working
- ❌ Claude Code-style autocomplete
- ❌ Space management for suggestions
- ❌ CLI discovery integration

### Enhancement Plan
**A. Claude Code-Style Autocomplete** *(✅ Config panel implementation confirmed from screenshots)*
- **Space Management**: Space appears when typing `/` to accommodate suggestions
- **Navigation**: Up/down arrows to navigate, continue typing to narrow
- **Visual Behavior**: Input field nudges up to make room (not overlay)
- **Content Strategy**: Include recent/most used commands in suggestions
- **Keyboard Flow**: Type what you want OR use arrows OR keep typing to narrow
- **Integration**: Connect to existing `discover_cli_commands()` from `orchestrator/cli_manager.py`

**B. Real CLI Integration**
- **Dynamic Discovery**: Connect to actual `CLIManager` methods
- **JSON Config Integration**: Dynamic command discovery from configs/cli/*.json
- **Validation**: Real-time command validation during typing
- **Method Routing**: Direct connection to interface methods specified in JSON

**C. Configuration Panel** *(Image review needed)*
- **Claude Code Style**: Modal-style config panel triggered by `/config`
- **Simple Toggles**: Space bar for options with few choices
- **Complex Settings**: Enter key for multi-option settings (themes)
- **Auto-save**: No manual save button - changes applied on selection
- **Visual Themes**: Show theme previews (not individual color picking)
- **Efficiency Goal**: Implement all app config settings at once

**D. Command History Integration**
- **Up Arrow Behavior**: Populate previous sent messages (like Claude Code)
- **Recent Commands**: Include in autocomplete suggestions
- **No Separate System**: Avoid keybinding conflicts, use existing autocomplete

**Files to Modify:**
- `ChatInterface.tsx` - Add autocomplete space management and input nudging
- `CommandAutocomplete.tsx` - Terminal-native autocomplete with space allocation
- `ConfigPanel.tsx` - Modal configuration interface with Claude Code UX
- `CommandHistory.ts` - Integration with autocomplete system
- **Reference**: Existing implementation in CLI autocomplete docs

---

## 4. Visual Chat Interface Fixes 🎨

### Current State *(Image review needed)*
- Need to fix message block stroke containers
- High-fidelity chat reference exists in action lists section
- Basic color scheme needs semantic refinement

### Enhancement Plan
**A. Message Block Containers**
- **Fix Implementation**: Stroke container system for message encapsulation
- **Reference Standard**: Match high-fidelity reference design exactly from action lists
- **Visual Hierarchy**: Proper spacing between message blocks
- **Container Behavior**: Responsive containers that adapt to terminal width

**B. Semantic Color System Implementation**
- **MAIN HIGHLIGHT COLOR** (pink/bold): Key information, first words of bullets
- **SYSTEM TEXT COLOR** (faded): Secondary info, timestamps, metadata
- **LIGHT GRAY TEXT**: User messages exclusively, always with `>` bullet
- **SUPER LIGHT BLUE ALMOST WHITE**: URLs and special links in numbered lists
- **Color Logic**: Conceptual syntax shades that work together, not arbitrary color picking

**C. Visual Brand Integration**
- **Reference Document**: Full implementation from `_VISUAL_BRAND_IDENTITY.md`
- **Terminal Constraints**: Work within terminal app's rendering capabilities
- **Consistency**: Maintain visual coherence across all message types

**Files to Modify:**
- `ChatInterface.tsx` - Fix message containers and implement stroke system
- `ColorSystem.ts` - Implement complete semantic color scheme
- `MessageContainer.tsx` - Dedicated container component with proper styling
- **Reference**: `_VISUAL_BRAND_IDENTITY.md` for complete color system

---

## 5. Action Lists: The Core UX Innovation 🎯

### Current State
- No action list functionality
- Missing the key "immediacy" UX feature

### Enhancement Plan
**A. Action List Types and Behavior**

**1. Finalized and Inactive Lists**
- **Visual State**: Filled circle `●` indicates completion
- **Collapsed Format**: 
  ```
  ● Task (Project memory updates)
    └── Done ($0.003 • 400 tokens • 8.3s)
  ```
- **Display Logic**: Originally had full todo list, collapsed to two lines on completion
- **Movement**: Completed tasks move above master list after collapsing

**2. Inactive but Not Finalized Lists (Master Lists)**
- **Visual State**: Empty circle `○` when inactive
- **Behavior**: Remains present, updates after each task completion
- **List Management**: New action lists created below, completed move above
- **Task Indicators**: Filled/empty triangles `▶︎`/`▷` show completion state

**3. Active Lists - The Key UX Feature**
- **Visual State**: Blinking circles (filled to empty) `○` when active
- **Rapid Changes**: Items change rapidly as AI completes actions
- **Immediacy UX**: "Provides sense of things getting done faster than they actually are"
- **Information Relevance**: Shows info helpful NOW for those few seconds it's active
- **User Emotion**: "Imagine staring at static list waiting, begging for just one more tool use!"

**B. Detailed Implementation Specs**

**Project Lists**:
```
○ Task (Analytics report generation)
  └── Update Todos
      ▶︎ Download monthly user data from agent deliverable  
      ▶︎ Download monthly system metrics from agent deliverable 
      ▷ Compile comprehensive data sets 
      ▷ Read last month's reports 
```

**Administrative Lists**:
```
○ Task (Preparing next project; Workflow ID: UID-1283)
  └── Read 54 lines (ctrl+b to expand)
      Read 88 lines (ctrl+b to expand)
      + 8 more tool uses
```

**File Path Lists**:
```
○ Task (Audit Commands 7-9 Orchestrator Integration)
  └── /Users/seanivore/Development/modular-agent-orchestrator/tools/web_search/
      button_web_search.py
      ... +37 lines (ctrl+r to expand)
      Bash (find /Users/seanivore/Development/modular-agent-orchestrator/configs/cli)
      
      Waiting...
      +16 more tool uses
```

**C. Visual Design Specifications**
- **Bold text** = **MAIN HIGHLIGHT COLOR** (pink/bold)
- **Italic text** = **SYSTEM TEXT COLOR** (faded)
- **Indentation**: Deliberate spacing matches actual terminal output
- **Icons**: Tree branches `└──`, triangles `▶︎`/`▷`, circles `●`/`○`
- **High-fidelity**: Exact representation of final product appearance

**Files to Create:**
- `ActionList.tsx` - Core action list component with all three types
- `ActionListManager.ts` - State management for rapid updates
- `TaskIndicators.tsx` - Circle and triangle visual states
- `RapidUpdateHandler.ts` - Real-time content changes for immediacy UX

---

## 6. Error Handling & Communication 🚨

### Current State
- Basic error fallbacks to mock responses
- No human-friendly error translation

### Enhancement Plan
**A. Mao Error Translation System**
- **Conversational Errors**: Convert technical errors to human explanations
- **Actionable Solutions**: Provide specific fix suggestions
- **Tone Consistency**: Maintain Mao's conversational personality during errors
- **Integration**: Errors flow through normal message block system

**B. Error Communication Strategy**
- **No Special UI**: Use standard message block behavior for errors
- **Message Format**: Mao explains error + simplified explanation + fix method
- **Reference Implementation**: Details in `_NEW_USER_FLOW.md`
- **Human Translation**: Convert backend errors to understandable language

**C. Implementation Requirements**
- **Error Detection**: Catch technical errors from Python backend
- **Context Awareness**: Understand what user was trying to accomplish
- **Solution Mapping**: Map common errors to known fixes
- **Learning System**: Improve error explanations based on user responses

**Files to Modify:**
- `ErrorHandler.ts` - Human-friendly error translation engine
- `ui_terminal.py` - Enhanced error communication to frontend
- `ErrorMessageFormatter.ts` - Convert errors to conversational format
- **Reference**: `_NEW_USER_FLOW.md` for error handling specifications

---

## 7. Context Window Management 📊

### Current State
- No token counting or context awareness
- No smart history management

### Enhancement Plan
**A. Smart Context Management**
- **Tiny Pie Chart**: Cursor-style context window percentage indicator (◐ 27%) always visible
- **Token Counting**: Track toward 200k context window limit with real-time updates
- **Claude Code Method**: Summarize old messages when approaching limit
- **Conversation Continuity**: Maintain thread coherence during summarization
- **Memory Management**: Preserve important context while reducing tokens

**B. Performance Optimization**
- **Terminal History**: Unlimited like macOS Terminal (no performance issues)
- **LLM Constraints**: Context limits only for language model interactions
- **Design Decisions**: Smart truncation based on conversation importance
- **Action List Memory**: Efficient management of rapidly-changing content

**C. Implementation Strategy**
- **Token Tracking**: Real-time counting of conversation tokens
- **Summarization Triggers**: Automatic summary when approaching limits
- **Context Preservation**: Keep recent messages, summarize older content
- **User Transparency**: Indicate when summarization occurs

**Files to Create:**
- `ContextManager.ts` - Token counting and summarization logic
- `ConversationSummarizer.ts` - Intelligent message summarization
- `TokenCounter.ts` - Real-time token tracking for all message types

---

## Implementation Approach

### **Phase 1A: Visual Foundation**
1. **Fix visual chat interface** *(Image review: need-to-fix-mao-chat.png)*
2. **Implement message block stroke containers**
3. **Deploy semantic color system**
4. **Create message block behavior foundation**

### **Phase 1B: Action Lists - Core Innovation**
1. **Build three action list types** (finalized, inactive, active)
2. **Implement rapid-changing feedback UX** (the key emotional feature)
3. **Add completion/collapse behavior with cost/time tracking**
4. **Create real-time update system for "immediacy" feeling**

### **Phase 1C: Terminal UX Excellence**
1. **Slash command autocomplete** *(Image review: before/after-typing-slash.png)*
2. **Configuration panel** *(Image review: config-slash-command-panel.png)*
3. **"Thinking" AI word system with emotional intelligence**
4. **Command integration with real CLI manager**

### **Phase 1D: Polish & Advanced Features**
1. **Error handling with human-friendly translation**
2. **Context window management with smart summarization**
3. **Performance optimization for extended sessions**
4. **Integration testing of all courteous text behaviors**

---

## Success Metrics

**User Experience:**
- **Zero Conflicts**: No interference with terminal app behavior
- **Single-Screen Flow**: Intuitive chat experience with no mode switching
- **Immediacy Feeling**: Action lists make progress feel faster than reality
- **Emotional Response**: "Audible noise" reactions to AI thinking words
- **Command Discovery**: Under 3 keystrokes to find any command

**Technical:**
- **100% Real Integration**: No mock responses in production
- **Smart Context**: Automatic handling approaching 200k token limit
- **Memory Efficiency**: Under 50MB for extended sessions
- **Response Time**: Under 200ms for all UI interactions

**Visual:**
- **Exact Match**: High-fidelity reference designs implemented perfectly
- **Semantic Colors**: Complete MAIN/SYSTEM/LIGHT GRAY/SUPER LIGHT BLUE system
- **Container Perfection**: Message block stroke containers working flawlessly
- **Courteous Text**: All message blocks managing space intelligently

**Innovation Metrics:**
- **Rapid Updates**: Action lists changing in real-time during tool execution
- **Space Courtesy**: All text blocks using minimal necessary space
- **Contextual Intelligence**: AI thinking words match conversation context
- **Terminal Native**: Feels like native terminal app, not web app port

---

## Image Review Schedule

**Ready for images when we reach each section:**
1. **need-to-fix-mao-chat.png** - Section 4: Visual chat interface fixes
2. **before/after-typing-slash.png** - Section 3: Autocomplete implementation  
3. **config-slash-command-panel.png** - Section 3: Configuration panel design
4. **High-fidelity action lists reference** - Section 5: Action list behavior

**Next Phase Preview**: Phase 2 will build on this terminal-native foundation to add tool ecosystem integration, workflow visualization, and advanced orchestration features. The courteous message blocks and action lists will provide the perfect framework for displaying complex multi-agent workflows.

---

## Comprehensive Testing Protocol 🧪

### Pre-Implementation Testing Setup
**Required before starting any implementation:**

1. **UI Access**
```bash
cd interfaces/mao
chmod +x ./dist/cli.js
./dist/cli.js --name=seanivore
```

2. **Backend Connection** *(Automatic - UI handles this)*
- UI automatically starts Python backend at project root
- Look for: "🚀 Starting Python backend at: /.../mao_v4.py"
- Status indicator: "● connected" (bottom right)

### Testing Each Implementation Section

#### Section 1: Message Block System Testing 🔍
**Execute BEFORE marking Section 1 as ✅**

**Test A: Basic Message Types**
```bash
# User message test
hello mao
Expected: Gray > bullet, gray text

# AI response test  
what are 3 ways to improve this?
Expected: White ● bullet, yellow text, pink bold keywords

# List response test
give me a bulleted list of features
Expected: White ● bullet, proper bullet formatting
```

**Test B: Action List Generation**
```bash
# Workflow trigger test
/goal "create a simple analytics report"
Expected: Action lists with ○ bullets, sub-tasks with ▶︎/▷

# Real-time updates
Watch for: Rapidly changing content, blinking indicators
```

**Test C: Pasted Text Handling**
```bash
# Large paste test (copy long text >100 tokens)
Paste large content here...
Expected: [XXX tokens of pasted text] indicator

# Small paste test (copy short text <100 tokens)  
Paste short text here
Expected: Full text display, no tokenization
```

**Test D: Courteous Behavior**
```bash
# Long response test
explain the entire MAO system in detail
Expected: Auto-truncation with "ctrl+r to expand" 

# Completed task collapse
Wait for task completion
Expected: Collapse to "Done ($0.003 • 400 tokens • 8.3s)"
```

#### Section 2: Thinking Words Testing 🔍
**Execute BEFORE marking Section 2 as ✅**

```bash
# Context-aware thinking test
ask complex question after 4+ message exchanges
Expected: AI improv word like "+ Organizing... (107s • 2.9k tokens • esc to interrupt)"

# Display rules test  
ask simple question immediately
Expected: NO thinking word shown (too early in conversation)

# Interrupt test
ESC key during thinking
Expected: Process cancellation with graceful exit
```

#### Section 3: Slash Commands Testing 🔍
**Execute BEFORE marking Section 3 as ✅**

```bash
# Autocomplete test
Type: /
Expected: Space appears below with command suggestions

# Navigation test  
Type: /he and use arrow keys
Expected: /help highlighted, can select with arrows

# Config panel test
Type: /config
Expected: Modal config panel opens with theme options
```

#### Section 4: Visual Protocol Testing 🔍
**Execute BEFORE marking Section 4 as ✅**

```bash
# Theme system test
/config → select different theme
Expected: All colors update immediately, maintain semantic meaning

# Bullet protocol test
Send multiple message types
Expected: Correct bullet colors per VISUAL_BRAND_IDENTITY.md specs

# Spacing test
Send long conversation
Expected: Clean 3-space bullet indentation, proper line spacing
```

#### Section 5: Action Lists Testing 🔍 
**Execute BEFORE marking Section 5 as ✅**

```bash
# Action list types test
/goal "multi-step project"
Expected: All 3 types (finalized ●, inactive ○, active ○ blinking)

# Rapid updates test
Watch active task execution
Expected: Content changes rapidly, "immediacy" feeling

# Completion behavior test
Wait for task completion
Expected: Collapse, move above master list, show cost/time
```

### Integration Testing *(All Sections Complete)*

**Final Comprehensive Test**
```bash
# Full workflow test combining all features:
1. Start conversation (normal messages)
2. Trigger workflow (/goal command)  
3. Watch action lists with thinking words
4. Use /config to change themes
5. Paste large content
6. Test command autocomplete
7. Verify courteous behavior throughout

Expected: Seamless experience matching high-fidelity specs exactly
```

### Failure Protocol
**If any test fails:**
1. Mark section status as ⚠️ **Issues**
2. Document specific failure in the section
3. Fix implementation before proceeding
4. Re-test until ✅ **Complete**
5. Never proceed with failing components

**Testing Philosophy**: "Do it right the first time" - each component must match high-fidelity specs exactly before moving forward.