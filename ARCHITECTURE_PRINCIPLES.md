# 🚨 CRITICAL: Mao Architecture Principles 🚨

## 🏠 **LOCAL ONLY APPLICATION - NO WEB SERVICES**

**READ THIS FIRST:** Mao is a **LOCAL APPLICATION** that runs entirely on the user's own machine. It is **NOT** a web service, cloud application, or API-based system.

---

## 🚫 **WHAT MAO IS NOT:**
- ❌ **NOT a web application** (no HTML, CSS, web browsers)
- ❌ **NOT an API provider** (doesn't serve REST endpoints to external clients)
- ❌ **NOT a cloud service** (no remote servers, no multi-tenant hosting)
- ❌ **NOT a mobile app** (initially - though planned for future)
- ❌ **NOT a SaaS product** (no remote hosting of the application itself)

## ✅ **WHAT MAO IS:**
- ✅ **LOCAL terminal application** (runs on user's machine)
- ✅ **Self-contained Python backend** (mao_v4.py + modules)
- ✅ **Local TypeScript/Node.js terminal UI** (beautiful terminal interface)
- ✅ **Subprocess communication** (Node.js ↔ Python via stdin/stdout/IPC)
- ✅ **Local file system** (all configs, data, logs stored locally)
- ✅ **API consumer** (calls OpenAI, Anthropic, search APIs, etc.)
- ✅ **Personal productivity tool** (like Claude Code, not like web apps)
- ✅ **Future subscription model** (download configs/tools/workflows)

---

## 🏗️ **ARCHITECTURE COMPARISON:**

### ✅ **MAO IS LIKE:**
- **Claude Code** (local terminal app that calls external APIs)
- **VSCode** (local app with rich UI and external integrations)
- **Photoshop** (runs on your machine, calls Adobe services)
- **Desktop applications** (self-contained with external API integrations)

### ❌ **MAO IS NOT LIKE:**
- **GitHub Codespaces** (web-based development environment)
- **Figma** (browser-based design tool)
- **Slack** (cloud service that other apps integrate with)
- **Google Docs** (web application)

---

## 🔧 **TECHNICAL ARCHITECTURE:**

```
User's Local Machine
├── TypeScript/Node.js Terminal UI (frontend)
│   ├── Rich terminal interface
│   ├── User input handling
│   └── Subprocess management
├── Python Backend (mao_v4.py)
│   ├── Core orchestration logic
│   ├── Tool ecosystem
│   ├── CLI commands
│   └── Local file operations
└── External API Calls
    ├── OpenAI/Anthropic APIs
    ├── Search APIs (Brave, Perplexity)
    ├── Other service APIs
    └── Future: Config/workflow downloads
```

**Local Communication:** Direct subprocess calls (Node.js ↔ Python)  
**External Communication:** HTTP API calls to services (Python → External APIs)  
**Data Storage:** Local files, NOT remote databases  
**Authentication:** Only for external APIs, not for local app access  
**Deployment:** User installs locally, NOT deployed to servers  

---

## 🎯 **FUTURE VISION:**

1. **Phase 1:** Local terminal application (current focus)
2. **Phase 2:** Local desktop application (Electron/Tauri wrapper)
3. **Phase 3:** Mobile application (running locally on phone/tablet)
4. **Phase 4:** Optional analytics aggregation (collect from multiple local instances)

**Even in future phases, the core principle remains: LOCAL FIRST, user owns their data and processing.**

---

## 💡 **FOR DEVELOPERS:**

When building ANY part of Mao:
- Think "**desktop app**" not "web app"
- Think "**subprocess calls**" not "API calls"  
- Think "**local files**" not "HTTP requests"
- Think "**terminal interface**" not "browser interface"
- Think "**personal tool**" not "multi-user service"

**If you find yourself thinking about APIs, web servers, authentication, or cloud deployment - STOP and re-read this document.**

---

## 📋 **REFERENCE FOR ALL DOCUMENTATION:**

Every documentation file should reinforce this principle. When in doubt, ask:
- "Does this run locally on the user's machine?" (Should be YES)
- "Does this require internet/servers?" (Should be NO)
- "Does this involve web technologies?" (Should be NO, except Node.js for terminal UI)
- "Is this like VSCode or like Google Docs?" (Should be like VSCode)

**This architecture principle overrides all other considerations and must be maintained throughout development.**
