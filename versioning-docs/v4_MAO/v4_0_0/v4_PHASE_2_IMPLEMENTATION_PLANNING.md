# Phase 2 Implementation Planning
**Complete specifications for Use-Case JSON, UI improvements, and setup flow**

*Plan it now, execute it cleanly later*

## What's Planned Out

✅ Complete Use-Case JSON Schema - All variable types, preferences, command patterns
✅ Enhanced UI/Terminal Displays - Progress bars, cost monitoring, error recovery
✅ Setup Conversation Flow - Goal analysis, variable collection, command generation
✅ Workspace Organization - Directory structure, README generation, metadata tracking
✅ Command Installation System - Executable script generation, argument parsing
✅ Quality Assurance Framework - Success criteria validation, automatic improvements

## Key Strategic Decisions Made

- Variable-Input Philosophy Maintained - No hardcoded categories in JSON configs
- Flexible Command Patterns - Support both direct args and interactive modes
- Intelligent Cost Monitoring - Real-time budget tracking with optimization suggestions
- Automatic Quality Validation - Success criteria with fallback improvement strategies
- Professional Workspace Organization - Clean deliverables with metadata tracking

---

## 🎯 USE-CASE JSON STRUCTURE

### Complete Use-Case Configuration Schema

```json
{
  "meta": {
    "id": "content_strategy_startup",
    "name": "Content Strategy for Startup",
    "description": "Comprehensive content strategy development for early-stage startups",
    "version": "1.0.0",
    "created": "2025-06-14T15:30:00Z",
    "created_by": "mao_setup_conversation",
    "tags": ["content", "strategy", "startup", "marketing"]
  },
  
  "workflow": {
    "pattern": "research_analysis_strategy_content",
    "phases": [
      {
        "name": "market_research",
        "agent_role": "Market Research Specialist",
        "tools": ["brave_search", "perplexity_search"],
        "model_preference": "cost_optimized",
        "estimated_duration": "8-12 minutes",
        "estimated_cost": "$0.08-0.15"
      },
      {
        "name": "content_analysis", 
        "agent_role": "Content Strategy Analyst",
        "tools": ["think", "text_editor"],
        "model_preference": "balanced",
        "estimated_duration": "6-10 minutes", 
        "estimated_cost": "$0.05-0.12"
      },
      {
        "name": "strategy_development",
        "agent_role": "Strategic Content Planner", 
        "tools": ["think", "text_editor", "graphic_design"],
        "model_preference": "premium",
        "estimated_duration": "10-15 minutes",
        "estimated_cost": "$0.12-0.20"
      },
      {
        "name": "content_creation",
        "agent_role": "Content Creator",
        "tools": ["text_editor", "graphic_design", "dalle_generate"],
        "model_preference": "creative",
        "estimated_duration": "12-18 minutes",
        "estimated_cost": "$0.15-0.25"
      }
    ]
  },
  
  "variables": {
    "required": {
      "business_description": {
        "type": "string",
        "description": "Brief description of the startup/business",
        "prompt": "Describe your startup in 2-3 sentences:",
        "example": "B2B SaaS platform for project management targeting remote teams"
      },
      "target_audience": {
        "type": "string", 
        "description": "Primary target audience",
        "prompt": "Who is your primary target audience?",
        "example": "Remote team managers at 50-500 person companies"
      },
      "content_goals": {
        "type": "string",
        "description": "What you want to achieve with content",
        "prompt": "What are your main content goals?",
        "example": "Build thought leadership, generate leads, educate prospects"
      }
    },
    
    "optional": {
      "budget_range": {
        "type": "string",
        "default": "flexible",
        "description": "Monthly content budget range",
        "prompt": "What's your monthly content budget? (optional)",
        "options": ["under_1k", "1k_5k", "5k_15k", "15k_plus", "flexible"]
      },
      "timeline": {
        "type": "string", 
        "default": "3_months",
        "description": "Content strategy timeline",
        "prompt": "What timeline are you planning for? (optional)",
        "options": ["1_month", "3_months", "6_months", "12_months", "ongoing"]
      },
      "content_types": {
        "type": "array",
        "default": ["blog_posts", "social_media"],
        "description": "Preferred content types",
        "prompt": "What types of content interest you? (optional, select multiple)",
        "options": ["blog_posts", "whitepapers", "case_studies", "videos", "podcasts", "social_media", "email_campaigns"]
      },
      "competitor_examples": {
        "type": "string",
        "default": "",
        "description": "Competitor examples for analysis",
        "prompt": "Any competitors we should analyze? (optional)",
        "example": "Asana, Monday.com, Notion"
      }
    }
  },
  
  "preferences": {
    "model_selection": {
      "cost_priority": "balanced",
      "quality_threshold": 8.0,
      "max_cost_per_workflow": 0.75,
      "preferred_providers": ["anthropic-direct", "gemini-direct"],
      "fallback_strategy": "cost_optimize"
    },
    
    "execution": {
      "progress_updates": true,
      "verbose_output": false,
      "auto_approve_under": 0.10,
      "require_approval_over": 0.50,
      "cache_results": true,
      "save_intermediate": true
    },
    
    "output": {
      "workspace_naming": "{workflow_id}_{timestamp}",
      "deliverable_format": ["markdown", "pdf"],
      "include_metadata": true,
      "include_cost_report": true,
      "include_performance_metrics": true
    }
  },
  
  "command": {
    "name": "content_strategy_startup",
    "description": "Generate comprehensive content strategy for startup",
    "usage": "content_strategy_startup \"<business_description>\" \"<target_audience>\" \"<content_goals>\"",
    "examples": [
      "content_strategy_startup \"B2B SaaS for remote teams\" \"Team managers\" \"Lead generation and thought leadership\"",
      "content_strategy_startup --interactive",
      "content_strategy_startup --budget 5k_15k --timeline 6_months \"EdTech platform\" \"K-12 educators\" \"Brand awareness\""
    ]
  },
  
  "quality_assurance": {
    "success_criteria": [
      "Market research covers at least 5 competitor analysis points",
      "Strategy includes specific content calendar with themes", 
      "Content samples demonstrate brand voice consistency",
      "Final deliverable includes actionable next steps"
    ],
    "validation_checkpoints": [
      "research_completeness",
      "analysis_depth", 
      "strategy_specificity",
      "content_quality"
    ],
    "fallback_actions": {
      "insufficient_research": "extend_research_phase", 
      "low_quality_analysis": "upgrade_to_premium_model",
      "generic_strategy": "request_more_specific_inputs"
    }
  }
}
```

