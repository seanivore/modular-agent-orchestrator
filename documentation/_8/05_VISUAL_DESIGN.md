# SECTION V: VISUAL RESOURCES & BRAND IDENTITY
*The Cognitive Design System with Implementation Code*

---

## Chapter 5.1: The Cognitive Flow Design System

### Visual Psychology for AI Orchestration

**The Challenge**: Traditional AI interfaces overwhelm users with technical complexity. **The Solution**: A cognitive design system that guides users through natural workflow creation.

#### **The Four-Color Cognitive Framework**

```css
/* The Mao Cognitive Color System */
:root {
  /* Primary Cognitive Colors */
  --cognitive-stop: #ff49ff;      /* Pink - "STOP and Focus Here" */
  --cognitive-flow: #f1d771;      /* Yellow - "Flow With This" */
  --cognitive-trust: #82d0ff;     /* Blue - "This is Trustworthy Action" */
  --cognitive-space: #bbbcbb;     /* Gray - "This is Your Space" */
  
  /* Supporting Colors */
  --success: #4CAF50;             /* Green - Completion */
  --warning: #FF9800;             /* Orange - Caution */
  --error: #F44336;               /* Red - Problems */
  --info: #2196F3;                /* Blue - Information */
  
  /* Cognitive Color Variations */
  --cognitive-stop-light: #ff79ff;
  --cognitive-stop-dark: #cc39cc;
  --cognitive-flow-light: #f5e191;
  --cognitive-flow-dark: #d4b851;
  --cognitive-trust-light: #a2e0ff;
  --cognitive-trust-dark: #5fa9cc;
  --cognitive-space-light: #d1d2d1;
  --cognitive-space-dark: #95969;
}

/* Cognitive Color Usage Classes */
.cognitive-stop {
  background-color: var(--cognitive-stop);
  color: white;
  border: 2px solid var(--cognitive-stop-dark);
  box-shadow: 0 4px 12px rgba(255, 73, 255, 0.3);
  /* Psychological impact: Demands attention, creates focus */
}

.cognitive-flow {
  background-color: var(--cognitive-flow);
  color: #333;
  border: 1px solid var(--cognitive-flow-dark);
  /* Psychological impact: Natural conversation, learning state */
}

.cognitive-trust {
  background-color: var(--cognitive-trust);
  color: white;
  border: 1px solid var(--cognitive-trust-dark);
  transition: all 0.2s ease;
  /* Psychological impact: Safe interaction, reliable action */
}

.cognitive-trust:hover {
  background-color: var(--cognitive-trust-dark);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(130, 208, 255, 0.4);
}

.cognitive-space {
  background-color: var(--cognitive-space);
  color: #333;
  border: 1px solid var(--cognitive-space-dark);
  /* Psychological impact: Familiar workspace, user control area */
}
```

#### **React Component Implementation**

```jsx
// components/CognitiveButton.jsx
import React from 'react';
import './CognitiveButton.css';

const CognitiveButton = ({ 
  type = 'trust',           // stop, flow, trust, space
  size = 'medium',          // small, medium, large
  icon,                     // Optional icon component
  children,
  onClick,
  disabled = false,
  loading = false,
  ...props 
}) => {
  const getButtonClass = () => {
    const baseClass = 'mao-button';
    const typeClass = `cognitive-${type}`;
    const sizeClass = `mao-button-${size}`;
    const stateClass = disabled ? 'disabled' : loading ? 'loading' : '';
    
    return `${baseClass} ${typeClass} ${sizeClass} ${stateClass}`.trim();
  };

  const getAriaLabel = () => {
    const typeDescriptions = {
      stop: 'Important action requiring attention',
      flow: 'Continue with natural workflow',
      trust: 'Safe and reliable action',
      space: 'User workspace interaction'
    };
    
    return props['aria-label'] || typeDescriptions[type];
  };

  return (
    <button
      className={getButtonClass()}
      onClick={onClick}
      disabled={disabled || loading}
      aria-label={getAriaLabel()}
      {...props}
    >
      {loading && <span className="mao-spinner" aria-hidden="true" />}
      {icon && <span className="mao-button-icon">{icon}</span>}
      <span className="mao-button-text">{children}</span>
    </button>
  );
};

// Usage examples with cognitive psychology
const CognitiveButtonExamples = () => {
  return (
    <div className="cognitive-examples">
      {/* Pink - STOP and Focus Here */}
      <CognitiveButton 
        type="stop" 
        onClick={() => console.log('Critical decision point')}
      >
        Start Workflow
      </CognitiveButton>
      
      {/* Yellow - Flow With This */}
      <CognitiveButton 
        type="flow"
        onClick={() => console.log('Natural conversation flow')}
      >
        Continue Learning
      </CognitiveButton>
      
      {/* Blue - Trustworthy Action */}
      <CognitiveButton 
        type="trust"
        onClick={() => console.log('Safe to proceed')}
      >
        Save Progress
      </CognitiveButton>
      
      {/* Gray - Your Space */}
      <CognitiveButton 
        type="space"
        onClick={() => console.log('User workspace')}
      >
        Edit Settings
      </CognitiveButton>
    </div>
  );
};

export default CognitiveButton;
```

