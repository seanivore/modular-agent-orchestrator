#!/usr/bin/env python3
"""
Clean Terminal User Interface
Beautiful, human-friendly terminal UI that's completely separate from logic!
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import asdict

from orchestrator.core import WorkflowOrchestrator, WorkflowPlan, ExecutionResult


class TerminalDisplay:
    """🎨 Beautiful terminal display that users actually want to see!"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        
    def header(self, title: str, goal: str) -> None:
        """🎭 Show beautiful header"""
        print(f"🎭 {title}")
        print("=" * 60)
        print(f"🎯 GOAL: {goal}")
        print("=" * 60)
    
    def workflow_created(self, workflow: WorkflowPlan) -> None:
        """📋 Show workflow creation success"""
        print(f"\n🧠 Workflow designed: {workflow.name}")
        print(f"📊 {len(workflow.phases)} phases • ${workflow.total_estimated_cost:.4f} • ~{workflow.estimated_duration_minutes} min")
        
        if self.verbose:
            print(f"\n📋 TECHNICAL DETAILS:")
            print(f"   Workflow ID: {workflow.id}")
            print(f"   Generated name: {workflow.name}")
            print(f"   Workspace dir: {workflow.workspace_dir}")
            print(f"   Description: {workflow.description}")
            print(f"   Total estimated cost: ${workflow.total_estimated_cost:.6f}")
            print(f"   Duration estimate: {workflow.estimated_duration_minutes} minutes")
            
            # Show task type analysis
            print(f"\n🔍 GOAL ANALYSIS:")
            print(f"   Original goal: {workflow.description}")
            
            # Show model selection reasoning
            models_used = {}
            for phase in workflow.phases:
                if phase.model not in models_used:
                    models_used[phase.model] = []
                models_used[phase.model].append(phase.name)
            
            print(f"\n🤖 MODEL SELECTION REASONING:")
            for model, phases in models_used.items():
                print(f"   {self._format_model_name(model)}:")
                print(f"     • Used for: {', '.join(phases)}")
                print(f"     • Phase count: {len(phases)}")
                
            # Cost breakdown by model
            print(f"\n💰 COST BREAKDOWN BY MODEL:")
            for model, phases in models_used.items():
                model_cost = sum(p.estimated_cost for p in workflow.phases if p.model == model)
                model_tokens = sum(p.estimated_tokens for p in workflow.phases if p.model == model)
                print(f"   {self._format_model_name(model)}: ${model_cost:.4f} ({model_tokens:,} tokens)")
                
            # Show dependencies between phases
            print(f"\n🔗 PHASE DEPENDENCIES:")
            for i, phase in enumerate(workflow.phases, 1):
                if phase.input_sources:
                    print(f"   Phase {i} ({phase.name}) depends on: {', '.join(phase.input_sources)}")
                else:
                    print(f"   Phase {i} ({phase.name}): Independent (no dependencies)")
    
    def workspace_info(self, workspace_path: Path) -> None:
        """📁 Show workspace setup"""
        print(f"📁 Workspace: {workspace_path}")
    
    def phase_summary(self, workflow: WorkflowPlan) -> None:
        """🎭 Show beautiful phase summary"""
        print(f"\n🎭 WORKFLOW PHASES:")
        
        for i, phase in enumerate(workflow.phases, 1):
            # Beautiful human display
            phase_name = phase.name.replace('_', ' ').title()
            model_display = self._format_model_name(phase.model)
            
            print(f"  {i}. {phase_name}")
            print(f"     🤖 {model_display}")
            print(f"     💰 ${phase.estimated_cost:.4f}")
            
            if self.verbose:
                print(f"     📄 Outputs: {', '.join(phase.output_files)}")
                print(f"     🧠 Agent role: {phase.agent_role}")
                print(f"     📊 Estimated tokens: {phase.estimated_tokens:,}")
                print(f"     📝 Task instructions: {phase.task_instructions}")
                if phase.input_sources:
                    print(f"     📥 Input sources: {', '.join(phase.input_sources)}")
                else:
                    print(f"     📥 Input sources: None (independent phase)")
                
                # Show cost breakdown for this phase
                input_tokens = int(phase.estimated_tokens * 0.7)
                output_tokens = int(phase.estimated_tokens * 0.3)
                print(f"     💸 Cost details: ~{input_tokens:,} input + {output_tokens:,} output tokens")
            else:
                print(f"     📄 {len(phase.output_files)} deliverable{'s' if len(phase.output_files) > 1 else ''}")
    
    def _format_model_name(self, model: str) -> str:
        """🎨 Make model names human-friendly using dynamic lookup"""
        # Use the orchestrator's model manager to get display names
        try:
            from orchestrator.manager_models import ModelManager
            model_manager = ModelManager()
            model_config = model_manager.get_model_config(model)
            if model_config and hasattr(model_config, 'display_name'):
                return model_config.display_name
        except Exception:
            pass
        
        # Fallback to cleaning up the model name if lookup fails
        if model.startswith('claude-'):
            if 'sonnet-4' in model:
                return "Claude Sonnet 4"
            elif 'opus-4' in model:
                return "Claude Opus 4"
            elif '3-7-sonnet' in model:
                return "Claude 3.7 Sonnet"
            return model.replace('-', ' ').title()
        elif model.startswith('openai/'):
            return model.split('/')[-1].replace('-', ' ').upper()
        elif model.startswith('google/'):
            return model.split('/')[-1].replace('-', ' ').title()
        elif 'gemini' in model.lower():
            return model.replace('-', ' ').title()
        elif 'local-' in model:
            return model.replace('local-', '').replace('-', ' ').title() + " (Local)"
        
        # Default: return the model name cleaned up
        return model.replace('-', ' ').title()
    
    def execution_confirm(self, workflow: WorkflowPlan) -> bool:
        """⚠️ Confirm execution for multi-phase workflows"""
        if len(workflow.phases) == 1:
            if self.verbose:
                print(f"\n⚡ Single phase workflow - executing immediately")
            return True
            
        print(f"\n⚠️  Ready to execute {len(workflow.phases)} phases for ${workflow.total_estimated_cost:.4f}")
        
        if self.verbose:
            total_tokens = sum(p.estimated_tokens for p in workflow.phases)
            print(f"   📊 Estimated tokens: {total_tokens:,}")
            print(f"   ⏱️  Estimated time: {workflow.estimated_duration_minutes} minutes")
            print(f"   🔄 Execution order: {' → '.join(p.name.replace('_', ' ').title() for p in workflow.phases)}")
            
            # Show what files will be created
            all_files = []
            for phase in workflow.phases:
                all_files.extend(phase.output_files)
            print(f"   📁 Will create {len(all_files)} files: {', '.join(all_files)}")
        
        response = input("Continue? [Y/n]: ").strip().lower()
        return response in ['', 'y', 'yes']
    
    def execution_start(self) -> None:
        """🚀 Show execution start"""
        print(f"\n🚀 Starting workflow execution...")
    
    def phase_progress(self, phase_name: str, progress: float, current_step: str = None) -> None:
        """📊 Show phase progress"""
        bar_length = 20
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        phase_display = phase_name.replace('_', ' ').title()
        
        if current_step:
            print(f"   {phase_display}: [{bar}] {progress:.1%} - {current_step}")
        else:
            print(f"   {phase_display}: [{bar}] {progress:.1%}")
    
    def phase_complete(self, phase_name: str, result: Dict[str, Any]) -> None:
        """✅ Show phase completion"""
        phase_display = phase_name.replace('_', ' ').title()
        print(f"✅ {phase_display} completed")
        
        if self.verbose and result:
            if 'cost' in result:
                print(f"   💰 Cost: ${result['cost']:.4f}")
            if 'tokens_used' in result:
                print(f"   📊 Tokens: {result['tokens_used']:,}")
            if 'files_created' in result:
                print(f"   📄 Files: {', '.join(result['files_created'])}")
    
    def workflow_complete(self, workflow: WorkflowPlan, results: List[Dict[str, Any]]) -> None:
        """🎉 Show workflow completion"""
        print(f"\n🎉 Workflow '{workflow.name}' completed successfully!")
        
        total_cost = sum(r.get('cost', 0) for r in results)
        total_tokens = sum(r.get('tokens_used', 0) for r in results)
        
        print(f"💰 Total cost: ${total_cost:.4f}")
        
        if self.verbose:
            print(f"📊 Total tokens: {total_tokens:,}")
            print(f"⏱️  Duration: {workflow.estimated_duration_minutes} minutes (estimated)")
            
            # Show tools used across all phases
            all_tools = set()
            for result in results:
                if 'tools_used' in result:
                    all_tools.update(result['tools_used'])
            
            if all_tools:
                print(f"\n🛠️  TOOLS USED: {', '.join(all_tools)}")
            else:
                print(f"\n🛠️  No external tools required")
    
    def deliverables_created(self, workspace_path: Path, workflow: WorkflowPlan) -> None:
        """📁 Show deliverables creation"""
        print(f"📁 Deliverables saved to: {workspace_path}")
        
        if self.verbose:
            print(f"\n📄 FILES CREATED:")
            all_files = []
            for phase in workflow.phases:
                all_files.extend(phase.output_files)
            
            for file in all_files:
                print(f"  ✅ {file}")
        else:
            total_files = sum(len(phase.output_files) for phase in workflow.phases)
            print(f"📄 {total_files} files created")
    
    def error(self, message: str) -> None:
        """❌ Show error message"""
        print(f"\n❌ ERROR: {message}")
    
    def cancelled(self) -> None:
        """❌ Show cancellation"""
        print("❌ Execution cancelled")
    
    def success_summary(self, workspace: str, cost: float) -> None:
        """🎉 Show final success"""
        print(f"\n🎉 Goal completed successfully!")
        print(f"📁 Results: {workspace}")
        print(f"💰 Cost: ${cost:.4f}")


