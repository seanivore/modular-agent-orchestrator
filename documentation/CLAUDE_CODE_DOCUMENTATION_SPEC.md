# Claude Code SPEC: Mao Documentation Gathering Project
> Use the documentation batch grouping files to systematically gather information from the codebase and create technical documentation.

## High-Level Objective

Create comprehensive technical documentation for the Mao v4 modular agent orchestrator using the predefined batch grouping files as questionnaires.

## Mid-Level Objective

- Read each batch grouping file in `./documentation/FILE_BATCH_DEFINITIONS/...`
- Answer the questions for each file listed in the batch
- Save the gathered information as organized documentation
- Focus on LOCAL terminal application architecture; read `/ARCHITECTURE_PRINCIPLES.md` first

## Implementation Notes

- **CRITICAL**: Mao is a LOCAL ONLY terminal application like Claude Code; read `/ARCHITECTURE_PRINCIPLES.md` first
- This is documentation gathering, NOT code modification 
- Only on limited files will you be asked to provide code that is not already in the codebase; e.g. 'UI interface patterns'
- Each batch file contains specific questions to answer about the listed files
- For each file, please copy the questionaire and insert your responses below each question or prompt 
- Save documentation in `/documentation/GATHERED_INFO/...` directory
- Each file should have its own copy of the questionaire 
- Name the file as as the batch number followed by the name of the file without its extension 
- E.g. 'CORE_SYSTEM_ARCHITECTURE_BATCH_01_FILE_NAME.md'; do this for every file in every batch 

## Context

### Beginning context
- 6 batch grouping files exist in `/documentation/FILE_BATCH_DEFINITIONS/...`
- Complete, audited, Mao v4 codebase ready for documentation
- Architecture principles document emphasizing LOCAL application

### Ending context 
- Comprehensive technical documentation saved in organized files
- All batch grouping questions answered with real codebase information
- When pulling code, only pull from codebase files; old, outdated implementation files exist  

## Tasks

### **Phase 1: Foundation (Sequential)**

**Task 1: Read Architecture Principles**
- Read `/ARCHITECTURE_PRINCIPLES.md` 
- Understand LOCAL terminal application concept
- Save: No output needed, just understanding

**Task 2: Core System Architecture** (25 files)
- Use `./documentation/FILE_BATCH_DEFINITIONS/CORE_SYSTEM_ARCHITECTURE.md` as questionnaire
- Answer questions for all files listed in the batches
  - Batch 01: Root Files (1 file)
  - Batch 02: Interfaces (1 file)
  - Batch 03: Orchestrator Core (12 files)
  - Batch 04: Orchestrator Managers (9 files)
  - Batch 05: Cache System (2 files) 
- Save: `/documentation/GATHERED_INFO/CORE_SYSTEM_ARCHITECTURE_BATCH_01_FILE_NAME.md`
  - 25 total deliverables for 'Task 2, Batches 1-5'

### **Phase 2: Modules (Parallel)**

**Task 3: Tools Ecosystem** (45 files)
- Use `/documentation/FILE_BATCH_DEFINITIONS/TOOLS_ECOSYSTEM.md` as questionnaire
- Answer questions for all files listed in the batch 
  - Batch 06: Search Tools (8 files)
  - Batch 07: Web Search Tools (4 files)
  - Batch 08: Content Creation Tools (8 files)
  - Batch 09: Development Tools (12 files)
  - Batch 10: System Tools (13 files)
- Save: `/documentation/GATHERED_INFO/TOOLS_ECOSYSTEM_BATCH_06_FILE_NAME.md`
  - 45 total deliverables for 'Task 3, Batches 6-10'

**Task 4: CLI Command System** (94 files)
- Use `/documentation/FILE_BATCH_DEFINITIONS/CLI_COMMAND_SYSTEM.md` as questionnaire  
- Answer questions for all files listed in the batch 
  - Batch 11: CLI Commands Group 1 (12 files)
  - Batch 12: CLI Commands Group 2 (12 files)
  - Batch 13: CLI Commands Group 3 (12 files)
  - Batch 14: CLI Commands Group 4 (12 files)
  - Batch 15: CLI Commands Group 5 (12 files)
  - Batch 16: CLI Commands Group 6 (12 files)
  - Batch 17: CLI Commands Group 7 (12 files)
  - Batch 18: CLI Commands Group 8 - JSON Only (10 files)
- Save: `/documentation/GATHERED_INFO/CLI_COMMAND_SYSTEM_BATCH_11_FILE_NAME.md`
  - 94 total deliverables for 'Task 4, Batches 11-18'

**Task 5: Configuration Management** (37 files)
- Use `/documentation/FILE_BATCH_DEFINITIONS/CONFIGURATION_MANAGEMENT.md` as questionnaire
- Answer questions for all files listed in the batch 
  - Batch 19: Models & Providers Configuration (13 files)
  - Batch 20: Settings & System Configuration (14 files)
  - Batch 21: User & Workflow Configuration (10 files)
- Save: `/documentation/GATHERED_INFO/CONFIGURATION_MANAGEMENT_BATCH_19_FILE_NAME.md`
  - 37 total deliverables for 'Task 5, Batches 19-21'

**Task 6: Templates and Scripts** (31 files)
- Use `/documentation/FILE_BATCH_DEFINITIONS/TEMPLATES_AND_SCRIPTS.md` as questionnaire
- Answer questions for all files listed in the batch 
  - Batch 22: Templates System (13 files)
  - Batch 23: Utility Scripts (14 files)
  - Batch 24: Workflow & GitHub Scripts (4 files)
- Save: `/documentation/GATHERED_INFO/TEMPLATES_AND_SCRIPTS_BATCH_22_FILE_NAME.md`
  - 31 total deliverables for 'Task 6, Batches 22-24'

### **Phase 3: Integration (Sequential)**

**Task 7: UI Integration Requirements** (41 files)
- Use `/documentation/FILE_BATCH_DEFINITIONS/UI_TYPESCRIPT_INTEGRATION.md` as questionnaire
- Focus on LOCAL subprocess communication patterns
  - Pythong terminal interface `./interfaces/ui_terminal.py` (1 file)
  - CLI `ui_*.py` files (29 files)
  - Tools `ui_*.py` files (11 files)
- Save: `/documentation/GATHERED_INFO/UI_TYPESCRIPT_INTEGRATION_FILE_NAME.md`
  - 41 total deliverables for 'Task 7'

### Phase 4: Finalization 

**NOTE: Task 8 Proposed**
*added by Sean at 0750 on 19 July 2025 while waiting for our rate limit to reset at 1100* 

```plaintext
I think we need to add a "Task 8" -- AI had originally written "Create final documentation" as a task 8 which I removed because it sounded a bit lofty a request for what we were doing. However the main intention of doing this is because we created a very narrative-heavy overview of the product and we want to create "Architecture" sections showing the code snippets, patterns, I.e. the type of stuff that is expected in standard technical documentation. We're just trying to create more of a vibe like... Anthropic's documentation for example, where each section is 60-80% written content with maybe 10-20% of that being bullet points. Then the remaining 40-20% of each section is the code. It really helps make things a lot more entry level. 

Anyway I removed task 8 because I thought that the questionnaires were implying that we highlights of each file's code be included in the "Code & Explanation" 

However, this is probably better to happen this route anyway, because we certainly don't need snippets of code for 8 tools and ~40 CLI commands, settings, etc. We only really need code snippets as examples for each section. If we do that then we can't really provide too much, it'll all be helpful. 

Wdyt? Can we add this as the final step? 
```