### Variable Types and Patterns

**Required Variables** - Must be provided for workflow to execute
- Always string type for maximum flexibility
- Clear prompts for setup conversation
- Real examples to guide user input
- No hardcoded categories or limitations

**Optional Variables** - Enhance workflow but have sensible defaults
- Include common options but allow custom input
- Default values enable one-click execution
- Arrays for multi-select options
- Empty string defaults for optional text

**Preference Variables** - Control execution behavior
- Model selection preferences and constraints
- Execution behavior (approvals, updates, caching)
- Output formatting and workspace organization
- Quality thresholds and fallback strategies

---

## 🎨 UI/TERMINAL DISPLAY IMPROVEMENTS

### Enhanced Progress Display

```
🎭 Content Strategy Workflow: B2B SaaS Startup
════════════════════════════════════════════════

Phase 1: Market Research [████████████████████] 100% ✅ (2m 34s)
├─ Market Analysis      [████████████████████] ✅ 47 sources analyzed
├─ Competitor Research  [████████████████████] ✅ 12 companies profiled  
├─ Audience Insights    [████████████████████] ✅ 3 key segments identified
└─ Trend Analysis       [████████████████████] ✅ 8 industry trends mapped

Phase 2: Content Analysis [██████████░░░░░░░░░░] 60% 🔄 (1m 12s)
├─ Content Gap Analysis [████████████████████] ✅ 15 gaps identified
├─ Voice & Tone Study   [███████████░░░░░░░░░] 🔄 In progress...
├─ Channel Assessment   [░░░░░░░░░░░░░░░░░░░░] ⏳ Queued
└─ Framework Selection  [░░░░░░░░░░░░░░░░░░░░] ⏳ Queued

Phase 3: Strategy Development [░░░░░░░░░░░░░░░░░░░░] 0% ⏳ Waiting
Phase 4: Content Creation [░░░░░░░░░░░░░░░░░░░░] 0% ⏳ Waiting

💰 Cost: $0.23/$0.75 budget | 🎯 Quality: 8.7/10 target | ⏱️ ETA: 8m 45s
🧠 Agent: Content Strategy Analyst using claude-sonnet-4 via anthropic-direct
```