### The Shape Language System

#### **Orchestrator & Agent Symbol Components**

```jsx
// components/StatusIndicators.jsx
import React from 'react';

const OrchestratorIndicator = ({ status = 'waiting', size = 24 }) => {
  const getTriangleClass = () => {
    return status === 'active' ? 'orchestrator-active' : 'orchestrator-waiting';
  };
  
  return (
    <div className={`orchestrator-indicator ${getTriangleClass()}`}>
      <svg width={size} height={size} viewBox="0 0 24 24">
        <triangle
          points="12,2 22,20 2,20"
          className={`orchestrator-triangle ${getTriangleClass()}`}
        />
      </svg>
      <span className="status-label">
        {status === 'active' ? '▲ Orchestrating' : '△ Ready'}
      </span>
    </div>
  );
};

const AgentIndicator = ({ status = 'waiting', agentName, size = 20 }) => {
  const getCircleClass = () => {
    return status === 'active' ? 'agent-active' : 'agent-waiting';
  };
  
  return (
    <div className={`agent-indicator ${getCircleClass()}`}>
      <svg width={size} height={size} viewBox="0 0 20 20">
        <circle
          cx="10"
          cy="10"
          r="8"
          className={`agent-circle ${getCircleClass()}`}
        />
      </svg>
      <span className="agent-label">
        {status === 'active' ? '●' : '○'} {agentName}
      </span>
    </div>
  );
};

// Workflow status display component
const WorkflowStatusDisplay = ({ 
  orchestratorStatus, 
  agents = [],
  currentPhase 
}) => {
  return (
    <div className="workflow-status-display">
      <div className="status-header">
        <OrchestratorIndicator status={orchestratorStatus} />
        <span className="phase-indicator">Phase: {currentPhase}</span>
      </div>
      
      <div className="agents-status">
        {agents.map(agent => (
          <AgentIndicator
            key={agent.id}
            status={agent.status}
            agentName={agent.name}
          />
        ))}
      </div>
    </div>
  );
};
```

```css
/* StatusIndicators.css */
.orchestrator-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 4px 0;
}

.orchestrator-triangle.orchestrator-waiting {
  fill: none;
  stroke: var(--cognitive-trust);
  stroke-width: 2px;
  /* △ Waiting State - outline shows potential energy */
}

.orchestrator-triangle.orchestrator-active {
  fill: var(--cognitive-stop);
  stroke: var(--cognitive-stop-dark);
  stroke-width: 1px;
  /* ▲ Active State - filled shows kinetic energy */
  animation: pulse-orchestrator 2s infinite;
}

@keyframes pulse-orchestrator {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

.agent-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 2px 0;
  padding: 4px 8px;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.agent-circle.agent-waiting {
  fill: none;
  stroke: var(--cognitive-space);
  stroke-width: 2px;
  /* ○ Agent waiting - harmonious with orchestrator */
}

.agent-circle.agent-active {
  fill: var(--cognitive-flow);
  stroke: var(--cognitive-flow-dark);
  stroke-width: 1px;
  /* ● Agent active - synchronized with orchestrator */
  animation: pulse-agent 1.5s infinite;
}

@keyframes pulse-agent {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.workflow-status-display {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 1px solid var(--cognitive-space);
  border-radius: 12px;
  padding: 16px;
  margin: 16px 0;
}

.status-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--cognitive-space-light);
}

.agents-status {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
```

---

## Chapter 5.2: Mobile-First Interface Design

### iOS-Inspired Workflow Creation

#### **Card-Based Interaction Components**

