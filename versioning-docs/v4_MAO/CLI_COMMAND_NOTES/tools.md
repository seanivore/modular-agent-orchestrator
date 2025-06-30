# Command #2: `tools`

## **Phase 1: Sequential Think Requirements Analysis**

**What functionality does this CLI command provide?**
- Scans `./tools/` directory to discover all available tools
- Reads tool JSON configs to extract `name`, new `display_name`, and `description` fields
- Organizes tools by logical grouping for optimal UX (search tools, content tools, etc.)
- Displays clean, scannable list of available tools with their capabilities
- Works both as `mao tools` and `/tools`

**Which orchestrator files need integration?**
- **Primary**: `manager_tools.py` - existing tool discovery and management logic
- **Universal**: `cli_manager.py` (routing), `ui_terminal.py` (slash commands) 
- **Minimal complexity** - leverages existing tool discovery patterns

**What manager methods will be called?**
- `ToolManager.discover_tools()` or similar existing discovery method
- May need helper method for organizing tools by category/type
- Possible integration with tool metadata and capabilities

**What UI patterns are needed for display?**
- **Tool listing with grouping** - categorize by function (Search, Content, Development, etc.)
- **Display priorities**: tool name, description, clear capability summary
- **Data structure**: organized for easy scanning and selection
- **UI Design Principle**: Essential data structure for UI designers, not detailed formatting

**Cost estimation approach (Claude Sonnet 4 costs):**
- Very low cost: 0.001 (file system reading and basic JSON parsing)
- No AI model calls, minimal processing
- Similar to help command cost profile

**Caching strategy and fingerprinting needs:**
- **Cache duration**: 10 minutes (tools change less frequently than commands but more than help)
- **Fingerprint includes**: Tools directory modification time, tool JSON file count, tool file modification times
- **Cache key**: Include tools directory state hash for invalidation when tools added/removed/updated### **Special Requirements & Implementation Notes:**

**Display Name Enhancement:**
- **Add `display_name` field** to all tool JSON files for UI flexibility
- **Initial implementation**: Convert "name" field to title case (e.g., "brave_search" → "Brave Search")
- **Future enhancement**: Custom display names for better UX (e.g., "web_search" → "Web Search")

**Tool Grouping Strategy:**
- **Search Tools**: brave_search, web_search, perplexity_search
- **Content Creation**: text_editor, dalle_generate, graphic_design  
- **Development**: code_execution, file_operations, mcp_connector
- **System**: files_api, think
- **Dynamic grouping**: Based on tool metadata and capabilities

**Integration with Existing Systems:**
- Leverage existing `manager_tools.py` tool discovery
- Enhance tool JSON schema with display_name field
- Maintain backward compatibility with existing tool references

---

### **Implementation Plan Summary**

**Files to Create:**
1. **`configs/cli/tools/tools.py`** - Logic with tool discovery and categorization
2. **`configs/cli/tools/ui_tools.py`** - Data-focused display patterns for tool listing
3. **Update `configs/cli/tools/tools.json`** - Add cost estimate and enhanced config

**Key Implementation Features:**
- ✅ Tool discovery from existing `manager_tools.py` integration
- ✅ Display name enhancement for all 11 tool JSON files
- ✅ Smart tool categorization for optimal UX
- ✅ Caching with tools directory fingerprinting (10-minute duration)
- ✅ Data-only UI patterns preserving creative freedom
- ✅ Universal touchpoints (cli_manager, ui_terminal) integration

**Why This Command Builds on #1:**
- **Establishes tool enhancement patterns** (display_name field addition)
- **Tests existing manager integration** (manager_tools.py) 
- **Creates tool categorization templates** for other commands
- **Simple but demonstrates manager integration** beyond pure discovery---

### **Strategic Implementation Value:**

**This Command Establishes:**
- ✅ **Manager Integration Patterns** - First command to integrate with existing `manager_tools.py`
- ✅ **Tool Enhancement Framework** - Display name field addition to all 11 tools  
- ✅ **Categorization Templates** - Smart grouping system for optimal UX
- ✅ **JSON Schema Evolution** - Pattern for enhancing existing tool configs

**Dependencies & Integration:**
- **Universal Touchpoints**: cli_manager.py, ui_terminal.py (established ✅)
- **Manager Integration**: manager_tools.py (existing tool discovery)
- **Schema Enhancement**: All 11 tool JSON files need display_name field

---

## 🚀 **Ready to Implement Command #2!**

This comprehensive analysis follows our established template and builds perfectly on command #1. The tools command will test manager integration while establishing tool enhancement patterns for the entire system.

**Should I proceed with implementing the 3-file structure:**
1. `configs/cli/tools/tools.py` - Logic with tool discovery and categorization
2. `configs/cli/tools/ui_tools.py` - Data-focused display patterns  
3. Enhanced `configs/cli/tools/tools.json` - With full config details

Plus the **display_name field addition** to all 11 tool JSON files?

This will create our tool enhancement foundation and test manager integration! 💎🔧

