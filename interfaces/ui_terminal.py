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
        """🎨 Make model names human-friendly"""
        model_names = {
            "claude-sonnet-4-20250514": "Claude Sonnet 4",
            "claude-opus-4-20250514": "Claude Opus 4", 
            "claude-3-7-sonnet-20250219": "Claude 3.7 Sonnet",
            "google/gemini-2.5-pro-exp-03-25": "Gemini 2.5 Pro (FREE)",
            "openai/gpt-4.1-nano": "GPT-4.1 Nano",
            "openai/gpt-4.1-mini": "GPT-4.1 Mini",
            "dalle-3": "DALL-E 3",
            "local-llama-3.1-8b": "Llama 3.1 8B (Local)"
        }
        return model_names.get(model, model)
    
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
        
        response = input("Continue? (y/N): ").lower().strip()
        return response == 'y'
    
    def execution_start(self) -> None:
        """🚀 Show execution starting"""
        print(f"\n🚀 EXECUTING WORKFLOW...")
        print("=" * 60)
    
    def phase_start(self, phase_num: int, total_phases: int, phase_name: str, model: str, estimated_cost: float) -> None:
        """🎯 Show phase starting"""
        phase_display = phase_name.replace('_', ' ').title()
        model_display = self._format_model_name(model)
        
        print(f"\n🎯 Phase {phase_num}/{total_phases}: {phase_display}")
        print(f"   🤖 {model_display}")
        
        if self.verbose:
            print(f"   💰 Estimated cost: ${estimated_cost:.6f}")
            print(f"   🔄 Status: Initializing model connection...")
            print(f"   📡 Sending request to {model_display}...")
        else:
            print(f"   💰 ${estimated_cost:.4f}")
    
    def phase_complete(self, result: ExecutionResult) -> None:
        """✅ Show phase completion"""
        if result.success:
            print(f"   ✅ Completed in {result.duration_seconds:.1f}s")
            
            if self.verbose:
                print(f"   📊 Tokens used: {result.tokens_used:,}")
                print(f"   💸 Actual cost: ${result.cost:.6f}")
                print(f"   🔧 Tool calls made: {len(result.tool_calls)}")
                if result.tool_calls:
                    print(f"   🛠️  Tools used: {', '.join(set(tc.get('name', 'unknown') for tc in result.tool_calls))}")
                print(f"   📝 Content length: {len(result.content)} characters")
                print(f"   ⚡ Processing rate: {result.tokens_used/result.duration_seconds:.0f} tokens/second")
        else:
            print(f"   ❌ Failed: {result.error}")
            if self.verbose:
                print(f"   ⏱️  Failed after: {result.duration_seconds:.1f}s")
                print(f"   💸 Cost before failure: ${result.cost:.6f}")
                print(f"   🔍 Debug info: Check logs for detailed error trace")
    
    def workflow_complete(self, workflow: WorkflowPlan, results: Dict[str, Any]) -> None:
        """🎉 Show workflow completion"""
        print("=" * 60)
        
        successful = len([r for r in results['results'] if r['success']])
        total = len(workflow.phases)
        
        if successful == total:
            print("🎉 WORKFLOW COMPLETED!")
        else:
            print(f"⚠️  WORKFLOW COMPLETED WITH ISSUES")
        
        print(f"💰 Total cost: ${results['total_cost']:.4f}")
        print(f"📊 Success rate: {successful}/{total} phases")
        
        if self.verbose:
            total_tokens = sum(r['tokens_used'] for r in results['results'])
            total_time = sum(r['duration_seconds'] for r in results['results'])
            avg_cost_per_token = results['total_cost'] / total_tokens if total_tokens > 0 else 0
            
            print(f"\n📊 DETAILED STATISTICS:")
            print(f"   Total tokens processed: {total_tokens:,}")
            print(f"   Total execution time: {total_time:.1f} seconds")
            print(f"   Average processing rate: {total_tokens/total_time:.0f} tokens/second")
            print(f"   Average cost per token: ${avg_cost_per_token:.8f}")
            print(f"   Cost efficiency: {total_tokens/results['total_cost']:.0f} tokens per dollar")
            
            # Show per-phase performance
            print(f"\n⚡ PHASE PERFORMANCE:")
            for i, result in enumerate(results['results'], 1):
                status = "✅" if result['success'] else "❌"
                rate = result['tokens_used']/result['duration_seconds'] if result['duration_seconds'] > 0 else 0
                print(f"   Phase {i}: {status} {result['tokens_used']:,} tokens in {result['duration_seconds']:.1f}s ({rate:.0f} t/s)")
            
            # Show cost breakdown
            print(f"\n💸 COST BREAKDOWN:")
            model_costs = {}
            for result in results['results']:
                model = result['model_used']
                if model not in model_costs:
                    model_costs[model] = {'cost': 0, 'tokens': 0}
                model_costs[model]['cost'] += result['cost']
                model_costs[model]['tokens'] += result['tokens_used']
            
            for model, data in model_costs.items():
                model_display = self._format_model_name(model)
                print(f"   {model_display}: ${data['cost']:.4f} ({data['tokens']:,} tokens)")
                
            # Show any tool usage
            all_tools = []
            for result in results['results']:
                for tool_call in result.get('tool_calls', []):
                    tool_name = tool_call.get('name', 'unknown')
                    if tool_name not in all_tools:
                        all_tools.append(tool_name)
            
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