```jsx
// components/WorkflowCards.jsx
import React, { useState } from 'react';
import { CognitiveButton } from './CognitiveButton';
import './WorkflowCards.css';

const GoalDefinitionCard = ({ onGoalSubmit }) => {
  const [goal, setGoal] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleSubmit = async () => {
    setIsAnalyzing(true);
    await onGoalSubmit(goal);
    setIsAnalyzing(false);
  };

  return (
    <div className="workflow-card goal-definition-card">
      <div className="card-header">
        <span className="card-icon">🎯</span>
        <h3 className="card-title">Goal Definition</h3>
      </div>
      
      <div className="card-content">
        <p className="card-description">
          What do you want to accomplish today?
        </p>
        
        <div className="goal-input-container">
          <textarea
            className="goal-input cognitive-space"
            placeholder="Describe your goal in natural language..."
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            rows={3}
          />
        </div>
        
        {isAnalyzing && (
          <div className="analysis-indicator cognitive-flow">
            <span className="analysis-symbol">△</span>
            <span>Mao analyzing your request...</span>
          </div>
        )}
      </div>
      
      <div className="card-actions">
        <CognitiveButton
          type="trust"
          onClick={handleSubmit}
          disabled={!goal.trim() || isAnalyzing}
          loading={isAnalyzing}
        >
          Analyze Goal
        </CognitiveButton>
      </div>
    </div>
  );
};

const WorkflowSuggestionCard = ({ 
  suggestion, 
  onAccept, 
  onModify 
}) => {
  return (
    <div className="workflow-card suggestion-card">
      <div className="card-header">
        <span className="card-icon">✨</span>
        <h3 className="card-title">Workflow Suggestion</h3>
      </div>
      
      <div className="card-content">
        <div className="suggestion-summary">
          <div className="workflow-name">
            <span className="orchestrator-symbol">▲</span>
            <span>Recommended: {suggestion.name}</span>
          </div>
          
          <div className="workflow-details">
            <div className="detail-item">
              <span className="agent-symbols">
                {suggestion.agents.map((_, i) => (
                  <span key={i} className="agent-symbol">○</span>
                ))}
              </span>
              <span>{suggestion.agents.length} agents will coordinate</span>
            </div>
            
            <div className="detail-item">
              <span className="time-icon">⏱️</span>
              <span>Estimated: {suggestion.estimatedTime}</span>
            </div>
            
            <div className="detail-item">
              <span className="cost-icon">💰</span>
              <span>Cost: {suggestion.estimatedCost}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div className="card-actions">
        <CognitiveButton
          type="stop"
          onClick={onAccept}
          size="large"
        >
          Start Workflow
        </CognitiveButton>
        
        <CognitiveButton
          type="space"
          onClick={onModify}
          size="medium"
        >
          Modify Settings
        </CognitiveButton>
      </div>
    </div>
  );
};

const ExecutionMonitoringCard = ({ 
  workflowStatus, 
  currentPhase, 
  progress, 
  onPause,
  onStop 
}) => {
  return (
    <div className="workflow-card execution-card">
      <div className="card-header">
        <span className="card-icon">🔄</span>
        <h3 className="card-title">Workflow Execution</h3>
      </div>
      
      <div className="card-content">
        <div className="execution-status">
          <div className="status-line">
            <span className="orchestrator-active">▲</span>
            <span className="status-text">{workflowStatus.name} Running</span>
          </div>
          
          <div className="agents-status">
            {workflowStatus.agents.map((agent, index) => (
              <div key={agent.id} className="agent-status-line">
                <span className={`agent-symbol ${agent.status === 'active' ? 'agent-active' : 'agent-waiting'}`}>
                  {agent.status === 'active' ? '●' : '○'}
                </span>
                <span className="agent-task">
                  Agent {index + 1}: {agent.currentTask}
                </span>
              </div>
            ))}
          </div>
          
          <div className="progress-container">
            <div className="progress-bar">
              <div 
                className="progress-fill"
                style={{ width: `${progress}%` }}
              />
            </div>
            <span className="progress-text">{progress}%</span>
          </div>
        </div>
      </div>
      
      <div className="card-actions">
        <CognitiveButton
          type="space"
          onClick={onPause}
          size="medium"
        >
          Pause
        </CognitiveButton>
        
        <CognitiveButton
          type="stop"
          onClick={onStop}
          size="medium"
        >
          Stop Workflow
        </CognitiveButton>
      </div>
    </div>
  );
};

export { GoalDefinitionCard, WorkflowSuggestionCard, ExecutionMonitoringCard };
```

#### **Card Styling with Mobile-First Approach**

