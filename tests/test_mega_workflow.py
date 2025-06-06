#!/usr/bin/env python3

# Let's test something REALLY complex!
import asyncio
from orchestrator.core import WorkflowOrchestrator

async def test_mega_complex_workflow():
    print('🌟 TESTING MEGA COMPLEX WORKFLOW')
    print('=' * 60)
    
    orchestrator = WorkflowOrchestrator()
    
    # Something that would have been IMPOSSIBLE to manually configure
    mega_goal = "Research AI market trends, analyze our competition, create a comprehensive business strategy with visual branding guidelines, and code a landing page prototype"
    
    workflow = await orchestrator.create_workflow_from_goal(mega_goal)
    
    print(f'\n🎭 ORCHESTRATOR MAGIC RESULTS:')
    print(f'📋 Phases: {len(workflow.phases)}')
    print(f'💰 Cost: ${workflow.total_estimated_cost:.4f}')
    print(f'⏱️  Time: {workflow.estimated_duration_minutes} minutes')
    
    print(f'\n🚀 WORKFLOW PHASES:')
    for i, phase in enumerate(workflow.phases):
        model_config = orchestrator.model_manager.get_model_config(phase.model)
        cost_indicator = "🆓" if model_config.input_price == 0 else "💰"
        print(f'{i+1}. {phase.name} {cost_indicator}')
        print(f'   🤖 {phase.model}')
        print(f'   🎭 {phase.agent_role[:60]}...')
        print(f'   💸 ${phase.estimated_cost:.4f}')
    
    print(f'\n🎉 THAT would have taken HOURS to configure manually!')
    print(f'🚀 Now it takes 1 sentence and happens automatically!')

if __name__ == "__main__":
    asyncio.run(test_mega_complex_workflow())