### Workflow Summary Display

```
🎉 WORKFLOW COMPLETED SUCCESSFULLY
════════════════════════════════════════════════

📊 Performance Summary:
├─ Total Duration:     11m 47s (estimated: 12-15m)
├─ Total Cost:         $0.34 (budgeted: $0.75) 
├─ Quality Score:      9.2/10 (target: 8.0+)
├─ Cache Hits:         23% (saved $0.11)
└─ Success Rate:       100% (4/4 phases completed)

📁 Deliverables Created:
├─ 📄 Content_Strategy_Executive_Summary.md
├─ 📄 Market_Research_Analysis.md
├─ 📄 Content_Calendar_Q2_2025.md
├─ 📄 Brand_Voice_Guidelines.md
├─ 📄 Sample_Blog_Post_Templates.md
├─ 🎨 Content_Themes_Visual.png
└─ 📊 Workflow_Performance_Report.json

💡 Key Insights Discovered:
├─ 🔍 Competitor content gaps in technical education space
├─ 🎯 Opportunity for video content (86% audience preference)
├─ 📈 Best posting schedule: Tue/Thu for technical, Fri for culture
└─ 🚀 Recommended next step: Implement blog content pilot program

📍 Workspace: ~/MAO_Workflows/content_strategy_startup_20250614_1547/
🔗 Quick Actions: [📧 Email Summary] [📋 Copy Key Points] [🔄 Refine Strategy]
```

### Interactive Command Builder

```
🎯 MAO Workflow Setup Assistant
════════════════════════════════════════════════

I'll help you create a custom workflow. Let's start with the basics:

❓ What would you like to accomplish?
   Type your goal in plain English, or choose from common patterns:
   
   [1] 📊 Research & Analysis     [2] ✍️  Content Creation
   [3] 🎯 Strategy Development    [4] 🔍 Market Research  
   [5] 💼 Business Planning       [6] 🎨 Creative Projects
   
   > I want to create a content strategy for my B2B startup

✨ Great! I'll use the "Content Strategy" workflow pattern.

📝 Tell me about your business:
   > B2B SaaS platform for project management targeting remote teams

👥 Who's your target audience? 
   > Remote team managers at 50-500 person companies

🎯 What are your main content goals?
   > Build thought leadership and generate qualified leads

⚙️  Optional Settings:
   💰 Budget range: [flexible] ✏️ Change
   📅 Timeline: [3 months] ✏️ Change  
   🎨 Content types: [blog posts, social media] ✏️ Change
   
🔧 I'm creating your custom workflow...

✅ Workflow Created! Your new command:
   content_strategy_startup

📖 Usage:
   content_strategy_startup "B2B SaaS for remote teams" "Team managers" "Thought leadership"
   
🚀 Ready to run? [Y/n]
```

### Cost Monitoring Display