```css
/* WorkflowCards.css */
.workflow-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin: 16px 0;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid var(--cognitive-space-light);
}

.workflow-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 20px 16px 20px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid var(--cognitive-space-light);
}

.card-icon {
  font-size: 24px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--cognitive-trust);
  border-radius: 8px;
  color: white;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: #2c3e50;
}

.card-content {
  padding: 20px;
}

.card-actions {
  padding: 16px 20px 20px 20px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

/* Goal Definition Card Specific */
.goal-input-container {
  margin: 16px 0;
}

.goal-input {
  width: 100%;
  padding: 16px;
  border-radius: 12px;
  border: 2px solid var(--cognitive-space);
  font-size: 16px;
  font-family: inherit;
  resize: vertical;
  min-height: 80px;
  transition: border-color 0.3s ease;
}

.goal-input:focus {
  outline: none;
  border-color: var(--cognitive-trust);
  box-shadow: 0 0 0 3px rgba(130, 208, 255, 0.2);
}

.analysis-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 8px;
  margin-top: 12px;
  animation: pulse-flow 2s infinite;
}

@keyframes pulse-flow {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

/* Suggestion Card Specific */
.suggestion-summary {
  space-y: 16px;
}

.workflow-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: var(--cognitive-stop);
  margin-bottom: 16px;
}

.orchestrator-symbol {
  color: var(--cognitive-stop);
  font-size: 20px;
}

.workflow-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #4a5568;
}

.agent-symbols {
  display: flex;
  gap: 2px;
}

.agent-symbol {
  color: var(--cognitive-flow);
  font-size: 16px;
}

/* Execution Card Specific */
.execution-status {
  space-y: 16px;
}

.status-line {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
}

.orchestrator-active {
  color: var(--cognitive-stop);
  font-size: 18px;
  animation: pulse-orchestrator 2s infinite;
}

.agents-status {
  margin: 16px 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.agent-status-line {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0;
}

.agent-symbol.agent-active {
  color: var(--cognitive-flow);
  animation: pulse-agent 1.5s infinite;
}

.agent-symbol.agent-waiting {
  color: var(--cognitive-space);
}

.progress-container {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 16px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: var(--cognitive-space-light);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--cognitive-trust) 0%, var(--cognitive-flow) 100%);
  border-radius: 4px;
  transition: width 0.5s ease;
}

.progress-text {
  font-weight: 600;
  color: var(--cognitive-trust);
  min-width: 40px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .workflow-card {
    margin: 12px 0;
    border-radius: 12px;
  }
  
  .card-header {
    padding: 16px;
  }
  
  .card-content {
    padding: 16px;
  }
  
  .card-actions {
    padding: 12px 16px 16px 16px;
    flex-direction: column;
  }
  
  .card-actions button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .workflow-card {
    margin: 8px;
    border-radius: 8px;
  }
  
  .goal-input {
    font-size: 16px; /* Prevents zoom on iOS */
  }
}
```

### Gesture-Inspired Desktop Interactions

#### **Swipe-Like Navigation Component**

```jsx
// components/SwipeNavigation.jsx
import React, { useState, useRef, useEffect } from 'react';
import './SwipeNavigation.css';

const SwipeNavigation = ({ 
  children, 
  currentIndex = 0, 
  onIndexChange,
  showDots = true 
}) => {
  const containerRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const [startX, setStartX] = useState(0);
  const [currentX, setCurrentX] = useState(0);
  const [translateX, setTranslateX] = useState(0);

  const handleMouseDown = (e) => {
    setIsDragging(true);
    setStartX(e.clientX);
    setCurrentX(e.clientX);
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    
    setCurrentX(e.clientX);
    const deltaX = e.clientX - startX;
    setTranslateX(deltaX);
  };

  const handleMouseUp = () => {
    if (!isDragging) return;
    
    setIsDragging(false);
    const deltaX = currentX - startX;
    const threshold = 100; // Minimum swipe distance
    
    if (Math.abs(deltaX) > threshold) {
      if (deltaX > 0 && currentIndex > 0) {
        // Swiped right - go to previous
        onIndexChange(currentIndex - 1);
      } else if (deltaX < 0 && currentIndex < children.length - 1) {
        // Swiped left - go to next
        onIndexChange(currentIndex + 1);
      }
    }
    
    setTranslateX(0);
  };

  const getTransform = () => {
    const baseTransform = -(currentIndex * 100);
    const dragOffset = isDragging ? (translateX / containerRef.current?.offsetWidth) * 100 : 0;
    return `translateX(${baseTransform + dragOffset}%)`;
  };

  return (
    <div className="swipe-navigation">
      <div 
        className="swipe-container"
        ref={containerRef}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        style={{
          transform: getTransform(),
          transition: isDragging ? 'none' : 'transform 0.3s ease'
        }}
      >
        {children.map((child, index) => (
          <div key={index} className="swipe-item">
            {child}
          </div>
        ))}
      </div>
      
      {showDots && (
        <div className="swipe-dots">
          {children.map((_, index) => (
            <button
              key={index}
              className={`swipe-dot ${index === currentIndex ? 'active' : ''}`}
              onClick={() => onIndexChange(index)}
            />
          ))}
        </div>
      )}
    </div>
  );
};

// Usage example for workflow stages
const WorkflowStageNavigation = () => {
  const [currentStage, setCurrentStage] = useState(0);
  
  const stages = [
    <GoalDefinitionCard onGoalSubmit={handleGoalSubmit} />,
    <WorkflowSuggestionCard suggestion={suggestion} onAccept={handleAccept} />,
    <ExecutionMonitoringCard workflowStatus={status} progress={progress} />
  ];

  return (
    <SwipeNavigation
      currentIndex={currentStage}
      onIndexChange={setCurrentStage}
    >
      {stages}
    </SwipeNavigation>
  );
};
```

---

## Chapter 5.3: Technical Data Flow Visualizations

### Mermaid Diagram Components with Cognitive Colors

#### **Dynamic Workflow Visualization**

