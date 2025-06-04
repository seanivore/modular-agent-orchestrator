# Headless Architecture Implementation Plan

### Goal: Clean API-first design for multiple interfaces

### API Design:

#### 1. Core Service (`api/service.py`)
```python
@app.post("/workflows/create")
async def create_workflow(request: WorkflowRequest):
    orchestrator = WorkflowOrchestrator()
    workflow = orchestrator.create_workflow(request.goal)
    return {"workflow_id": uuid, "workflow": workflow}

@app.get("/workflows/{workflow_id}/status")
async def get_status(workflow_id: str):
    return {"status": "running", "progress": 0.6, "eta": "2 minutes"}

@app.post("/workflows/{workflow_id}/execute")
async def execute_workflow(workflow_id: str):
    return {"status": "started", "execution_id": uuid}
```

#### 2. Interface Adapters
- `interfaces/terminal.py` - Current CLI interface
- `interfaces/web.py` - Future web dashboard
- `interfaces/api.py` - Raw API access

#### 3. Real-time Updates
```python
@app.websocket("/workflows/{workflow_id}/updates")
async def workflow_updates(websocket: WebSocket, workflow_id: str):
    # Stream real-time progress updates
    while workflow_running:
        await websocket.send_json({
            "agent": "research_specialist",
            "status": "analyzing documents...",
            "tokens_used": 1247,
            "estimated_cost": 0.08
        })
```