```
💰 COST MONITORING DASHBOARD
════════════════════════════════════════════════

Current Workflow: Content Strategy (content_strategy_startup)
Budget Allocated: $0.75 | Used: $0.34 | Remaining: $0.41

Phase Breakdown:
├─ Research:    $0.12 (✅ completed) [claude-sonnet-4]
├─ Analysis:    $0.08 (✅ completed) [gemini-2.5-pro]  
├─ Strategy:    $0.14 (✅ completed) [claude-sonnet-4]
└─ Content:     $0.00 (⏳ queued)    [estimated: $0.15]

Cache Savings: $0.11 (24% efficiency gain)
├─ Market research cache hit: $0.07 saved
└─ Competitor data cache hit: $0.04 saved

Model Optimization:
├─ 🟢 Cost-optimized phases: 2/4 (using gemini-2.5-pro)
├─ 🟡 Balanced phases: 1/4 (using claude-sonnet-4)  
└─ 🔴 Premium phases: 1/4 (using claude-opus-4 for strategy)

Monthly Usage: $4.23/$25.00 budget (83% remaining)
```

### Error Recovery Display

```
⚠️  WORKFLOW ISSUE DETECTED
════════════════════════════════════════════════

Phase: Market Research (Phase 1 of 4)
Issue: API rate limit exceeded (brave_search)
Impact: 2m delay, minimal cost impact

🔄 Auto-Recovery Options:
├─ [1] Switch to backup search tool (perplexity_search) [+$0.02]
├─ [2] Wait for rate limit reset (60 seconds) [+$0.00]
└─ [3] Reduce search scope and continue [+$0.00]

MAO Recommendation: Option 1 (switch tools)
Reason: Maintains quality, minimal cost increase, faster completion

Auto-executing in 10 seconds... [Space] to choose manually

🔄 Switching to perplexity_search...
✅ Recovery successful! Workflow continuing...
   New ETA: 13m 20s (was 12m 45s)
   New cost estimate: $0.36 (was $0.34)
```

---

## 🎬 SETUP CONVERSATION FLOW

### Natural Language Goal Processing

```python
def analyze_user_goal(goal_text: str) -> Dict[str, Any]:
    """
    Process natural language goals into workflow specifications
    
    Examples:
    "Create content strategy" → content_strategy pattern
    "Research my competitors" → competitive_research pattern  
    "Help with job applications" → job_application pattern
    "Analyze this market" → market_analysis pattern
    """
    
    patterns = {
        "content_strategy": {
            "keywords": ["content", "strategy", "marketing", "blog", "social"],
            "template": "content_strategy_generic",
            "required_vars": ["business_description", "target_audience", "content_goals"]
        },
        "market_research": {
            "keywords": ["research", "market", "competitor", "analysis", "industry"],  
            "template": "market_research_comprehensive",
            "required_vars": ["industry_focus", "research_scope", "key_questions"]
        },
        "job_application": {
            "keywords": ["job", "application", "resume", "cover letter", "interview"],
            "template": "job_application_complete", 
            "required_vars": ["job_description", "company_name", "candidate_background"]
        }
    }
```

### Interactive Variable Collection

```python
def collect_workflow_variables(pattern: str, user_responses: Dict) -> Dict:
    """
    Intelligent variable collection with context awareness
    """
    
    conversation_flow = {
        "content_strategy": [
            {
                "var": "business_description",
                "prompt": "Tell me about your business in 2-3 sentences:",
                "validation": "min_length:20",
                "followup": "What industry/sector?"
            },
            {
                "var": "target_audience", 
                "prompt": "Who's your ideal customer or audience?",
                "context_hint": "Based on '{business_description}'",
                "validation": "min_length:10"
            },
            {
                "var": "content_goals",
                "prompt": "What do you want to achieve with content?",
                "suggestions": ["lead_generation", "brand_awareness", "thought_leadership", "customer_education"],
                "allow_custom": True
            }
        ]
    }
```

### Command Generation Logic

