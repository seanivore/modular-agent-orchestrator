#!/usr/bin/env python3

# Quick test of our orchestrator magic!
from orchestrator.manager_models import ModelManager
from orchestrator.manager_buttons import ButtonManager

print('🎭 Testing SFA v4 Orchestrator!')
print('=' * 40)

# Test model manager
manager = ModelManager()
print(f'✅ Models loaded: {len(manager.models)}')
print(f'💰 Free models: {len(manager.list_free_models())}')
print(f'🔧 Models with tools: {len(manager.list_models_by_capability("tools"))}')

# Test model selection
research_model = manager.get_best_model_for_task('research')
reasoning_model = manager.get_best_model_for_task('reasoning')
print(f'\n🎯 Best for research: {research_model}')
print(f'🧠 Best for reasoning: {reasoning_model}')

# Test human buttons
buttons = ButtonManager(manager)
print(f'\n🚀 Testing human button generation...')
snippet = buttons.create_api_call_snippet(research_model, 'Test prompt')
print(f'✅ Generated {len(snippet)} character snippet for {research_model}')

print('\n🎉 All systems operational! Ready to orchestrate! 💎')
