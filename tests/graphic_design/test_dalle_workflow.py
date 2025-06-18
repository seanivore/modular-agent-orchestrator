#!/usr/bin/env python3

# Test DALL-E 3 integration!
import asyncio
from orchestrator.core import WorkflowOrchestrator

async def test_image_generation_workflow():
    print('🎨 TESTING: Art History Image Generation Workflow')
    print('=' * 60)
    
    orchestrator = WorkflowOrchestrator()
    
    # Art history workflow like Sean used to make!
    art_goal = "Research Renaissance art styles and generate 3 original paintings in the style of Leonardo da Vinci"
    
    workflow = await orchestrator.create_workflow_from_goal(art_goal)
    
    print(f'\n🎭 DALL-E 3 WORKFLOW RESULTS:')
    print(f'📋 Phases: {len(workflow.phases)}')
    print(f'💰 Cost: ${workflow.total_estimated_cost:.4f}')
    
    print(f'\n🚀 PHASE BREAKDOWN:')
    for i, phase in enumerate(workflow.phases):
        model_config = orchestrator.model_manager.get_model_config(phase.model)
        art_indicator = "🎨" if "dalle" in phase.model or "image" in phase.name else "📚"
        print(f'{i+1}. {phase.name} {art_indicator}')
        print(f'   🤖 Model: {phase.model}')
        if model_config:
            print(f'   💰 Cost: ${phase.estimated_cost:.4f}')
            if hasattr(model_config, 'image_generation_price_per_image'):
                print(f'   🎨 Image generation model detected!')
    
    print(f'\n✨ Ready to create beautiful art history images! 🖼️')

if __name__ == "__main__":
    asyncio.run(test_image_generation_workflow())