```python
def generate_custom_command(config: Dict) -> Dict[str, str]:
    """
    Generate executable command from workflow configuration
    """
    
    # Command naming convention
    command_name = f"{config['meta']['id']}"
    
    # File structure creation
    use_case_dir = f"configs/use_case/{command_name}/"
    files_to_create = {
        f"{use_case_dir}config.json": config,
        f"{use_case_dir}README.md": generate_readme(config),
        f"{use_case_dir}command.py": generate_command_script(config)
    }
    
    # Shell command installation
    command_script = f"""#!/usr/bin/env python3
import sys
import json
from pathlib import Path

# Load configuration
config_path = Path(__file__).parent / "config.json"
with open(config_path) as f:
    config = json.load(f)

# Execute workflow with MAO
from mao_v4 import execute_workflow_from_config
result = execute_workflow_from_config(config, sys.argv[1:])
"""
    
    return {
        "command_name": command_name,
        "files": files_to_create,
        "install_script": command_script
    }
```

---

## 📁 WORKSPACE ORGANIZATION

### Directory Structure Pattern

```
~/MAO_Workflows/
├── content_strategy_startup_20250614_1547/
│   ├── 00_workflow_config.json              # Original configuration
│   ├── 01_research_phase/
│   │   ├── market_analysis.md
│   │   ├── competitor_profiles.md
│   │   ├── audience_insights.md
│   │   └── research_sources.json
│   ├── 02_analysis_phase/
│   │   ├── content_gap_analysis.md
│   │   ├── voice_tone_guidelines.md
│   │   └── framework_recommendations.md
│   ├── 03_strategy_phase/
│   │   ├── content_strategy_document.md
│   │   ├── content_calendar_q2.md
│   │   └── strategy_visual.png
│   ├── 04_content_phase/
│   │   ├── blog_post_templates/
│   │   ├── social_media_examples/
│   │   └── content_samples.md
│   ├── DELIVERABLES/                        # Final outputs
│   │   ├── Executive_Summary.md
│   │   ├── Implementation_Guide.md
│   │   └── Quick_Reference_Guide.pdf
│   └── METADATA/
│       ├── workflow_performance.json
│       ├── cost_breakdown.json
│       ├── agent_activity_log.json
│       └── cache_usage_report.json
```

### Automatic README Generation

```markdown
# Content Strategy for B2B SaaS Startup
*Generated by MAO v4 on June 14, 2025 at 3:47 PM*

## Workflow Summary
- **Pattern**: Content Strategy Development
- **Target**: B2B SaaS platform for remote team project management
- **Audience**: Remote team managers at 50-500 person companies  
- **Goals**: Build thought leadership and generate qualified leads

## Results Overview
- **Duration**: 11m 47s (estimated: 12-15m)
- **Cost**: $0.34 (budgeted: $0.75)
- **Quality**: 9.2/10 (target: 8.0+)
- **Phases**: 4/4 completed successfully

## Key Deliverables
1. **Executive Summary** - High-level strategy overview and recommendations
2. **Market Research** - Competitor analysis and industry insights  
3. **Content Calendar** - Q2 2025 content schedule with themes
4. **Implementation Guide** - Step-by-step execution plan

## Quick Actions
```bash
# Re-run this workflow
content_strategy_startup "B2B SaaS for remote teams" "Team managers" "Thought leadership"

# Customize timeline
content_strategy_startup --timeline 6_months "B2B SaaS for remote teams" "Team managers" "Thought leadership"

# Run in interactive mode
content_strategy_startup --interactive
```

## Next Steps
1. Review Executive Summary and strategy recommendations
2. Implement blog content pilot program (highest ROI opportunity)
3. Set up content calendar in your preferred tool
4. Begin with technical education content (identified gap)
```

---

## 🔧 COMMAND INSTALLATION SYSTEM

### Setup Script Pattern

