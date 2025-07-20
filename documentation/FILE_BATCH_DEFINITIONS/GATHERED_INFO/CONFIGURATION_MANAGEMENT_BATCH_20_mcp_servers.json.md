# Configuration Management - mcp_servers.json

**File Location:** `/Users/seanivore/Development/modular-agent-orchestrator/configs/connections/mcp_servers.json`

## Simple Sentence Form

**Overview:** MCP servers configuration defines external tool integration capabilities through Model Context Protocol with comprehensive server definitions for aider, filesystem, brave_search, and github tools including command specifications, requirements, and global settings.

## Code & Explanation

**Architecture Overview:**
- **MCP Server Ecosystem:** Implements comprehensive Model Context Protocol server configurations for external tool integration with standardized command and requirement specifications
- **Selective Enablement Strategy:** All servers configured with "enabled": false requiring explicit activation for security and resource management
- **Tool Capability Declaration:** Each server explicitly declares available tools (edit_file, brave_web_search, create_repository) for dynamic tool discovery
- **Dependency Management:** Specifies exact requirements (aider-chat, @modelcontextprotocol packages) and environment variables for proper server operation
- **Global Configuration Framework:** Implements system-wide settings (30s timeout, 3 retry attempts, INFO logging) for consistent MCP server management

**MCP Server Categories:**
- **Code Editing (Aider):** Python-based code editing server with file manipulation capabilities
- **File Operations (Filesystem):** Node.js filesystem server for comprehensive file system operations
- **Web Search (Brave):** Search integration requiring BRAVE_API_KEY for web search capabilities
- **Version Control (GitHub):** Repository operations requiring GITHUB_TOKEN for GitHub integration

**Recommended Documentation Location:** `./docs/mcp/server-integration-architecture.md` for MCP server configuration and external tool integration patterns

## Written & Illustrated Data Info

**Data In-Flow:**
- MCP server activation requests requiring server enablement and dependency validation
- Tool capability discovery requiring available tool enumeration and capability assessment
- External API integration requiring environment variable configuration and authentication setup
- Server dependency installation requiring package and requirement management

**Data Out-Flow:**
- MCP server availability confirmation with tool capability specifications
- Dependency requirement validation with installation and configuration guidance
- Authentication setup guidance for API-dependent servers (Brave, GitHub)
- Tool integration capability assessment with server enablement recommendations

**Key Configuration Elements:**
```json
{
  "servers": {
    "filesystem": {
      "command": ["npx", "@modelcontextprotocol/server-filesystem"],
      "enabled": false,
      "tools": ["read_file", "write_file", "list_directory"]
    },
    "brave_search": {
      "env_vars": ["BRAVE_API_KEY"],
      "tools": ["brave_web_search"]
    }
  },
  "global_settings": {
    "timeout_seconds": 30,
    "retry_attempts": 3
  }
}
```

**Integration Points:**
- MCP integration systems use server configurations for external tool connectivity
- Tool discovery frameworks reference server tool declarations for capability enumeration
- Dependency management systems use requirements for server installation and setup
- Authentication managers coordinate environment variable setup for API-dependent servers

**Privacy and Local Storage Compliance:**
- MCP server configurations stored locally ensuring user control over external tool integration
- Selective enablement preventing unauthorized external connections without user consent
- Local dependency management without external configuration dependencies
- User-controlled API integration with local environment variable management for external services