#!/usr/bin/env python3

# Test Sean's first planned agentic use case!
import asyncio
from orchestrator.core import WorkflowOrchestrator

async def test_competitor_pricing_workflow():
    print('🎯 TESTING: "Research competitor pricing and create a strategy presentation"')
    print('=' * 70)
    
    orchestrator = WorkflowOrchestrator()
    
    # Sean's planned use case
    workflow = await orchestrator.create_workflow_from_goal(
        "Research competitor pricing and create a strategy presentation"
    )
    
    print(f'\n📋 WORKFLOW PLAN GENERATED:')
    print(f'Name: {workflow.name}')
    print(f'Phases: {len(workflow.phases)}')
    print(f'Estimated Cost: ${workflow.total_estimated_cost:.4f}')
    print(f'Estimated Time: {workflow.estimated_duration_minutes} minutes')
    
    print(f'\n🎭 PHASE BREAKDOWN:')
    for i, phase in enumerate(workflow.phases):
        print(f'{i+1}. {phase.name}')
        print(f'   🤖 Model: {phase.model}')
        print(f'   🎭 Role: {phase.agent_role}')
        print(f'   💰 Cost: ${phase.estimated_cost:.4f}')
        print(f'   📁 Outputs: {", ".join(phase.output_files)}')
    
    print(f'\n🚀 Ready to execute! This would run via Claude 4 Code Execution Tool')

if __name__ == "__main__":
    asyncio.run(test_competitor_pricing_workflow())
