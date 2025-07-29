# Database Implementation for Experimental Intelligence
*v4.1.0 - Data infrastructure that serves experimentation, not just storage*

## Core Philosophy: USE Before SAVE

**Primary Goal**: Support live experimental protocol adjustment
**Secondary Goal**: Store data efficiently for analysis
**Anti-Pattern**: "Save all the data" without clear usage strategy

## Data We Actually Need

### 1. Protocol Effectiveness Metrics
**What**: Did the experimental protocol work?
- User commented positively on greeting: `YES/NO`
- Session length after contextual greeting: `duration_seconds`
- User mentioned the greeting in conversation: `YES/NO`
- Return frequency after good greetings: `days_between_sessions`

**How we use it**: Adjust protocol sensitivity, timing, patterns

### 2. Pattern Recognition Accuracy
**What**: Are we catching the right context?
- Detected temporal anchor: `presentation_friday`
- User confirmed event happened: `YES/NO/UNKNOWN`
- Follow-up was relevant: `YES/NO`
- False positive rate: `percentage`

**How we use it**: Refine regex patterns, add context categories

### 3. User Preference Learning
**What**: What works for THIS specific user?
- Preferred follow-up timing: `immediate/natural/delayed`
- Context categories they respond to: `work_events/deadlines/personal`
- Greeting style preference: `formal/casual/contextual`

**How we use it**: Personalize protocol for individual users

## Database Architecture

### Experimental Results Table
```sql
CREATE TABLE protocol_experiments (
    id UUID PRIMARY KEY,
    user_id VARCHAR(255),
    experiment_type VARCHAR(100), -- 'emotional_intelligence', 'proactive_suggestions'
    protocol_version VARCHAR(50), -- 'ei_v1.2', 'ei_v1.3'
    trigger_detected TEXT, -- "presentation on Friday"
    action_taken TEXT, -- "Welcome back, Karen. How was your presentation?"
    user_reaction ENUM('positive', 'negative', 'neutral', 'unknown'),
    success_metrics JSONB, -- {session_length: 480, mentioned_greeting: true}
    timestamp TIMESTAMP,
    follow_up_needed BOOLEAN
);
```

### User Context Memory
```sql
CREATE TABLE user_context (
    id UUID PRIMARY KEY,
    user_id VARCHAR(255),
    category VARCHAR(100), -- 'personal_context', 'emotional_context', 'recurring_patterns'
    content TEXT,
    trigger_phrases JSONB,
    temporal_data JSONB, -- {event_date: '2025-01-17', follow_up_window: '2025-01-18 to 2025-01-20'}
    importance_score FLOAT,
    retention_days INTEGER,
    created_at TIMESTAMP,
    last_accessed TIMESTAMP,
    access_count INTEGER
);
```

### Protocol Adjustments Log
```sql
CREATE TABLE protocol_adjustments (
    id UUID PRIMARY KEY,
    experiment_type VARCHAR(100),
    previous_config JSONB,
    new_config JSONB,
    reason TEXT, -- "Too many false positives", "Users requesting more sensitivity"
    user_feedback_sample TEXT,
    effectiveness_change FLOAT, -- +15% success rate
    timestamp TIMESTAMP
);
```

## Usage-First Analytics

### Real-Time Protocol Tuning
```python
# Check if current protocol is working
def should_adjust_protocol(experiment_type: str) -> Dict:
    recent_results = query_recent_experiments(experiment_type, days=7)
    
    if recent_results['success_rate'] < 0.6:
        return {
            'action': 'reduce_sensitivity',
            'reason': 'Too many false positives',
            'adjustment': 'Tighten regex patterns'
        }
    
    if recent_results['user_complaints'] > 0.1:
        return {
            'action': 'increase_timing_delay', 
            'reason': 'Users finding it creepy',
            'adjustment': 'Wait longer for follow-ups'
        }
    
    return {'action': 'no_change', 'reason': 'Protocol performing well'}
```

### User-Specific Optimization
```python
# Personalize protocol for individual user
def optimize_user_protocol(user_id: str) -> Dict:
    user_history = get_user_experiment_history(user_id)
    
    preferences = {
        'timing': analyze_timing_preference(user_history),
        'sensitivity': analyze_sensitivity_preference(user_history),
        'categories': analyze_category_preferences(user_history)
    }
    
    return generate_personalized_protocol(preferences)
```

## Implementation Priority

### Phase 1: Basic Experiment Tracking
- Track protocol effectiveness metrics
- Simple success/failure classification
- Manual protocol adjustment based on weekly reviews

### Phase 2: Automated Pattern Recognition
- Detect when protocols need adjustment
- Automated A/B testing setup
- Real-time sensitivity tuning

### Phase 3: Personalized Intelligence
- Individual user preference learning
- Dynamic protocol customization
- Cross-user pattern sharing (privacy-compliant)

### Phase 4: Advanced Analytics
- Predictive protocol effectiveness
- Multi-experiment coordination
- Advanced privacy-preserving analytics

## Privacy & Ethics

### Data Minimization
- Only store data that directly improves user experience
- Automatic deletion of emotional context after retention period
- User control over what gets remembered

### Consent & Control
- Clear opt-in for experimental protocols
- Easy disable for any category
- User can review and delete their context data

### Cross-User Learning
- Aggregate patterns only (no individual data sharing)
- Differential privacy for shared insights
- No personal context shared between users

## Success Metrics

### We Know It's Working When:
- Protocol adjustment cycles get shorter (faster optimization)
- User satisfaction with greetings increases month-over-month
- False positive rates decrease as patterns improve
- Individual user Mao instances become noticeably better at context

### Red Flags:
- Users asking "how do you know that?" (privacy concern)
- Decreasing session lengths after contextual greetings
- Increasing opt-out rates for experimental features