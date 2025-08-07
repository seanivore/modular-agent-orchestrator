# v4.2.0 Must Update Items 

## MCP Servers

### Turn the MCP Server Config Into a Directory 

- Our only current inclusion is the `memory` MCP server. 
- `./configs/connections/mcp_servers.json` 
- But we definitely want this to be a directory, so that each MCP server is on it's own JSON file. 
- We'll need to update the code to support this. 

### Ensure the MCP Server Config Is Defined For Using STDIO (and HTTP)

- We're currently using the `memory` MCP server, which is a subprocess. 
- We need to update the code to use STDIO, so that we can use the `memory` MCP server. 
- We'll need to update the code to support this. 