class TerminalInterface:
    """🎭 Clean terminal interface - UI separated from logic!"""
    
    def __init__(self, config_dir: str = "configs", verbose: bool = False):
        self.orchestrator = WorkflowOrchestrator(config_dir)
        self.display = TerminalDisplay(verbose)
        self.verbose = verbose
        
    async def execute_goal(
        self, 
        goal: str, 
        workspace: Optional[str] = None,
        preferences: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """🚀 Execute a goal with beautiful UI"""
        
        self.display.header("AI Workflow Orchestrator", goal)
        
        try:
            # Create workflow
            workflow = await self.orchestrator.create_workflow_from_goal(goal, preferences)
            self.display.workflow_created(workflow)
            
            # Set up workspace
            workspace_path = Path(workspace) if workspace else Path(workflow.workspace_dir)
            workspace_path.mkdir(parents=True, exist_ok=True)
            self.display.workspace_info(workspace_path)
            
            # Show phases
            self.display.phase_summary(workflow)
            
            # Confirm execution
            if not self.display.execution_confirm(workflow):
                self.display.cancelled()
                return {"cancelled": True}
            
            # Execute workflow
            self.display.execution_start()
            
            # Show progress for each phase
            results = await self._execute_with_progress(workflow)
            
            # Create actual files
            await self._create_deliverables(workspace_path, workflow)
            
            # Show completion
            self.display.workflow_complete(workflow, results)
            self.display.deliverables_created(workspace_path, workflow)
            
            return {
                "success": True,
                "workflow_id": workflow.id,
                "workspace": str(workspace_path),
                "total_cost": workflow.total_estimated_cost,
                "results": results
            }
            
        except Exception as e:
            self.display.error(str(e))
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _execute_with_progress(self, workflow: WorkflowPlan) -> List[Dict[str, Any]]:
        """🔄 Execute workflow phases with progress display"""
        results = []
        
        for i, phase in enumerate(workflow.phases):
            # Phase start
            self.display.phase_progress(phase.name, 0.0, "Starting...")
            
            # Execute phase (this would call the actual orchestrator)
            result = await self.orchestrator.execute_phase(phase)
            
            # Phase completion
            self.display.phase_complete(phase.name, result)
            results.append(result)
        
        return results
    
    async def _create_deliverables(self, workspace_path: Path, workflow: WorkflowPlan) -> None:
        """📁 Create deliverable files in workspace"""
        
        # Create workflow summary
        summary = {
            "workflow_id": workflow.id,
            "name": workflow.name,
            "description": workflow.description,
            "total_phases": len(workflow.phases),
            "total_estimated_cost": workflow.total_estimated_cost,
            "estimated_duration_minutes": workflow.estimated_duration_minutes,
            "created_timestamp": datetime.now().isoformat(),
            "phases": [asdict(phase) for phase in workflow.phases]
        }
        
        summary_file = workspace_path / "workflow_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Create deliverable files
        for phase in workflow.phases:
            for output_file in phase.output_files:
                file_path = workspace_path / output_file
                
                if output_file.endswith('.md'):
                    content = f"""# {output_file.replace('_', ' ').title().replace('.md', '')}

Generated by: {self.display._format_model_name(phase.model)}
Phase: {phase.name.replace('_', ' ').title()}
Agent Role: {phase.agent_role}

## Task Instructions
{phase.task_instructions}

## Generated Content
[This would be the actual AI-generated content from {phase.model}]

---
*Generated by AI Workflow Orchestrator*
*Timestamp: {datetime.now().isoformat()}*
*Cost: ${phase.estimated_cost:.4f}*
"""
                elif output_file.endswith('.json'):
                    content = json.dumps({
                        "generated_by": phase.model,
                        "phase": phase.name,
                        "timestamp": datetime.now().isoformat(),
                        "cost": phase.estimated_cost,
                        "data": "[Actual structured data would be here]"
                    }, indent=2)
                else:
                    content = f"Generated by {phase.model} in phase {phase.name}\nTimestamp: {datetime.now().isoformat()}\nCost: ${phase.estimated_cost:.4f}\n\n[Actual content would be here]"
                
                with open(file_path, 'w') as f:
                    f.write(content)
    
    def get_stats(self) -> None:
        """📊 Show orchestrator statistics"""
        stats = self.orchestrator.model_manager.get_stats()
        
        print("📊 AI WORKFLOW ORCHESTRATOR STATS")
        print("=" * 40)
        print(f"🤖 Total models: {stats['total_models']}")
        print(f"🏢 Total providers: {stats['total_providers']}")
        print(f"💰 Free models: {stats['free_models']}")
        print(f"🔧 Models with tools: {stats['models_with_tools']}")
        
        if self.verbose:
            print(f"🖼️  Models with vision: {stats.get('models_with_vision', 0)}")
            print(f"🎨 Models with image generation: {stats.get('models_with_image_generation', 0)}")
            
            print(f"\n🤖 DETAILED MODEL INVENTORY:")
            for model_name, model_info in self.orchestrator.model_manager.models.items():
                provider = model_info.get('provider', 'unknown')
                input_cost = model_info.get('input_price_per_million', 0)
                output_cost = model_info.get('output_price_per_million', 0)
                context = model_info.get('context_window', 0)
                max_output = model_info.get('max_output', 0)
                capabilities = model_info.get('capabilities', {})
                
                print(f"  • {self.display._format_model_name(model_name)}:")
                print(f"    Provider: {provider}")
                print(f"    Cost: ${input_cost:.2f}/${output_cost:.2f} per million (in/out)")
                print(f"    Context: {context:,} tokens, Max output: {max_output:,}")
                
                caps = []
                if capabilities.get('tools'): caps.append('tools')
                if capabilities.get('vision'): caps.append('vision')
                if capabilities.get('image_generation'): caps.append('images')
                if caps:
                    print(f"    Capabilities: {', '.join(caps)}")
    
    def list_workflows(self) -> None:
        """📋 Show available workflow patterns"""
        print("📋 AVAILABLE WORKFLOW PATTERNS")
        print("=" * 40)
        
        patterns = [
            {
                "name": "Research & Analysis",
                "description": "Multi-source research with comprehensive analysis",
                "example": "Research renewable energy trends and create investment recommendations",
                "phases": ["research", "analysis", "synthesis"],
                "cost_range": "$0.05-0.25"
            },
            {
                "name": "Content Creation",
                "description": "Research-backed content with multiple formats",
                "example": "Create blog post series about AI developments",
                "phases": ["research", "writing", "editing"],
                "cost_range": "$0.03-0.15"
            },
            {
                "name": "Technical Development",
                "description": "Code generation with documentation",
                "example": "Build a REST API with documentation",
                "phases": ["planning", "coding", "documentation", "testing"],
                "cost_range": "$0.10-0.50"
            },
            {
                "name": "Creative Projects",
                "description": "Visual and written content generation",
                "example": "Design marketing campaign with visuals and copy",
                "phases": ["concept", "design", "copywriting", "refinement"],
                "cost_range": "$0.15-0.75"
            }
        ]
        
        for i, pattern in enumerate(patterns, 1):
            print(f"\n{i}. {pattern['name']}")
            print(f"   📝 {pattern['description']}")
            print(f"   💡 Example: {pattern['example']}")
            print(f"   🎭 Phases: {' → '.join(pattern['phases'])}")
            print(f"   💰 Cost range: {pattern['cost_range']}")
        
        print(f"\n💡 Tip: Describe your goal naturally - the orchestrator will create the optimal workflow!")
    
    def help(self) -> None:
        """❓ Show help information"""
        print("❓ AI WORKFLOW ORCHESTRATOR HELP")
        print("=" * 40)
        print("🎯 GETTING STARTED:")
        print("   Just describe what you want to accomplish!")
        print("   Example: 'Research competitor pricing and create a strategy document'")
        print("")
        print("📊 USEFUL COMMANDS:")
        print("   --stats     Show system statistics")
        print("   --workflows Show available workflow patterns") 
        print("   --verbose   Show detailed execution information")
        print("   --help      Show this help message")
        print("")
        print("💡 TIPS:")
        print("   • Be specific about your desired outputs")
        print("   • Mention if you need specific formats (PDF, JSON, etc.)")
        print("   • Include any constraints or preferences")
        print("")
        print("🔧 TROUBLESHOOTING:")
        print("   1. Set up API keys (see documentation)")
        print("   2. Run: python mao_v4.py --doctor")
        print("")
        print("🔧 Common Issues:")
        print("   • ImportError: Missing dependencies")
        print("   • AuthError: Invalid API keys") 
        print("   • NetworkError: Internet connection")


# Clean interface - no legacy compatibility needed