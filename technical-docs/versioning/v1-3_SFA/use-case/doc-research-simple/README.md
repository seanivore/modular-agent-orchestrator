# Document Research Simple Workflow

## Overview
This Single-File Agent workflow automates the process of reviewing, synthesizing, and refining research documents for voice marketing strategies. It transforms complex research documents into clear, actionable summaries through a three-phase review process involving different specialist roles.

## Workflow Phases

### Phase 1: Initial Research Synthesis
- Role: Research Synthesis Specialist
- Takes raw research documents and creates initial draft summaries
- Maintains key insights while improving organization and clarity
- Connects findings to emotional triggers
- Output: Draft documents with `_DRAFT_1` suffix

### Phase 2: Quality Review
- Role: Senior Research Reviewer
- Reviews draft summaries against original documents
- Ensures accuracy and evaluates structural improvements
- Provides structured feedback with specific recommendations
- Output: Feedback documents with `_FEEDBACK` suffix

### Phase 3: Final Refinement
- Role: Voice Research Director
- Integrates feedback to create polished final documents
- Ensures consistent formatting with executive summaries
- Adds implementation guidelines and tactical recommendations
- Output: Finalized documents in the findings directory

## Usage

Run the workflow using:
```bash
./doc-research-simple.sh
```

## Expected Outputs

The workflow processes documents through three directories:

1. `/01-draft-1/`: Initial synthesized drafts
   - Example: `curiosity-gap_DRAFT_1.md`

2. `/02-feedback/`: Review feedback documents
   - Example: `curiosity-gap_FEEDBACK.md`

3. `/findings/strategy/`: Final polished documents
   - Example: `curiosity-gap.md`

Each research document goes through all three phases, maintaining consistency in formatting and quality while improving clarity and actionability of the content.

## Document Types Processed
- Curiosity Gap Research
- Empathy Objection Studies
- Strategy Combination Analysis
- Strongest Variables Research

Each document is processed independently through the workflow while maintaining consistent formatting and quality standards across all outputs.

---
Note: Ensure all input documents are placed in the correct source directories before running the workflow.