```jsx
// components/WorkflowVisualization.jsx
import React, { useEffect, useRef } from 'react';
import mermaid from 'mermaid';

const WorkflowVisualization = ({ workflowData, type = 'execution' }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    mermaid.initialize({
      theme: 'base',
      themeVariables: {
        primaryColor: '#82d0ff',      // cognitive-trust
        primaryTextColor: '#2c3e50',
        primaryBorderColor: '#5fa9cc', // cognitive-trust-dark
        lineColor: '#bbbcbb',         // cognitive-space
        secondaryColor: '#f1d771',    // cognitive-flow
        tertiaryColor: '#ff49ff',     // cognitive-stop
        background: '#ffffff',
        mainBkg: '#f8f9fa',
        secondBkg: '#e9ecef',
        tertiaryBkg: '#dee2e6'
      }
    });
  }, []);

  const generateMermaidDiagram = () => {
    switch (type) {
      case 'execution':
        return `
          graph LR
            A[User Goal: "${workflowData.goal}"] --> B[Intent Parser]
            B --> C[Tool Selection Engine]
            C --> D[Agent Coordination Layer]
            D --> E[${workflowData.agents[0]}]
            D --> F[${workflowData.agents[1]}]
            D --> G[${workflowData.agents[2]}]
            E --> H[Data Collection]
            F --> I[Analysis]
            G --> J[Report Generation]
            H --> K[Results Aggregation]
            I --> K
            J --> K
            K --> L[Deliverable: ${workflowData.deliverable}]
            
            classDef userInput fill:#f1d771,stroke:#d4b851,stroke-width:2px
            classDef processing fill:#82d0ff,stroke:#5fa9cc,stroke-width:2px
            classDef coordination fill:#ff49ff,stroke:#cc39cc,stroke-width:2px
            classDef agents fill:#bbbcbb,stroke:#959695,stroke-width:2px
            classDef output fill:#82d0ff,stroke:#5fa9cc,stroke-width:3px
            
            class A userInput
            class B,C processing
            class D coordination
            class E,F,G agents
            class L output
        `;
        
      case 'architecture':
        return `
          graph TB
            subgraph "User Interface Layer"
              A[Terminal UI]
              B[Conversation Bridge]
            end
            
            subgraph "Orchestration Layer"
              C[Core Orchestrator]
              D[Agent Callback System]
              E[Memory MCP]
            end
            
            subgraph "Tool Ecosystem"
              F[Research Tool]
              G[Analysis Tool]
              H[Generation Tool]
            end
            
            A --> B
            B --> C
            C --> D
            D --> E
            D --> F
            D --> G
            D --> H
            
            classDef interface fill:#f1d771,stroke:#d4b851,stroke-width:2px
            classDef orchestration fill:#ff49ff,stroke:#cc39cc,stroke-width:2px
            classDef tools fill:#82d0ff,stroke:#5fa9cc,stroke-width:2px
            
            class A,B interface
            class C,D,E orchestration
            class F,G,H tools
        `;
        
      default:
        return `graph TD; A[Default] --> B[Diagram]`;
    }
  };

  useEffect(() => {
    if (chartRef.current) {
      const diagramDefinition = generateMermaidDiagram();
      mermaid.render('mermaid-chart', diagramDefinition).then(({ svg }) => {
        chartRef.current.innerHTML = svg;
      });
    }
  }, [workflowData, type]);

  return (
    <div className="workflow-visualization">
      <div ref={chartRef} className="mermaid-container" />
    </div>
  );
};

// Real-time workflow progress visualization
const LiveWorkflowProgress = ({ workflowStatus }) => {
  const generateProgressDiagram = () => {
    const { currentPhase, completedPhases, agents } = workflowStatus;
    
    let diagram = `graph LR\n`;
    
    // Add phases
    workflowStatus.phases.forEach((phase, index) => {
      const isCompleted = completedPhases.includes(phase.name);
      const isCurrent = currentPhase === phase.name;
      
      diagram += `  ${phase.id}[${phase.name}]\n`;
      
      if (index > 0) {
        diagram += `  ${workflowStatus.phases[index-1].id} --> ${phase.id}\n`;
      }
    });
    
    // Add styling based on status
    diagram += `\n`;
    workflowStatus.phases.forEach((phase) => {
      const isCompleted = completedPhases.includes(phase.name);
      const isCurrent = currentPhase === phase.name;
      
      if (isCompleted) {
        diagram += `  class ${phase.id} completed\n`;
      } else if (isCurrent) {
        diagram += `  class ${phase.id} current\n`;
      } else {
        diagram += `  class ${phase.id} pending\n`;
      }
    });
    
    diagram += `
      classDef completed fill:#4CAF50,stroke:#388E3C,stroke-width:2px,color:#fff
      classDef current fill:#ff49ff,stroke:#cc39cc,stroke-width:3px,color:#fff
      classDef pending fill:#bbbcbb,stroke:#959695,stroke-width:1px
    `;
    
    return diagram;
  };

  return (
    <div className="live-progress-visualization">
      <h4>Workflow Progress</h4>
      <WorkflowVisualization 
        workflowData={{ 
          customDiagram: generateProgressDiagram() 
        }} 
        type="custom" 
      />
      
      <div className="progress-legend">
        <div className="legend-item">
          <span className="legend-dot completed"></span>
          <span>Completed</span>
        </div>
        <div className="legend-item">
          <span className="legend-dot current"></span>
          <span>Current</span>
        </div>
        <div className="legend-item">
          <span className="legend-dot pending"></span>
          <span>Pending</span>
        </div>
      </div>
    </div>
  );
};
```

