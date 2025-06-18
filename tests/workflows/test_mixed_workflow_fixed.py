async def test_mixed_workflow():
    """Test: Mixed text + image workflow to stress test the orchestrator"""
    
    orchestrator = WorkflowOrchestrator("configs")
    
    print("\n" + "=" * 60)
    print("🔀 MIXED WORKFLOW TEST")
    print("=" * 60)
    
    goal = """Research the top 3 competitors in sustainable packaging, analyze their marketing strategies, 
    create a competitive positioning strategy, and generate marketing visuals for our eco-friendly 
    packaging startup 'GreenWrap'."""
    
    print(f"Goal: {goal}")
    
    try:
        workflow = await orchestrator.create_workflow_from_goal(goal)
        
        print(f"\n📋 WORKFLOW: {workflow.name}")
        print(f"Phases: {len(workflow.phases)}")
        
        # Show model selection across phases
        models_used = []
        for phase in workflow.phases:
            model = phase.model
            models_used.append(model)
            print(f"  {phase.name}: {model}")
        
        # Should show smart model selection:
        # Research → Gemini (free, huge context)
        # Analysis → Claude (reasoning)
        # Image Generation → DALL-E 3
        
        print(f"\n🤖 MODELS SELECTED: {len(set(models_used))} different models")
        for model in set(models_used):
            count = models_used.count(model)
            print(f"  {model}: {count} phase{'s' if count > 1 else ''}")
        
        # Use workflow's estimated cost
        print(f"\n💰 ESTIMATED COST: ${workflow.total_estimated_cost:.3f}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False
