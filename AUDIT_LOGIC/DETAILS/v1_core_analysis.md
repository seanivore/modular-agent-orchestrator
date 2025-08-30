# Core.py Analysis - Critical Violations Found

## File Purpose According to MAO_FLOW.md
Core.py should be the main orchestration brain that converts natural language goals into intelligent workflows by trusting AI intelligence completely, without hardcoded constraints or predetermined categories.

## Major Violations Identified

### 1. **CRITICAL VIOLATION: Hardcoded Workflow Patterns (Lines 135-140)**
```python
"workflow_patterns": {
    "research_then_create": ["research", "reasoning", "creative"],
    "analyze_and_recommend": ["research", "reasoning"],
    "multimedia_project": ["research", "creative", "vision"]
}
```
**Violation Type**: Predetermined English workflow categories
**Impact**: Forces Western linear thinking patterns on all users, violates multilingual design
**MAO_FLOW.md Quote**: "NO HARDCODED 'SUGGESTIONS' OR GUIDES ALLOWED"

### 2. **CRITICAL VIOLATION: English Task Type Detection (Lines 233-275)**
```python
if any(word in goal_lower for word in ["research", "analyze", "study", "investigate", "find", "look up"]):
    analysis["task_types"].append("research")

if any(word in goal_lower for word in ["create", "write", "design", "draft", "compose", "generate"]):
    analysis["task_types"].append("creative")
```
**Violation Type**: English keyword assumptions for workflow generation
**Impact**: Completely breaks multilingual functionality, forces English business concepts
**MAO_FLOW.md Quote**: "Trust AI intelligence completely - modern AI doesn't need constraints"

### 3. **CRITICAL VIOLATION: Hardcoded Workflow Phase Generation (Lines 309-393)**
```python
# Research-driven workflows
if "research" in task_types:
    phases.append(WorkflowPhase(
        name="research_phase",
        model="",
        agent_role=self._get_agent_role("research", analysis["domain"]),
        task_instructions=self._get_task_instructions("research", analysis),
        input_sources=[],
        output_files=["research_findings.md", "key_data.json"]
    ))

# Analysis / reasoning phase
if "reasoning" in task_types:
    # ... more hardcoded phase logic
```
**Violation Type**: Predetermined workflow structure based on English categories
**Impact**: Prevents AI from designing optimal workflows for different cultural approaches
**MAO_FLOW.md Quote**: "Everything should be dynamic and discoverable via directory scanning"

### 4. **CRITICAL VIOLATION: Hardcoded Agent Roles (Lines 427-454)**
```python
roles = {
    "research": {
        "business": "Business intelligence analyst with expertise in market research and competitive analysis",
        "technology": "Technology research specialist with deep knowledge of AI and software trends",
        "creative": "Creative industry research expert with understanding of design and brand trends",
        "general": "Professional research analyst with broad domain expertise"
    },
    "reasoning": {
        "business": "Strategic business consultant with expertise in data-driven decision making",
        # ... more hardcoded Western business roles
    }
}
```
**Violation Type**: English business assumptions for agent personalities
**Impact**: Cultural imperialism - assumes all users think in Western business paradigms
**MAO_FLOW.md Quote**: "Multilingual-first design - remove English-specific assumptions"

### 5. **CRITICAL VIOLATION: Hardcoded Task Instructions (Lines 459-477)**
```python
base_instructions = {
    "research": "Conduct comprehensive research using web search and analysis tools. Gather current, relevant information and organize findings clearly.",
    "reasoning": "Analyze the provided information critically. Identify patterns, draw insights, and develop strategic recommendations based on evidence.",
    "creative": "Create compelling, high-quality content that meets the specified requirements. Focus on clarity, engagement, and achieving the stated goals.",
    # ... more predetermined instructions
}
```
**Violation Type**: Predetermined AI behavior guidance with examples
**Impact**: Constrains AI capabilities, violates "describe what Mao is to do" principle
**MAO_FLOW.md Quote**: "DO NOT LET THAT TEMPT YOU INTO CREATING EXAMPLES, or suggestions in the codebase"

## Required Changes

### 1. **Remove All Hardcoded Workflow Patterns**
- Delete lines 135-140 (workflow_patterns)
- Replace with dynamic analysis that trusts AI intelligence

### 2. **Replace English Task Detection with Dynamic Analysis**
- Delete lines 233-275 (task type detection)
- Allow Claude to analyze goals in user's language and cultural context
- Remove predetermined categories entirely

### 3. **Replace Hardcoded Phase Generation with AI-Driven Design**
- Delete lines 309-393 (hardcoded phase logic)
- Let Claude design optimal workflow phases based on actual goal requirements
- Support emergent workflow patterns that don't fit English business categories

### 4. **Remove Hardcoded Agent Roles**
- Delete lines 427-454 (roles dictionary)
- Let Claude generate appropriate agent descriptions based on actual task context
- Remove Western business assumptions

### 5. **Replace Hardcoded Instructions with Dynamic Guidance**
- Delete lines 459-477 (base_instructions dictionary)
- Provide behavioral guidance as code comments, not predetermined examples
- Trust Claude to generate appropriate task instructions

## Correct Implementation Approach

The correct approach is to:
1. **Trust Claude's Intelligence**: Let Claude analyze goals and design workflows without constraints
2. **Dynamic Goal Analysis**: Analyze user goals in their language and cultural context
3. **Emergent Workflow Patterns**: Allow workflow patterns to emerge from user needs
4. **Cultural Adaptation**: Support different cultural problem-solving approaches
5. **True Modularity**: Tools describe capabilities, not workflow positions

## Compliance Assessment

**Current Compliance**: ❌ **CRITICAL VIOLATIONS** - Complete reconstruction required
**Impact on Multilingual Users**: 🚫 **COMPLETELY BROKEN** - System unusable for non-English users
**AI Intelligence Utilization**: 🚫 **SEVERELY CONSTRAINED** - Hardcoded logic prevents optimal AI behavior

This file represents exactly the kind of "cultural imperialism disguised as features" that MAO_FLOW.md warns against and must be completely restructured to trust AI intelligence and support true multilingual functionality.