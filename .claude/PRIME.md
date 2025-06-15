# MAO (Modular Agent Orchestrator) Product Development 
*MAO v4.0.0, fka. 'SFA'*

## Context Priming 

Important files will be specifically added here for context priming after the next session. We're cleaning up documentation next. For now you can find all the entire project directory tree below should you want to better explore things. 

### Project State Updates to `memory` MCP Server 

Search for entity --> `mao`, `mao-v4`, or for the earliest updates of the few weeks we've been refactoring, entity `sfa-v4-refactor`, to see the big picture. 

**UPDATE PROJECT STATE TO MEMORY MCP AT THESE TIMES:**
  
  1. When we start a session and have decided what we're doing to work on first, post the plan to Memory MCP 
  2. During the work on those tasks, if something changes or unexpected comes up, post it to the Memory MCP 
  3. After completion of the batch of tasks, post an update and include what the next steps are 

### Sequential Thinking MCP 

  - Don't forget about this tool 
  - Use it often 

Anthropic tested it on their flight reservation task booking model and the results were insane like off the charts improvement, especially when using tools to gather info which is always. 

  - Most responses 
  - If you have to find something in context 
  - While you are using other tools, between tools
  - Jump to thinking, writing, thinking, searing web, thinking, writing, etc. 

## About SFAv4 --> MAOv4

Our 'Single-File Agent' has transformed.

  - We've gone all-in strict on the modular plug-and-play variables for tools, models, providers 
  - We've gone all in on being agentic with Claude Sonnet 4 as our Orchestrator delegating to Agents 
    - Most workflows will not have a planned end; MAO will assess and build the finalized plan as it progresses based on actual needs 
    - Agents call MAO when they're done a task and meet MAO directly; this eliminated all 'logistical' tools 
  - Setting up a new use-case workflow is as simple as chatting with Claude MAO 
  - Claude 4's 'Code Execution' tool creates 'button snippets' for agent tools, mean in more translating SDKs 
  - We're at about 60 modular files, and the magic is that the complexity has made the UX simpler 
  - The whole thing should use about 1% as many tokens --> Pure magic ✨