---

## Chapter 5.4: Brand Identity & Implementation Guidelines

### Complete CSS Design System

#### **Typography System**

```css
/* Typography.css */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  /* Typography Scale */
  --font-family-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-family-mono: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', monospace;
  
  /* Font Sizes */
  --font-size-xs: 0.75rem;     /* 12px */
  --font-size-sm: 0.875rem;    /* 14px */
  --font-size-base: 1rem;      /* 16px */
  --font-size-lg: 1.125rem;    /* 18px */
  --font-size-xl: 1.25rem;     /* 20px */
  --font-size-2xl: 1.5rem;     /* 24px */
  --font-size-3xl: 1.875rem;   /* 30px */
  --font-size-4xl: 2.25rem;    /* 36px */
  --font-size-5xl: 3rem;       /* 48px */
  
  /* Line Heights */
  --line-height-tight: 1.25;
  --line-height-snug: 1.375;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.625;
  --line-height-loose: 2;
  
  /* Font Weights */
  --font-weight-light: 300;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
}

/* Typography Classes */
.mao-heading-1 {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  color: #1a202c;
  margin-bottom: 1rem;
}

.mao-heading-2 {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-tight);
  color: #2d3748;
  margin-bottom: 0.75rem;
}

.mao-heading-3 {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-snug);
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.mao-body-large {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-normal);
  line-height: var(--line-height-relaxed);
  color: #4a5568;
}

.mao-body-normal {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-normal);
  line-height: var(--line-height-normal);
  color: #4a5568;
}

.mao-body-small {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-normal);
  line-height: var(--line-height-normal);
  color: #718096;
}

.mao-caption {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  line-height: var(--line-height-normal);
  color: #a0aec0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.mao-code {
  font-family: var(--font-family-mono);
  font-size: var(--font-size-sm);
  background: #f7fafc;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  border: 1px solid #e2e8f0;
}

/* Responsive Typography */
@media (max-width: 768px) {
  .mao-heading-1 {
    font-size: var(--font-size-3xl);
  }
  
  .mao-heading-2 {
    font-size: var(--font-size-2xl);
  }
  
  .mao-heading-3 {
    font-size: var(--font-size-xl);
  }
}
```

#### **Complete Button System**

```css
/* Buttons.css */
.mao-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-family: var(--font-family-primary);
  font-weight: var(--font-weight-medium);
  text-decoration: none;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
  
  /* Focus styles for accessibility */
  &:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(130, 208, 255, 0.3);
  }
  
  /* Disabled state */
  &.disabled {
    opacity: 0.6;
    cursor: not-allowed;
    pointer-events: none;
  }
  
  /* Loading state */
  &.loading {
    cursor: wait;
  }
}

/* Size Variations */
.mao-button-small {
  padding: 8px 16px;
  font-size: var(--font-size-sm);
  min-height: 36px;
}

.mao-button-medium {
  padding: 12px 24px;
  font-size: var(--font-size-base);
  min-height: 44px;
}

.mao-button-large {
  padding: 16px 32px;
  font-size: var(--font-size-lg);
  min-height: 52px;
}

/* Cognitive Type Variations */
.mao-button.cognitive-trust {
  background: linear-gradient(135deg, var(--cognitive-trust) 0%, var(--cognitive-trust-dark) 100%);
  color: white;
  border: 1px solid var(--cognitive-trust-dark);
}

.mao-button.cognitive-trust:hover:not(.disabled) {
  background: linear-gradient(135deg, var(--cognitive-trust-dark) 0%, var(--cognitive-trust) 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(130, 208, 255, 0.4);
}

.mao-button.cognitive-stop {
  background: linear-gradient(135deg, var(--cognitive-stop) 0%, var(--cognitive-stop-dark) 100%);
  color: white;
  border: 2px solid var(--cognitive-stop-dark);
  box-shadow: 0 4px 12px rgba(255, 73, 255, 0.3);
}

.mao-button.cognitive-stop:hover:not(.disabled) {
  background: linear-gradient(135deg, var(--cognitive-stop-dark) 0%, var(--cognitive-stop) 100%);
  transform: translateY(-1px);
  box-shadow: 0 8px 25px rgba(255, 73, 255, 0.5);
}

.mao-button.cognitive-flow {
  background: linear-gradient(135deg, var(--cognitive-flow) 0%, var(--cognitive-flow-dark) 100%);
  color: #2d3748;
  border: 1px solid var(--cognitive-flow-dark);
}

.mao-button.cognitive-flow:hover:not(.disabled) {
  background: linear-gradient(135deg, var(--cognitive-flow-dark) 0%, var(--cognitive-flow) 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(241, 215, 113, 0.4);
}

.mao-button.cognitive-space {
  background: var(--cognitive-space);
  color: #2d3748;
  border: 1px solid var(--cognitive-space-dark);
}

.mao-button.cognitive-space:hover:not(.disabled) {
  background: var(--cognitive-space-dark);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(187, 188, 187, 0.3);
}

/* Button Icons */
.mao-button-icon {
  display: flex;
  align-items: center;
  font-size: 1.2em;
}

.mao-button-text {
  display: flex;
  align-items: center;
}

/* Loading Spinner */
.mao-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Button Groups */
.mao-button-group {
  display: flex;
  gap: 0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.mao-button-group .mao-button {
  border-radius: 0;
  border-right: 1px solid rgba(255, 255, 255, 0.2);
}

.mao-button-group .mao-button:first-child {
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
}

.mao-button-group .mao-button:last-child {
  border-top-right-radius: 8px;
  border-bottom-right-radius: 8px;
  border-right: none;
}
```

