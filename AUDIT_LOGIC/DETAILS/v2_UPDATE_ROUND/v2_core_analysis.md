# core.py Analysis - Main Orchestrator Brain

## MAO_FLOW.md Intended Functionality
- Transform natural language goals into intelligent workflows
- Trust AI intelligence completely - no hardcoded suggestions
- Support multilingual goals and cultural contexts
- Let AI design optimal workflow phases dynamically
- No predetermined patterns - emergent workflow design

## Current Implementation Analysis

### ✅ Excellent Principles Implemented
- **Dynamic Goal Analysis**: `_analyze_goal()` avoids English keyword detection
- **AI-Driven Phase Design**: `_design_workflow_phases()` trusts AI to create structure
- **Clean Model Selection**: Uses dynamic analysis rather than hardcoded categories
- **No Hardcoded Workflow Patterns**: Removed from protocol config (line 135)
- **Multilingual Support**: Goal analysis works with any language
- **Intelligent Caching**: Sophisticated caching with content fingerprinting

### ❌ Issues Found

#### 1. **Hardcoded Task Multipliers for Cost Estimation**
```python
# Lines 378-384
task_multiplier = {
    "research": 3.0,  # Lots of web search results
    "reasoning": 2.0,  # Detailed analysis
    "creative": 2.5,  # Rich content creation
    "coding": 3.0,    # Code + documentation
    "vision": 1.5     # Image analysis
}
```
- **Problem**: English keyword-based cost estimation
- **Violation**: Hardcoded categories that break multilingual support
- **Impact**: Inaccurate cost estimates for non-English workflows

#### 2. **English Word Filtering in Name Generation**
```python
# Lines 410-411
key_words = [w for w in words if len(w) > 3 and w not in ["and", "the", "for", "with", "that", "this"]]
```
- **Problem**: Hardcoded English stop words
- **Impact**: Poor workflow naming for non-English goals
- **Cultural Issue**: Assumes English language structure

#### 3. **Predetermined Phase Structure Logic**
```python
# Lines 274-286
if complexity == "high" and len(phases) == 1:
    # For complex goals, suggest AI might want to break into planning + execution phases
    phases.insert(0, WorkflowPhase(
        name="planning_analysis",
        # ...
    ))
```
- **Problem**: Forces predetermined "planning + execution" pattern
- **Violation**: Should trust AI to determine optimal phase structure

## Required Changes

### 1. Remove Hardcoded Task Multipliers
- Replace with dynamic analysis based on actual requirements
- Use model capabilities and tool costs for estimation
- Remove English keyword dependencies

### 2. Fix Multilingual Name Generation
- Remove English stop word filtering
- Use language-neutral approach to workflow naming
- Support Unicode and international characters properly

### 3. Trust AI for Phase Design
- Remove predetermined phase insertion logic
- Let AI determine optimal workflow structure completely
- Support emergent patterns that don't fit Western business models

### 4. Improve Dynamic Cost Estimation
- Base costs on actual tool requirements and model selection
- Use real provider pricing data
- Remove task-type assumptions

## Compliance with MAO_FLOW.md
- **Trust AI Intelligence**: ✅ Mostly excellent, minor violations in cost estimation
- **No Hardcoded Categories**: ❌ Task multipliers violate this principle  
- **Multilingual Support**: ❌ English stop words and keywords break this
- **Dynamic Workflow Design**: ⚠️ Good overall, but forces some patterns
- **Cultural Neutrality**: ❌ Western business assumptions in phase logic

## Audit Verdict
**Status**: Needs targeted fixes
**Priority**: Medium-High  
**Core Logic**: Excellent foundation with minor violations
**Main Issues**: Cost estimation and naming need multilingual cleanup
**Strengths**: Excellent caching, dynamic tool integration, AI-first approach