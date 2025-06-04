# Documentation Writing & Review Workflow

## Overview
This Single-File Agent (SFA) workflow automates the process of reviewing and improving technical documentation based on feedback. It consists of two phases that help integrate review feedback into existing documentation and perform quality assurance checks on the updated content.

## Workflow Phases

### Phase 1: Initial Documentation Update
- Acts as a senior developer from a top tech company
- Processes review feedback from multiple source documents
- Integrates feedback into existing technical documentation
- Adds notation for missing sections and needed improvements 
- Creates DRAFT_1 versions of all documents

### Phase 2: Quality Assurance Review
- Acts as a technical documentation editor
- Reviews DRAFT_1 documents against original feedback
- Ensures all feedback was properly integrated
- Fixes any missed items or incorrect implementations
- Creates DRAFT_2 versions of all documents

## Input Documents
- Original documentation (6 markdown files)
- Review feedback documents (3 markdown files)
  - Blockchain elements feedback
  - MCP elements feedback
  - Other elements feedback

## Usage
To run the workflow, execute the following command from the terminal:

```bash
sfa run doc-write-best
```

## Expected Outputs
The workflow will generate two sets of updated documentation:

### Draft 1 Files (Phase 1 Output)
- 01_MCP_TRANSPORT_LAYER_DRAFT_1.md
- 02_TOKEN_ECONOMICS_DRAFT_1.md
- 03_USER_INTERACTION_DRAFT_1.md
- 04_COMMUNITY_MANAGEMENT_DRAFT_1.md
- 05_DEVELOPMENT_PHASES_DRAFT_1.md
- 06_INFRASTRUCTURE_REQUIREMENTS_DRAFT_1.md

### Draft 2 Files (Phase 2 Output)
- 01_MCP_TRANSPORT_LAYER_DRAFT_2.md
- 02_TOKEN_ECONOMICS_DRAFT_2.md
- 03_USER_INTERACTION_DRAFT_2.md
- 04_COMMUNITY_MANAGEMENT_DRAFT_2.md
- 05_DEVELOPMENT_PHASES_DRAFT_2.md
- 06_INFRASTRUCTURE_REQUIREMENTS_DRAFT_2.md

All output files will be saved in the `/docs/03-new-drafts/` directory with appropriate notations and improvements based on the provided feedback.