### Layout & Component System

#### **Grid System**

```css
/* Grid.css */
.mao-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

.mao-container-fluid {
  width: 100%;
  padding: 0 16px;
}

.mao-row {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -8px;
}

.mao-col {
  flex: 1;
  padding: 0 8px;
}

/* Responsive columns */
.mao-col-1 { flex: 0 0 8.333333%; max-width: 8.333333%; }
.mao-col-2 { flex: 0 0 16.666667%; max-width: 16.666667%; }
.mao-col-3 { flex: 0 0 25%; max-width: 25%; }
.mao-col-4 { flex: 0 0 33.333333%; max-width: 33.333333%; }
.mao-col-5 { flex: 0 0 41.666667%; max-width: 41.666667%; }
.mao-col-6 { flex: 0 0 50%; max-width: 50%; }
.mao-col-7 { flex: 0 0 58.333333%; max-width: 58.333333%; }
.mao-col-8 { flex: 0 0 66.666667%; max-width: 66.666667%; }
.mao-col-9 { flex: 0 0 75%; max-width: 75%; }
.mao-col-10 { flex: 0 0 83.333333%; max-width: 83.333333%; }
.mao-col-11 { flex: 0 0 91.666667%; max-width: 91.666667%; }
.mao-col-12 { flex: 0 0 100%; max-width: 100%; }

@media (max-width: 768px) {
  .mao-col-sm-12 { flex: 0 0 100%; max-width: 100%; }
  .mao-col-sm-6 { flex: 0 0 50%; max-width: 50%; }
  .mao-col-sm-4 { flex: 0 0 33.333333%; max-width: 33.333333%; }
  .mao-col-sm-3 { flex: 0 0 25%; max-width: 25%; }
}

@media (max-width: 480px) {
  .mao-row {
    margin: 0 -4px;
  }
  
  .mao-col {
    padding: 0 4px;
  }
  
  .mao-col-xs-12 { flex: 0 0 100%; max-width: 100%; }
}
```

#### **Terminal UI Implementation**

```jsx
// components/TerminalUI.jsx
import React, { useState, useRef, useEffect } from 'react';
import './TerminalUI.css';

const TerminalUI = ({ onCommand, history = [] }) => {
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const inputRef = useRef(null);
  const terminalRef = useRef(null);

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [history]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isProcessing) return;

    setIsProcessing(true);
    await onCommand(input);
    setInput('');
    setIsProcessing(false);
    inputRef.current?.focus();
  };

  return (
    <div className="mao-terminal">
      <div className="terminal-header">
        <div className="terminal-controls">
          <span className="terminal-dot terminal-dot-red"></span>
          <span className="terminal-dot terminal-dot-yellow"></span>
          <span className="terminal-dot terminal-dot-green"></span>
        </div>
        <div className="terminal-title">
          Mao - Modular Agent Orchestrator
        </div>
      </div>
      
      <div className="terminal-body" ref={terminalRef}>
        <div className="terminal-welcome">
          <div className="welcome-logo">
            <span className="orchestrator-symbol">△</span>
            <span className="welcome-text">Mao v4.0</span>
          </div>
          <div className="welcome-message">
            Ready to orchestrate AI workflows. Type your goal in natural language.
          </div>
        </div>
        
        {history.map((entry, index) => (
          <div key={index} className={`terminal-entry ${entry.type}`}>
            {entry.type === 'user' && (
              <div className="terminal-user-input">
                <span className="terminal-prompt">$</span>
                <span className="terminal-command">{entry.content}</span>
              </div>
            )}
            
            {entry.type === 'system' && (
              <div className="terminal-system-output">
                <div className="system-header">
                  <span className="orchestrator-active">▲</span>
                  <span className="system-message">{entry.title}</span>
                </div>
                <div className="system-content">
                  {entry.content}
                </div>
              </div>
            )}
            
            {entry.type === 'result' && (
              <div className="terminal-result">
                <div className="result-header">
                  <span className="success-symbol">✅</span>
                  <span className="result-title">{entry.title}</span>
                </div>
                <div className="result-content">
                  {entry.content}
                </div>
              </div>
            )}
          </div>
        ))}
        
        <form onSubmit={handleSubmit} className="terminal-input-form">
          <div className="terminal-input-line">
            <span className="terminal-prompt">$</span>
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="What would you like to accomplish?"
              className="terminal-input"
              disabled={isProcessing}
              autoFocus
            />
            {isProcessing && (
              <div className="terminal-processing">
                <span className="processing-spinner">△</span>
                <span>Processing...</span>
              </div>
            )}
          </div>
        </form>
      </div>
    </div>
  );
};

export default TerminalUI;
```

