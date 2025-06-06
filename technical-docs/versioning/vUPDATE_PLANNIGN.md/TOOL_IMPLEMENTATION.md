# Tool Implementation Update 

## **TOOL** Markdown to PDF Export 

- We made this MCP; our third 
- Attempted to recreate VS Code preview typography styles document we found 
- Converting it to python styles lost most of any impressing factor
- Let's make it simple, clean, functional 
- As a tool first
- Maybe update the MCP after 

Project Directory: `/Users/seanivore/Development/md-pdf-mcp` 

## **TOOL** Anthropic API MCP Connector 

*This feature requires the `anthropic-beta`: `mcp-client-2025-04-04` beta header*

- Connect MCP servers directory 
- Uses messages API 
- No separate client 

Documentation: `https://docs.anthropic.com/en/docs/agents-and-tools/mcp-connector`

### Other Key Features 

  - **Direct API integration**: Connect to MCP servers without implementing an MCP client
  - **Tool calling support**: Access MCP tools through the Messages API
  - **OAuth authentication**: Support for OAuth Bearer tokens for authenticated servers
  - **Multiple servers**: Connect to multiple MCP servers in a single request

### Specifics 

  - Of MCP specifications, only tool calls supported for now 
  - Publicly exposed server through HTTP 
    - Supports Streamable HTTP and SSE transports 
    - Local STDIO servers cannot be connected directly.

### Messages API Connect Remote MCP Server Via `mcp_servers parameter`

```python
response = anthropic.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=[{
        "role": "user",
        "content": "What tools do you have available?"
    }],
    mcp_servers=[{
        "type": "url",
        "url": "https://mcp.example.com/sse",
        "name": "example-mcp",
        "authorization_token": "YOUR_TOKEN"
    }],
    betas=["mcp-client-2025-04-04"]
)
```

### Configuration `mcp_servers` Array Servers Support 

```python 
{
  "type": "url",
  "url": "https://example-server.modelcontextprotocol.io/sse",
  "name": "example-mcp",
  "tool_configuration": {
    "enabled": true,
    "allowed_tools": ["example_tool_1", "example_tool_2"]
  },
  "authorization_token": "YOUR_TOKEN"
}
```

#### Field Descriptions 

| Property                           | Type    | Required | Description                                      |
| ---------------------------------- | ------- | -------- | ------------------------------------------------ |
| `type`                             | string  | Yes      | Only 'url' supported                             |
| `url`                              | string  | Yes      | https:// MCP server URL                          |
| `name`                             | string  | Yes      | Unique identifier used in `mcp_tool_call` blocks |
| `tool_configuration`               | object  | No       | Configure tool usage                             |
| `tool_configuration.enabled`       | boolean | No       | Turn server tools on and off; default is true    |
| `tool_configuration.allowed_tools` | array   | No       | List allowed tools; default none restricted      |
| `authorization_token`              | string  | No       | MCP server OAuth authorization token             |

### Two Block Tool Use Response 
​
  1. Use Block

```python
{
  "type": "mcp_tool_use",
  "id": "mcptoolu_014Q35RayjACSWkSj4X2yov1",
  "name": "echo",
  "server_name": "example-mcp",
  "input": { "param1": "value1", "param2": "value2" }
}
```
  2. Result Block

```python
{
  "type": "mcp_tool_result",
  "tool_use_id": "mcptoolu_014Q35RayjACSWkSj4X2yov1",
  "is_error": false,
  "content": [
    {
      "type": "text",
      "text": "Hello"
    }
  ]
}
```
### Multiple Servers In `mcp_servers` Array 

```python 
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1000,
  "messages": [
    {
      "role": "user",
      "content": "Use tools from both mcp-server-1 and mcp-server-2 to complete this task"
    }
  ],
  "mcp_servers": [
    {
      "type": "url",
      "url": "https://mcp.example1.com/sse",
      "name": "mcp-server-1",
      "authorization_token": "TOKEN1"
    },
    {
      "type": "url",
      "url": "https://mcp.example2.com/sse",
      "name": "mcp-server-2",
      "authorization_token": "TOKEN2"
    }
  ]
}
```

### Authentication & Token Testing Details at Document: `https://docs.anthropic.com/en/docs/agents-and-tools/mcp-connector`





