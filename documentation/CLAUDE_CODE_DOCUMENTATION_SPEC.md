# Claude Code SPEC: Mao Documentation Gathering Project
> Use the documentation batch grouping files to systematically gather information from the codebase and create technical documentation.

## High-Level Objective

Create comprehensive technical documentation for the Mao v4 modular agent orchestrator using the predefined batch grouping files as questionnaires.

## Mid-Level Objective

- Read each batch grouping file in `/documentation/FILE_BATCH_DEFINITIONS/`
- Answer the questions for each file listed in the batch
- Save the gathered information as organized documentation
- Focus on LOCAL terminal application architecture (read `/ARCHITECTURE_PRINCIPLES.md` first)

## Implementation Notes

- **CRITICAL**: Mao is a LOCAL ONLY terminal application like Claude Code - read `/ARCHITECTURE_PRINCIPLES.md` first
- This is documentation gathering, NOT code modification
- Each batch file contains specific questions to answer about the listed files
- Save documentation in `/documentation/GATHERED_INFO/` directory

## Context

### Beginning context
- 6 batch grouping files exist in `/documentation/FILE_BATCH_DEFINITIONS/`
- Complete Mao v4 codebase ready for documentation
- Architecture principles document emphasizing LOCAL application

### Ending context  
- Comprehensive technical documentation saved in organized files
- All batch grouping questions answered with real codebase information

## Tasks

### **Phase 1: Foundation (Sequential)**

**Task 1: Read Architecture Principles**
- Read `/ARCHITECTURE_PRINCIPLES.md` 
- Understand LOCAL terminal application concept
- Save: No output needed, just understanding

**Task 2: Core System Architecture**
- Use `/documentation/FILE_BATCH_DEFINITIONS/CORE_SYSTEM_ARCHITECTURE.md` as questionnaire
- Answer questions for all files listed in the batch (28 files total)
- Save: `/documentation/GATHERED_INFO/01_CORE_SYSTEM_ARCHITECTURE.md`

### **Phase 2: Modules (Parallel)**

**Task 3: Tools Ecosystem** 
- Use `/documentation/FILE_BATCH_DEFINITIONS/TOOLS_ECOSYSTEM.md` as questionnaire
- Answer questions for all files listed in the batch (45 files total)
- Save: `/documentation/GATHERED_INFO/02_TOOLS_ECOSYSTEM.md`

**Task 4: CLI Command System**
- Use `/documentation/FILE_BATCH_DEFINITIONS/CLI_COMMAND_SYSTEM.md` as questionnaire  
- Answer questions for all files listed in the batch (96 files total)
- Save: `/documentation/GATHERED_INFO/03_CLI_COMMAND_SYSTEM.md`

**Task 5: Configuration Management**
- Use `/documentation/FILE_BATCH_DEFINITIONS/CONFIGURATION_MANAGEMENT.md` as questionnaire
- Answer questions for all files listed in the batch (37 files total)
- Save: `/documentation/GATHERED_INFO/04_CONFIGURATION_MANAGEMENT.md`

**Task 6: Templates and Scripts**
- Use `/documentation/FILE_BATCH_DEFINITIONS/TEMPLATES_AND_SCRIPTS.md` as questionnaire
- Answer questions for all files listed in the batch (31 files total)
- Save: `/documentation/GATHERED_INFO/05_TEMPLATES_AND_SCRIPTS.md`

### **Phase 3: Integration (Sequential)**

**Task 7: UI Integration Requirements**
- Use `/documentation/FILE_BATCH_DEFINITIONS/UI_TYPESCRIPT_INTEGRATION.md` as questionnaire
- Focus on LOCAL subprocess communication patterns
- Save: `/documentation/GATHERED_INFO/06_UI_INTEGRATION.md`

**Task 8: Create Final Documentation**
- Consolidate all gathered information into organized technical documentation
- Save: `/documentation/GATHERED_INFO/00_COMPLETE_DOCUMENTATION.md`