# These are from the mao_v4.py file to go in the 'MaoTerminalInterface' class

def handle_critical_error(self, error: Exception) -> None:
    """
    Handle critical system errors with beautiful formatting
    """
    from rich.panel import Panel
    from rich.text import Text
    
    error_text = Text()
    error_text.append("❌ Critical System Error\n\n", style="bold red")
    error_text.append(f"Error: {str(error)}\n", style="red")
    error_text.append(f"Type: {type(error).__name__}\n", style="dim")
    
    if self.verbose:
        import traceback
        error_text.append(f"\nStack trace:\n{traceback.format_exc()}", style="dim red")
    
    error_text.append("\n💡 Troubleshooting:\n", style="bold yellow")
    error_text.append("   • Check system requirements\n", style="yellow")
    error_text.append("   • Verify dependencies: pip install -r requirements.txt\n", style="yellow")
    error_text.append("   • Try running with --debug for more details\n", style="yellow")
    
    panel = Panel(
        error_text,
        title="[bold red]System Error[/bold red]",
        border_style="red",
        padding=(1, 2)
    )
    
    self.console.print(panel)

def handle_bootstrap_failure(self, error_details: str) -> None:
    """
    Handle bootstrap failures with user-friendly guidance
    """
    from rich.panel import Panel
    from rich.text import Text
    
    help_text = Text()
    help_text.append("🚨 Bootstrap Failure\n\n", style="bold red")
    help_text.append("Mao cannot start due to missing dependencies.\n\n", style="red")
    help_text.append("📋 Required Actions:\n", style="bold yellow")
    help_text.append("   1. pip install -r requirements.txt\n", style="green")
    help_text.append("   2. python -m pip install --upgrade pip\n", style="green")
    help_text.append("   3. Check Python version (3.8+ required)\n", style="green")
    help_text.append(f"\n🔍 Technical Details: {error_details}", style="dim")
    
    panel = Panel(
        help_text,
        title="[bold red]Installation Required[/bold red]",
        border_style="red",
        padding=(1, 2)
    )
    
    self.console.print(panel)