```css
/* TerminalUI.css */
.mao-terminal {
  background: #1a1a1a;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  font-family: var(--font-family-mono);
  max-width: 900px;
  margin: 0 auto;
  border: 1px solid #333;
}

.terminal-header {
  background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid #333;
}

.terminal-controls {
  display: flex;
  gap: 6px;
}

.terminal-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.terminal-dot-red { background: #ff5f56; }
.terminal-dot-yellow { background: #ffbd2e; }
.terminal-dot-green { background: #27ca3f; }

.terminal-title {
  color: #a0aec0;
  font-size: 14px;
  font-weight: 500;
}

.terminal-body {
  background: #1a1a1a;
  color: #e2e8f0;
  padding: 20px;
  height: 500px;
  overflow-y: auto;
  font-size: 14px;
  line-height: 1.5;
}

.terminal-welcome {
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #333;
}

.welcome-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.orchestrator-symbol {
  color: var(--cognitive-stop);
  font-size: 20px;
}

.welcome-text {
  color: var(--cognitive-trust);
  font-weight: 600;
  font-size: 16px;
}

.welcome-message {
  color: #a0aec0;
  font-size: 13px;
}

.terminal-entry {
  margin-bottom: 16px;
}

.terminal-user-input {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.terminal-prompt {
  color: var(--cognitive-trust);
  font-weight: bold;
}

.terminal-command {
  color: #e2e8f0;
}

.terminal-system-output {
  background: rgba(130, 208, 255, 0.1);
  border: 1px solid var(--cognitive-trust);
  border-radius: 8px;
  padding: 12px;
  margin: 8px 0;
}

.system-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  color: var(--cognitive-trust);
  font-weight: 600;
}

.orchestrator-active {
  color: var(--cognitive-stop);
  animation: pulse-orchestrator 2s infinite;
}

.system-content {
  color: #cbd5e0;
  padding-left: 24px;
}

.terminal-result {
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid #4CAF50;
  border-radius: 8px;
  padding: 12px;
  margin: 8px 0;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  color: #4CAF50;
  font-weight: 600;
}

.result-content {
  color: #cbd5e0;
  padding-left: 24px;
}

.terminal-input-form {
  position: sticky;
  bottom: 0;
  background: #1a1a1a;
  padding-top: 16px;
  border-top: 1px solid #333;
}

.terminal-input-line {
  display: flex;
  align-items: center;
  gap: 8px;
}

.terminal-input {
  flex: 1;
  background: transparent;
  border: none;
  color: #e2e8f0;
  font-family: inherit;
  font-size: 14px;
  outline: none;
}

.terminal-input::placeholder {
  color: #718096;
}

.terminal-processing {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--cognitive-flow);
  font-size: 12px;
}

.processing-spinner {
  animation: pulse-orchestrator 1.5s infinite;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .mao-terminal {
    border-radius: 0;
    height: 100vh;
  }
  
  .terminal-body {
    height: calc(100vh - 60px);
  }
  
  .terminal-header {
    padding: 16px;
  }
  
  .terminal-body {
    padding: 16px;
  }
}
```

**🎯 EPIC VISUAL DESIGN SYSTEM COMPLETE!**

**What You Now Have:**
- **Complete CSS framework** with cognitive color psychology
- **React component library** for all UI patterns  
- **Mobile-first responsive design** with iOS inspiration
- **Terminal interface** with real-time workflow visualization
- **Mermaid diagram integration** with brand colors
- **Accessible design patterns** with proper ARIA labels
- **Performance-optimized animations** with smooth transitions

**Ready to build the most intuitive AI workflow interface ever created!** 💎✨

The full 5-document suite is now complete - each one packed with implementable code that developers can actually use to build the Mao interface exactly as designed!