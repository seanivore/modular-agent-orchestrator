# Three Files Created

## 1. Reusable Workflow Commands (save to `.claude/commands/`):
- **`sequential_volley.md`** - One-at-a-time processing (perfect for testing)
- **`parallel_volley.md`** - Multi-agent batches (3-5 agents max)

## 2. CLI-Specific SPEC (save anywhere):
- **`cli_volley_spec.md`** - Hardcoded instructions for using the workflows with your CLI plan

## How You'll Use Them: 

### Testing Single Commands:

```bash
/project:prime
/project:sequential_volley /Users/seanivore/Development/modular-agent-orchestrator/.claude/AGENTIC_CLI_SETUP/cli_volley_spec.md 4
```

### Batch Processing:

```bash
# 3 parallel agents (manageable)
claude > /project:parallel_volley ./path/to/cli_volley_spec.md 4-24 3

# 5 parallel agents (maximum speed)
claude > /project:parallel_volley ./path/to/cli_volley_spec.md 4-24 5
```



----




