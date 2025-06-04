# Voice Cheat Sheet - Single-File Agent Workflow

## Overview
This workflow automates the creation of a comprehensive voice marketing cheat sheet for telemarketers using AI voice tools (specifically Bland AI). It processes source documentation through multiple phases of refinement to produce a polished, ready-to-use reference guide.

## Workflow Phases

### 1. Initial Draft Creation
- **Agent Role**: Voice Marketing Specialist
- **Purpose**: Combines separate documents on voice modulation techniques and pro tips into a unified cheat sheet
- **Input**: Two source documents (bland-ai-pro-tips.md, bland-ai-voice-modulation.md)
- **Output**: Initial draft cheat sheet (CHEAT_SHEET_DRAFT_1.md)

### 2. Quality Assurance Review
- **Agent Role**: QA Specialist
- **Purpose**: Thoroughly reviews the draft for completeness, clarity, organization, and technical accuracy
- **Input**: Draft cheat sheet and original source documents
- **Output**: Detailed feedback document (CHEAT_SHEET_FEEDBACK.md)

### 3. Final Production
- **Agent Role**: Head of Voice Marketing Training
- **Purpose**: Creates polished final version incorporating all QA feedback
- **Input**: Draft cheat sheet and QA feedback
- **Output**: Final production-ready cheat sheet (CHEAT_SHEET.md)

## Usage

Run the workflow using the following command:
```bash
python sfa_agent.py voice-cheat-sheet.sh
```

## Expected Outputs

The workflow will generate the following files in your specified directories:

1. `/SFA-RESEARCH-REVIEW/bland-ai-docs/01-combine/CHEAT_SHEET_DRAFT_1.md`
   - Initial combined draft of the cheat sheet

2. `/SFA-RESEARCH-REVIEW/bland-ai-docs/02-review/CHEAT_SHEET_FEEDBACK.md`
   - Detailed QA feedback and recommendations

3. `/findings/core/CHEAT_SHEET.md`
   - Final, production-ready voice marketing cheat sheet

## Requirements

- Python environment with Single-File Agent framework installed
- Source documents must be present in the specified input paths
- Write permissions for all output directories