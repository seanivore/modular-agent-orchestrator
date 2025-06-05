# Introducing Claude 4
Pricing remains consistent with previous Opus and Sonnet models: 
  - Opus 4 at $15/$75 per million tokens (input/output) and Sonnet 4 at $3/$15
  - 200k context window
  - 32k output max

From: claude-3-7-sonnet-20250219
To: claude-sonnet-4-20250514 or claude-opus-4-20250514

## Migration checklist
  - Update model id in your API calls
  - Test existing requests (should work without changes)
  - Remove token-efficient-tools-2025-02-19 beta header if applicable
  - Remove output-128k-2025-02-19 beta header if applicable
  - Handle new refusal stop reason
  - Update text editor tool type and name if using it
  - Remove any code that uses the undo_edit command
  - Explore new tool interleaving capabilities with extended thinking
  - Review Claude 4 prompt engineering best practices for optimal results
  - Test in development before production deployment 
  - https://github.com/anthropics/anthropic-cookbook?tab=readme-ov-file


| Model           | Base Input Tokens | 5m Cache Writes | 1h Cache Writes | Cache Hits & Refreshes |
| --------------- | ----------------- | --------------- | --------------- | ---------------------- |
| Claude Opus 4   | $15 / MTok        | $18.75 / MTok   | $30 / MTok      | $1.50 / MTok           |
| Claude Sonnet 4 | $3 / MTok         | $3.75 / MTok    | $6 / MTok       | $0.30 / MTok           |

## Claude Opus 4
  - the world’s best coding model
  - sustained performance on complex, long-running tasks and agent workflows
  - dramatically outperforms all previous models on memory capabilities
    - long-term task awareness, coherence, and performance
    - skilled at creating and maintaining 'memory files' to store key information
    - example: creating a 'Navigation Guide' while playing Pokémon

## Claude Sonnet 4
  - a significant upgrade to Claude Sonnet 3.7
  - delivers superior coding and reasoning
  - responds more precisely to your instructions

## New model capabilities
  - can use tools in parallel
  - follow instructions more precisely
  - when given access to local files by developers
    - demonstrate significantly improved memory capabilities
    - extract and save key facts to maintain continuity and build tacit knowledge over time

### Extended thinking with tool use (beta)
  - Both models can use tools—like web search—during extended thinking 
  - alternate between reasoning and tool use to improve responses
  - use a smaller model to condense lengthy thought processes
  - thinking_delta for streaming responses 

## Claude Code
  - now generally available
  - supports background tasks via GitHub Actions and native integrations with VS Code and JetBrains
  - displays edits directly in your files for seamless pair programming
  - SDK released: https://docs.anthropic.com/en/docs/claude-code/sdk
  - extensions for VS Code and JetBrains
  - Simply run Claude Code in your IDE terminal to install
  - run /install-github-app from within Claude Code
  - ./.claude 
    - User settings are defined in ~/.claude/settings.json and apply to all projects.
    - Project settings are saved in your project directory under .claude/settings.json for shared settings 
    - .claude/settings.local.json for local project settings 
    - Claude Code will configure git to ignore .claude/settings.local.json when it is created.


## New API capabilities
  - code execution tool
  - MCP connector
  - Files API
  - ability to cache prompts for up to one hour
  - near-instant responses and extended thinking for deeper reasoning

### Code Execution Tool 
  - https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/code-execution-tool

### MCP Connector
  - https://docs.anthropic.com/en/docs/agents-and-tools/mcp-connector
  - Connect to remote MCP servers directly from the Messages API without building an MCP client 
  - seamless integration with MCP-compatible tools and services
  - This feature requires the beta header: "anthropic-beta": "mcp-client-2025-04-04"
  - Direct API integration: Connect to MCP servers without implementing an MCP client
  - Tool calling support: Access MCP tools through the Messages API
  - OAuth authentication: Support for OAuth Bearer tokens for authenticated servers
  - Multiple servers: Connect to multiple MCP servers in a single request

### Files API
  - https://docs.anthropic.com/en/docs/build-with-claude/files
  - particularly useful when using the code execution tool
  - beta feature header: anthropic-beta: files-api-2025-04-14
  - Upload a file to be referenced in future API calls
  - document blocks, image blocks 
  - You can only download files that were created by the code execution tool. Files that you uploaded cannot be downloaded
  - Maximum file size: 32 MB per file
  - Total storage: 100 GB per organization
  - File API operations are free

### Prompt Caching
  - https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
  - caching with the Messages API using a cache_control block
  - Prompt caching references the entire prompt 
    - tools, system, and messages (in that order) 
    - up to and including the block designated with cache_control
  - cache is refreshed for no additional cost each time the cached content is used
  - by default the cache has a 5 minute lifetime 
  - 5-minute cache write tokens are 1.25 times the base input tokens price
  - 1-hour cache write tokens are 2 times the base input tokens price
    - To use the extended cache, add extended-cache-ttl-2025-04-11 as a beta header to your request 
    - include ttl in the cache_control
  - COST 
    - Cache read tokens are 0.1 times the base input tokens price
    - Regular input and output tokens are priced at standard rates
  - Cache prefixes are created in the following order: tools, system, then messages 
  - MINIMUM cacheable prompt length 
    - 1024 tokens for Claude Opus 4, Claude Sonnet 4, Claude Sonnet 3.7, Claude Sonnet 3.5 and Claude Opus 3
    - 2048 tokens for Claude Haiku 3.5 and Claude Haiku 3


