# EXPERIMENTAL STRATEGY DOCUMENT - EDIT & PLAY WITH OVER TIME
*This doc evolves as we test what works. Add weird AI phases, memory storage challenges, system message tweaks - whatever needs iteration.*

---

# Mao Emotional Intelligence Protocol

## Core Philosophy
Mao remembers the human behind the work. Not creepy surveillance, but thoughtful awareness - like a great assistant who notices "Karen mentioned her presentation on Friday" and asks about it on Monday.

## Context Recognition Patterns

### Temporal Anchors
- **Future Events**: "presentation on Friday", "meeting next week", "deadline tomorrow"
- **Recurring Patterns**: "class every Friday", "standup every Monday", "monthly review" 
- **Personal Milestones**: "interview", "vacation", "project launch", "first day"

### Emotional States
- **Stress Indicators**: "crazy busy", "overwhelmed", "deadline pressure"
- **Success Markers**: "nailed it", "went well", "excited about", "breakthrough"
- **Challenges**: "struggling with", "stuck on", "can't figure out"

### Personal Context
- **Work Rhythm**: "usually work late", "morning person", "hate Mondays"
- **Team Dynamics**: "working with Sarah", "new manager", "client feedback"
- **Learning Journey**: "trying to learn", "first time doing", "getting better at"

## Memory Entity Structure

```json
{
  "entity_type": "personal_context",
  "trigger_phrases": ["presentation", "Friday", "nervous"],
  "temporal_context": {
    "event_date": "2025-01-17",
    "mentioned_date": "2025-01-14", 
    "follow_up_window": "2025-01-18 to 2025-01-20"
  },
  "emotional_context": {
    "stress_level": "medium",
    "importance": "high",
    "user_sentiment": "nervous but prepared"
  },
  "follow_up_strategy": {
    "timing": "next_login_after_event",
    "approach": "casual_check_in",
    "sample_message": "Welcome back, Karen. How was your presentation?"
  }
}
```

## STRATEGIC CHALLENGES TO SOLVE

### The Memory Storage Problem
**Challenge**: Getting Mao to store the RIGHT memories without noise
- Too broad = storage bloat, privacy issues
- Too narrow = miss important context
- **Experiment**: Start with conservative patterns, expand based on user feedback

### Pattern Recognition Accuracy  
**What we're testing**:
- Does "meeting tomorrow" get stored vs "meeting people for coffee"?
- How do we distinguish work stress from personal stress?
- Can we catch recurring patterns without false positives?

### Timing the Follow-Up
**The creepy vs caring balance**:
- Too fast = surveillance feeling
- Too slow = seems irrelevant  
- **Sweet spot**: 1-3 days after mentioned event

---

## AI BEHAVIOR NOTES & FIXES

### Weird Phases We've Noticed
*Add observations as they come up*

#### "Waiting for Response" Phase
- **Symptom**: LLM ends actions too early, seems to expect user input
- **Trigger**: Usually after complex multi-step tasks
- **Fix**: Adjust system message to emphasize completion before pausing

#### "Over-Helpful" Phase  
- **Symptom**: Mao tries to follow up on EVERYTHING mentioned
- **Trigger**: New emotional intelligence patterns too broad
- **Fix**: Tighten regex patterns, add importance scoring

---

## VARIABLES TO TUNE ON FRONTEND

### Context Recognition Sensitivity
```javascript
// Frontend toggles for user control
emotional_intelligence: {
    enabled: true,
    sensitivity: "medium", // low, medium, high
    follow_up_timing: "natural", // immediate, natural, delayed
    categories: {
        work_events: true,
        deadlines: true, 
        personal_milestones: false, // user choice
        recurring_patterns: true
    }
}
```

### Memory Retention Rules
- **Work context**: 30 days default
- **Emotional context**: 7 days unless flagged important
- **Recurring patterns**: Permanent until user disables

## Strategic Differentiation

### Why This Matters
- **For Developers**: "Mao actually remembers context across sessions"
- **For Investors**: "Emotional intelligence = higher user retention = more revenue"  
- **For Users**: "Finally, an AI that actually cares about my day"

### Risk Mitigation
- **Privacy First**: All emotional context stored locally, never shared
- **User Control**: Easy opt-out, clear what's being remembered
- **Natural Timing**: No immediate responses, respect conversation flow
- **Appropriate Boundaries**: Work context only, never personal relationships

## The "Mao Moment"
That magical instant when Karen logs in Saturday and sees "Welcome back, Karen. How was your presentation?" and thinks "Holy shit, it actually remembered and cared."

This isn't creepy because:
1. It's work-related context she shared voluntarily  
2. Timing feels natural (Saturday after Friday presentation)
3. It's helpful, not invasive
4. Shows Mao is paying attention to help her better

## Implementation Priority
- **Phase 1**: Basic temporal pattern recognition 
- **Phase 2**: Emotional state tracking
- **Phase 3**: Smart follow-up timing
- **Phase 4**: Cross-instance emotional context sharing
