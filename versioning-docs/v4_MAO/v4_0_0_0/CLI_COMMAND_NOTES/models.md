# Command #3: `models`

## Phase 1: Sequential Think Requirements Analysis

**What functionality does this CLI command provide?**
- Scans `./configs/models/` directory to discover all available models
- Reads model JSON configs to extract existing `display_name` and metadata
- Displays models with UX-friendly information for model selection
- Works both as `mao models` and `/models`

**Which orchestrator files need integration?**
- **Primary**: `manager_models.py` - "Loads JSON configs and provides intelligent model selection"
- **Universal**: `cli_manager.py` (routing), `ui_terminal.py` (slash commands) 
- **Minimal complexity** - leverages existing model discovery patterns

**What manager methods will be called?**
- `ModelManager.discover_models()` or similar existing discovery method
- Existing model metadata and selection logic
- No new helper methods needed - use existing patterns

**What UI patterns are needed for display?**
- **Simple model listing** - let Claude organize naturally in conversation
- **Display priorities**: model name, display_name, capabilities, cost info
- **Data structure**: raw model data for Claude to organize contextually
- **UI Design Principle**: Essential data structure only, no predefined grouping

**Cost estimation approach (Claude Sonnet 4 costs):**
- Low cost: 0.002 (API message exchange with potentially large model list response)
- Conversation-based interaction with Sonnet 4 for model display
- Response caching critical for cost optimization

**Caching strategy and fingerprinting needs:**
- **Cache duration**: 10 minutes (models directory changes)
- **Fingerprint includes**: Models directory modification time, model JSON file count, model file modification times
- **Cache key**: Include models directory state hash for invalidation when models added/removed/updated

### **Special Requirements & Implementation Notes:**

**No Schema Enhancement Needed:**
- ✅ Model JSON files already have `display_name` fields
- ✅ No file modifications required (unlike tools command)
- ✅ Ready to use existing display names

**No Hardcoded Grouping:**
- ❌ **NO** predefined categorization strategies
- ✅ Raw model data only - let Claude organize naturally
- ✅ Dynamic organization based on conversation context
- ✅ Future-proof against new model types and providers

**No Backward Compatibility:**
- ❌ **NO** backward compatibility requirements per MAO Protection Rules
- ✅ Clean implementation without legacy considerations
- ✅ Follow MAO standardization patterns only

---

### **Implementation Plan Summary**

**Files to Create:**
1. **`configs/cli/models/models.py`** - Logic with model discovery (no categorization)
2. **`configs/cli/models/ui_models.py`** - Data-focused display patterns 
3. **Update `configs/cli/models/models.json`** - Add cost estimate and enhanced config

**Key Implementation Features:**
- ✅ Model discovery from existing `manager_models.py` integration
- ✅ Raw model data output (no hardcoded grouping)
- ✅ Conversation-optimized cost estimation (0.002 for API exchange)
- ✅ Caching with models directory fingerprinting (10-minute duration)
- ✅ Data-only UI patterns preserving creative freedom
- ✅ Universal touchpoints (cli_manager, ui_terminal) integration

**Why This Command Builds on #2:**
- **Tests manager integration patterns** across different system components
- **Validates caching strategies** for directory-based discovery
- **No schema enhancement needed** (unlike tools command)
- **Clean implementation** without hardcoded assumptions

---

## 🚀 **Ready to Implement Command #3!**

Much cleaner approach! No hardcoded grouping, no unnecessary schema changes, proper cost estimation for API conversation.

**Should I proceed with implementing the 3-file structure:**
1. `configs/cli/models/models.py` - Logic with clean model discovery
2. `configs/cli/models/ui_models.py` - Data-focused display patterns  
3. Enhanced `configs/cli/models/models.json` - With proper cost estimate

This will test manager integration patterns without the complexity of schema enhancement! 💎🔧