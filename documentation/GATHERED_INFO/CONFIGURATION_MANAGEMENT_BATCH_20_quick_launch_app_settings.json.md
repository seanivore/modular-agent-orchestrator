# Configuration Management - quick_launch_app_settings.json

**File Location:** `/Users/seanivore/Development/modular-agent-orchestrator/configs/settings/quick_launch_app_settings.json`

## Simple Sentence Form

**Overview:** Quick launch application settings control startup and login behavior with three distinct modes for automatic user session restoration, manual login requirements, or conditional continuation based on command-line usage.

## Code & Explanation

**Architecture Overview:**
- **Startup Behavior Control:** Implements three-tier startup system managing user session persistence and login requirements
- **Session Restoration Logic:** "Always" mode enables automatic user restoration from last session unless explicitly logged out
- **Manual Login Enforcement:** "Off" mode requires username login on every startup for enhanced security
- **Conditional Launch Pattern:** "Continue Only" mode enables `mao --continue` command for quick session resumption while defaulting to login otherwise
- **UI Startup Integration:** Places in "Startup & Navigation" section without preview but with comprehensive help text explaining login behavior

**Startup Mode Implementation:**
- **Always ("always"):** Automatic session restoration providing seamless user experience unless logout explicitly performed
- **Off ("off"):** Manual login required every startup ensuring security but requiring user interaction
- **Continue Only ("continue_only"):** Hybrid approach enabling command-line quick launch while maintaining login security for standard startup

**Recommended Documentation Location:** `./docs/startup/launch-behavior-architecture.md` for startup sequence management and user session restoration patterns

## Written & Illustrated Data Info

**Data In-Flow:**
- Startup behavior preference selection requiring launch mode configuration
- Session restoration requests checking quick launch setting for automatic login
- Security validation requiring startup behavior assessment for appropriate login enforcement
- Command-line launch requests needing conditional startup behavior validation

**Data Out-Flow:**
- Startup behavior confirmation with session restoration capability specifications
- Login requirement validation based on quick launch preference
- Security level confirmation matching startup behavior with user preferences
- Command-line capability validation for conditional quick launch scenarios

**Key Configuration Elements:**
```json
{
  "quick_launch": {
    "default": "always",
    "options": [
      {
        "value": "always",
        "description": "Launch app with user from last session, unless logged out"
      },
      {
        "value": "continue_only",
        "description": "Launch `mao --continue` to skip login, otherwise load Username login"
      }
    ]
  }
}
```

**Integration Points:**
- Startup sequence systems reference quick launch setting for appropriate login behavior
- Session management systems use setting for automatic restoration vs. manual login decisions
- Command-line handlers implement conditional quick launch based on startup preference
- Security frameworks adapt login requirements based on quick launch configuration

**Privacy and Local Storage Compliance:**
- Startup behavior preferences stored locally ensuring user control over session management
- Local session restoration without external dependencies for user privacy
- User-autonomous startup behavior selection without external monitoring
- Privacy-compliant session management supporting complete user control over login patterns