```python
#!/usr/bin/env python3
"""
MAO Workflow Command Installer
Converts workflow configs into executable commands
"""

import os
import stat
import json
from pathlib import Path

def install_workflow_command(config: Dict, install_path: str = "/usr/local/bin"):
    """
    Install workflow as system command
    """
    
    command_name = config["command"]["name"]
    command_script = f"""#!/usr/bin/env python3
import sys
import os
import json
from pathlib import Path

# MAO Configuration
MAO_ROOT = "{Path.cwd()}"
CONFIG_PATH = "{Path.cwd()}/configs/use_case/{command_name}/config.json"

# Load workflow configuration
with open(CONFIG_PATH) as f:
    workflow_config = json.load(f)

# Add MAO to path and execute
sys.path.insert(0, MAO_ROOT)
from mao_v4 import execute_workflow_from_config

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description=workflow_config["meta"]["description"],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="\\n".join(workflow_config["command"]["examples"])
    )
    
    # Add required arguments
    for var_name, var_config in workflow_config["variables"]["required"].items():
        parser.add_argument(
            var_name,
            help=var_config["description"],
            metavar=var_config.get("example", "VALUE")
        )
    
    # Add optional arguments
    for var_name, var_config in workflow_config["variables"]["optional"].items():
        parser.add_argument(
            f"--{var_name}",
            default=var_config["default"],
            help=f"{var_config['description']} (default: {var_config['default']})"
        )
    
    # System arguments
    parser.add_argument("--interactive", action="store_true", help="Interactive setup mode")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without executing")
    
    args = parser.parse_args()
    
    # Execute workflow
    result = execute_workflow_from_config(workflow_config, vars(args))
    
    if result.get("success"):
        print(f"✅ Workflow completed successfully!")
        print(f"📁 Results: {result['workspace']}")
        print(f"💰 Cost: ${result['total_cost']:.6f}")
    else:
        print(f"❌ Workflow failed: {result.get('error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
"""
    
    # Write command script
    command_path = Path(install_path) / command_name
    with open(command_path, "w") as f:
        f.write(command_script)
    
    # Make executable
    os.chmod(command_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    
    return command_path
```

---

## 🎯 QUALITY ASSURANCE FRAMEWORK

### Success Criteria Validation

```python
def validate_workflow_quality(result: Dict, criteria: List[str]) -> Dict:
    """
    Validate workflow results against success criteria
    """
    
    validation_results = {}
    
    for criterion in criteria:
        if "market_research_covers" in criterion:
            # Example: "Market research covers at least 5 competitor analysis points"
            min_points = extract_number(criterion)
            actual_points = count_competitor_points(result)
            validation_results[criterion] = {
                "passed": actual_points >= min_points,
                "actual": actual_points,
                "required": min_points
            }
            
        elif "strategy_includes" in criterion:
            # Example: "Strategy includes specific content calendar with themes"
            required_elements = extract_elements(criterion)
            found_elements = find_strategy_elements(result)
            validation_results[criterion] = {
                "passed": all(elem in found_elements for elem in required_elements),
                "found": found_elements,
                "required": required_elements
            }
    
    return validation_results
```

### Automatic Quality Improvement

```python
def improve_workflow_quality(result: Dict, validation: Dict, config: Dict) -> Dict:
    """
    Automatically improve workflow quality based on validation results
    """
    
    improvements = []
    
    for criterion, validation_result in validation.items():
        if not validation_result["passed"]:
            
            if "research_completeness" in criterion:
                improvements.append({
                    "action": "extend_research_phase",
                    "reason": "Insufficient research depth",
                    "cost_impact": "+$0.05-0.10",
                    "time_impact": "+3-5 minutes"
                })
                
            elif "analysis_depth" in criterion:
                improvements.append({
                    "action": "upgrade_to_premium_model", 
                    "reason": "Analysis quality below threshold",
                    "cost_impact": "+$0.08-0.15",
                    "time_impact": "+2-4 minutes"
                })
    
    return improvements
```
