# Zed Editor: Critical Feedback from an AI-First Developer

## Core Diagnosis

The fundamental issue isn't just features - it's philosophy. Someone who hasn't lived and breathed AI-assisted development is making decisions about AI features. Evidence:

1. **Token-Blind Development**
   - Creating new files instead of reading/editing (massive token waste)
   - No consideration of token efficiency in basic operations
   - Rate limits in free tier (!?) shows fundamental misunderstanding
   - Basic operations like editing markdown shouldn't trigger limits

2. **Market Misread**
   - Treating AI as a "side feature" rather than core workflow
   - Email about "not interrupting normal coding flow" reveals mindset
   - Missing that IDEs themselves are evolving into AI interfaces
   - 6-month horizon for IDE investment given current AI pace
   - Competition (Cursor) shipping AI-first updates constantly

3. **Philosophical Disconnect**
   - Built as "Rust IDE with AI features"
   - Should be "AI interface that happens to be an IDE"
   - Stability issues suggest focus on wrong priorities
   - Basic AI workflow issues would be obvious to AI-native devs

Someone who doesn't primarily develop using AI/Agentic tools appears to be developing this app's AI features — there are too many basic UX/UI issues that would be immediately apparent to any developer who relies on AI assistance daily.

## Fundamental Issues with AI Implementation

1. **Rate Limiting Makes AI Features Unusable**
   - Hits limits during AI's own operations (!)
   - Interrupts mid-file-edit
   - Claims "free messages" but has rate limits
   - No warning before limits hit
   - No indication of reset time
   - Competitors (Cursor) have no such limitations
   - Makes continuous development impossible

2. **Basic AI UX Missing**
   - No clickable files in chat
   - No image support
   - No spellcheck in AI messenger
   - No right-click menu
   - Character count instead of tokens
   - No context window management tools
   - No way to recover chat state

3. **Stability Issues**
   - Crashes during AI operations
   - No crash recovery
   - Less stable than Electron-based competitors
   - Chat context lost on crash
   - No auto-save of interactions
   - Rust promises unfulfilled

## Basic Developer Workflow Broken

1. **Root Directory Issues**
   - Can't create/save files without root
   - No explanation of failures
   - Forces understanding of internal architecture
   - No temporary file support
   - Even AI tools fail without root
   - Empty window with no guidance

2. **File Edit UX Problems**
   - Inconsistent edit approval UI
   - Sometimes opens new window
   - Sometimes no visible changes
   - No in-chat diff preview
   - No configurable approval modes
   - Less functional than Cursor's "YOLO mode"

3. **Theme/Settings Management**
   - Some themes break basic functionality
   - JSON syntax highlighting randomly disabled
   - No color picker for hex values
   - Settings revert unexpectedly
   - No JSONC support
   - Poor documentation

## Impact on Development

1. **Workflow Disruption**
   - Constant rate limit interruptions
   - Lost context after crashes
   - Manual list numbering required
   - Settings need frequent reconfiguration
   - Basic operations blocked

2. **Missing AI-First Features**
   - No token management
   - No image sharing
   - Poor error handling
   - Limited tool documentation
   - No chat state persistence

3. **Migration Barriers**
   - All issues more severe than Cursor/VSCode
   - Basic functionality less reliable
   - AI features more limited
   - Settings less persistent
   - Documentation inadequate

## Required Changes for Viability

1. **Immediate Fixes Needed**
   - Remove/rework rate limits
   - Add crash recovery
   - Fix root directory UX
   - Add token counter
   - Improve error messages
   - Make file operations reliable

2. **Core Feature Gaps**
   - AI context persistence
   - Image support
   - Better edit preview
   - Settings stability
   - Theme reliability

3. **Developer Experience**
   - JSONC support
   - Color picker
   - Better documentation
   - Configurable approval modes
   - Chat state management

## Current Status
- Context Window: 37k/200k (good feature, poor implementation)
- Platform: macOS
- Previous Editor: Cursor/VSCode
- Migration Status: Blocked by fundamental issues
- Comparison: Cursor provides all missing features without limitations

## Conclusion

The vision of an AI-first, Rust-based editor is promising, but the current implementation suggests a fundamental disconnect between the development team and AI-driven development practices. Many issues would be immediately apparent to developers who rely on AI tools daily.

The per-minute rate limiting particularly exemplifies this disconnect - it treats AI interaction like an API service rather than a continuous development dialogue. Rate limiting a text chat conversation makes no sense, especially when:

- Messages are part of the same conversation
- AI is mid-task or mid-file-edit
- User has "free messages" remaining
- Competition offers unlimited interaction

Without a dramatic philosophical shift toward truly AI-first development, Zed risks falling behind as IDEs evolve into AI interfaces. The market isn't waiting for "Rust IDEs with AI features" - it needs "AI interfaces that happen to be IDEs."
