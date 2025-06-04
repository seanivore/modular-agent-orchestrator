# Research Combine Report - Single-File Agent Workflow

## Overview
This workflow orchestrates a comprehensive process for synthesizing voice marketing research and developing detailed caller personas. It transforms multiple marketing strategy documents into a unified framework and creates implementation-ready caller archetypes through a series of specialized agent interactions.

## Workflow Phases

### 1. Strategy Synthesis
- Combines five voice marketing strategy documents into a unified tactical framework
- Creates foundation for persona development
- Maintains key insights while organizing tactics logically
- Output: `VOICE_MKT_TACTICS.md`

### 2. Initial Persona Development
- Analyzes unified strategy to recommend 3-5 distinct caller archetypes
- Creates preliminary persona profiles with core traits and strategies
- Aligns personas with marketing strategies
- Output: `VOICE_MKT_PERSONAS_DRAFT_1.md`

### 3. Detailed Persona Creation
- Transforms preliminary concepts into comprehensive persona profiles
- Develops detailed voice signatures and tactical implementations
- Includes specific phrases, objection handling, and targeting recommendations
- Output: `VOICE_MKT_PERSONAS_DRAFT_2.md`

### 4. Quality Review
- Conducts thorough review of persona profiles
- Ensures strategic alignment and psychological consistency
- Provides detailed feedback and recommendations
- Output: `VOICE_MKT_PERSONAS_FEEDBACK.md`

### 5. Final Persona Refinement
- Integrates all feedback into final, implementation-ready profiles
- Polishes and standardizes persona documentation
- Creates executive summary and usage guidance
- Output: `VOICE_MKT_PERSONAS.md`

## Usage

To run the workflow, execute:

```bash
./research-combine-report.sh
```

## Expected Outputs

The workflow generates a series of documents in a progressive refinement process:

1. `/findings/core/VOICE_MKT_TACTICS.md`
   - Unified voice marketing strategy framework

2. `/SFA-RESEARCH-REVIEW/variable-docs-combine/02-recommend/VOICE_MKT_PERSONAS_DRAFT_1.md`
   - Initial persona development creative brief

3. `/SFA-RESEARCH-REVIEW/variable-docs-combine/03-personas/VOICE_MKT_PERSONAS_DRAFT_2.md`
   - Detailed persona profiles

4. `/SFA-RESEARCH-REVIEW/variable-docs-combine/04-accuracy/VOICE_MKT_PERSONAS_FEEDBACK.md`
   - Comprehensive review and feedback

5. `/findings/core/VOICE_MKT_PERSONAS.md`
   - Final, implementation-ready persona profiles

Each output builds upon the previous document, culminating in a polished, deployment-ready set of voice marketing personas and strategies.