def show_installation_help(self) -> None:
    """
    Show comprehensive installation and setup help
    """
    from rich.panel import Panel
    from rich.text import Text
    
    help_text = Text()
    help_text.append("🛠️ Mao Installation Guide\n\n", style="bold blue")
    help_text.append("Required Dependencies:\n", style="bold")
    help_text.append("   • Python 3.8 or higher\n", style="green")
    help_text.append("   • pip (Python package manager)\n", style="green")
    help_text.append("   • Internet connection for AI models\n", style="green")
    
    help_text.append("\n📦 Installation Steps:\n", style="bold")
    help_text.append("   1. pip install -r requirements.txt\n", style="cyan")
    help_text.append("   2. Set up API keys (see documentation)\n", style="cyan")
    help_text.append("   3. Run: python mao_v4.py --doctor\n", style="cyan")
    
    help_text.append("\n🔧 Common Issues:\n", style="bold")
    help_text.append("   • ImportError: Missing dependencies\n", style="yellow")
    help_text.append("   • AuthError: Invalid API keys\n", style="yellow")
    help_text.append("   • NetworkError: Internet connection\n", style="yellow")
    
    panel = Panel(
        help_text,
        title="[bold blue]Installation Help[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    )
    
    self.console.print(panel)

class OCTerminalInterface:
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
        
        self.display.header("OC - AI Workflow Orchestrator", goal)
        
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
                "total_cost": results["total_cost"],
                "deliverables": [str(workspace_path / f) for phase in workflow.phases for f in phase.output_files]
            }
            
        except Exception as e:
            self.display.error(str(e))
            return {"success": False, "error": str(e)}
    
    async def _execute_with_progress(self, workflow: WorkflowPlan) -> Dict[str, Any]:
        """Execute workflow with live progress display"""
        results = {"results": [], "total_cost": 0.0}
        
        for i, phase in enumerate(workflow.phases, 1):
            self.display.phase_start(i, len(workflow.phases), phase.name, phase.model, phase.estimated_cost)
            
            # For now, simulate execution (in real version, this calls orchestrator)
            # This is where the orchestrator.execute_workflow would be called per-phase
            result = ExecutionResult(
                phase_name=phase.name,
                model_used=phase.model,
                content="[Generated content would be here]",
                tool_calls=[],
                tokens_used=phase.estimated_tokens,
                cost=phase.estimated_cost,
                duration_seconds=2.0,  # Simulated
                success=True
            )
            
            self.display.phase_complete(result)
            results["results"].append(asdict(result))
            results["total_cost"] += result.cost
        
        return results
    
    async def _create_deliverables(self, workspace_path: Path, workflow: WorkflowPlan) -> None:
        """Create actual deliverable files"""
        # Create workflow summary
        summary = {
            "workflow_name": workflow.name,
            "executed_at": datetime.now().isoformat(),
            "total_cost": workflow.total_estimated_cost,
            "phases_completed": len(workflow.phases),
            "workspace": str(workspace_path)
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
*Generated by OC Orchestrator*
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
    
    async def job_application_workflow(
        self, 
        job_description: str, 
        company: str,
        workspace: Optional[str] = None
    ) -> Dict[str, Any]:
        """📄 Specialized job application workflow"""
        
        goal = f"""Create a complete job application package for a position at {company}. 
        Research the company, analyze the job requirements, create a tailored resume and cover letter, 
        and prepare interview talking points. Job description: {job_description}"""
        
        preferences = {
            "optimize_for": "job_application",
            "include_research": True,
            "output_formats": ["pdf", "docx", "txt"]
        }
        
        return await self.execute_goal(goal, workspace, preferences)
    
    def get_stats(self) -> None:
        """📊 Show orchestrator statistics"""
        stats = self.orchestrator.model_manager.get_stats()
        
        print("📊 OC ORCHESTRATOR STATS")
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
                if capabilities.get('caching'): caps.append('caching')
                if capabilities.get('code_execution'): caps.append('code')
                print(f"    Capabilities: {', '.join(caps) if caps else 'text-only'}")
                
            print(f"\n🏢 PROVIDER DETAILS:")
            for provider_name, provider_info in self.orchestrator.model_manager.providers.items():
                print(f"  • {provider_info.get('display_name', provider_name)}:")
                print(f"    Base URL: {provider_info.get('base_url', 'N/A')}")
                print(f"    API Type: {provider_info.get('api_type', 'unknown')}")
                rate_limits = provider_info.get('rate_limits', {})
                if rate_limits:
                    print(f"    Rate limits: {rate_limits.get('requests_per_minute', 'N/A')} req/min, {rate_limits.get('tokens_per_minute', 'N/A')} tokens/min")
                    
            print(f"\n📈 OPTIMIZATION OPPORTUNITIES:")
            free_models = [m for m, info in self.orchestrator.model_manager.models.items() 
                          if info.get('input_price_per_million', 1) == 0]
            if free_models:
                print(f"   💰 {len(free_models)} free models available for cost optimization")
                
            tool_models = [m for m, info in self.orchestrator.model_manager.models.items() 
                          if info.get('capabilities', {}).get('tools')]
            print(f"   🔧 {len(tool_models)} models support tool use")
            
            vision_models = [m for m, info in self.orchestrator.model_manager.models.items() 
                            if info.get('capabilities', {}).get('vision')]
            if vision_models:
                print(f"   👁️  {len(vision_models)} models support vision tasks")
                
            # Show current workflow history
            workflows = self.orchestrator.list_workflows()
            if workflows:
                total_workflow_cost = sum(w.get('estimated_cost', 0) for w in workflows)
                print(f"\n📊 WORKFLOW HISTORY:")
                print(f"   Total workflows created: {len(workflows)}")
                print(f"   Total estimated cost: ${total_workflow_cost:.4f}")
        else:
            # Show a hint about verbose mode
            print(f"\n💡 Use --verbose flag for detailed model and provider information")
    
    def list_workflows(self) -> None:
        """📋 List all available workflows"""
        workflows = self.orchestrator.list_workflows()
        
        if not workflows:
            print("📋 No workflows found")
            return
        
        print("📋 AVAILABLE WORKFLOWS:")
        print("-" * 50)
        
        for wf in workflows:
            print(f"🎭 {wf['name']}")
            if self.verbose:
                print(f"   📝 {wf['description']}")
                print(f"   📊 {wf['phases']} phases | ${wf['estimated_cost']:.4f} | {wf['status']}")
            else:
                print(f"   📊 {wf['phases']} phases • ${wf['estimated_cost']:.4f}")
            print()


# Example usage showing the clean separation
async def demo_clean_interface():
    """🎨 Demo the beautiful clean interface"""
    
    # Regular user experience (clean and simple)
    oc = OCTerminalInterface(verbose=False)
    
    print("🎨 REGULAR USER EXPERIENCE:")
    await mao.execute_goal("Create a marketing plan for my startup")
    
    print("\n" + "="*60 + "\n")
    
    # Developer experience (verbose technical details)
    oc_verbose = OCTerminalInterface(verbose=True)
    
    print("🛠️  DEVELOPER EXPERIENCE:")
    await oc_verbose.execute_goal("Create a marketing plan for my startup")


if __name__ == "__main__":
    asyncio.run(demo_clean_interface())