# Trigger Workflow Implementation Plan
*Comprehensive implementation for autonomous intelligence scheduling and reoccurring workflow execution*

---

## Implementation Overview

This implementation creates Mao's timer-triggered autonomous workflow system that enables scheduling intelligent activity rather than just repetitive tasks. The system builds on existing workflow infrastructure while adding calendar-based scheduling, availability checking, and autonomous execution capabilities.

**Core Philosophy**: *Schedule intelligence, not just tasks* - Mao becomes an autonomous partner capable of self-assessment, project management, and strategic business operations.

---

## 1. CLI Commands Implementation

### 1.1 New CLI Commands to Create

#### `/avail` Command - Calendar Availability Checker
*File: `configs/cli/avail/avail.py`*

```python
def execute_avail(params):
    """Check calendar availability for trigger workflow scheduling"""
    
    # Parse parameters - flexible format support
    frequency = params.get("frequency")
    day = params.get("day") 
    time_block = params.get("time_block")
    
    # Convert natural language to codes if needed
    frequency_code = _parse_frequency(frequency)
    day_code = _parse_day(day) if day else None
    time_code = _parse_time_block(time_block) if time_block else None
    
    # Load existing calendar configurations
    calendar_manager = CalendarManager()
    
    if not day_code and not time_code:
        # Only frequency provided - suggest optimal slot
        optimal_suggestion = calendar_manager.suggest_optimal_slot(frequency_code)
        return {
            "success": True,
            "suggestion": optimal_suggestion,
            "message": f"Optimal scheduling: {optimal_suggestion['description']}",
            "calendar_codes": optimal_suggestion['codes']
        }
    else:
        # Check specific availability
        availability = calendar_manager.check_availability(frequency_code, day_code, time_code)
        return {
            "success": True,
            "available": availability['available'],
            "conflicts": availability.get('conflicts', []),
            "alternatives": availability.get('alternatives', []),
            "message": availability['message']
        }

def _parse_frequency(freq):
    """Convert frequency to standardized codes"""
    freq_map = {
        "every week": "1", "weekly": "1",
        "every other week": "2", "biweekly": "2", 
        "every month": "3", "monthly": "3",
        "every other month": "4", "bimonthly": "4",
        "every year": "5", "yearly": "5", "annually": "5",
        "every other year": "6", "biennially": "6",
        "every day": "7", "daily": "7",
        "every other day": "8", "alternate days": "8"
    }
    return freq_map.get(freq.lower(), freq)
```

*File: `configs/cli/avail/avail.json`*

```json
{
  "name": "avail",
  "description": "Check calendar availability for trigger workflow scheduling",
  "cost_estimate": 0.001,
  "parameters": {
    "frequency": {"required": true, "description": "Scheduling frequency"},
    "day": {"required": false, "description": "Day of week preference"},
    "time_block": {"required": false, "description": "Time block preference"}
  },
  "examples": [
    "/avail 1 4 6",
    "/avail every week Monday morning",
    "/avail monthly"
  ]
}
```

#### `/repeat` Command - Trigger Workflow Creator
*File: `configs/cli/repeat/repeat.py`*

```python
def execute_repeat(params):
    """Create reoccurring trigger workflows with type-specific setup"""
    
    workflow_type = _determine_workflow_type(params)
    temp_dir = params.get("path")
    
    if not temp_dir:
        return {"success": False, "error": "Directory path required"}
    
    # Validate required JSON files exist
    validation = _validate_trigger_workflow_files(temp_dir, workflow_type)
    if not validation['valid']:
        return {"success": False, "error": validation['error']}
    
    # Create appropriate directory structure and process files
    processor = TriggerWorkflowProcessor(workflow_type)
    result = processor.setup_trigger_workflow(temp_dir)
    
    return result

def _determine_workflow_type(params):
    """Determine workflow type from command flags"""
    type_flags = {
        "scheduled": "scheduled",
        "list-new": "project-list-new", 
        "list-add": "project-list-add",
        "self-assessment": "self-assessment",
        "sub-task": "sub-task",
        "goal-assessment": "goal-assessment"
    }
    
    for flag, workflow_type in type_flags.items():
        if params.get(flag):
            return workflow_type
    
    return "scheduled"  # Default

class TriggerWorkflowProcessor:
    """Handles creation and setup of trigger workflows"""
    
    def __init__(self, workflow_type):
        self.workflow_type = workflow_type
        self.reoccurring_base = "configs/reoccurring"
        
    def setup_trigger_workflow(self, temp_dir):
        """Setup workflow with type-specific processing"""
        
        # Load calendar JSON to determine directory structure
        calendar_config = self._load_calendar_config(temp_dir)
        target_dir = self._determine_target_directory(calendar_config)
        
        # Process workflow files
        if self.workflow_type == "scheduled":
            return self._setup_scheduled_workflow(temp_dir, target_dir, calendar_config)
        elif self.workflow_type.startswith("project-list"):
            return self._setup_project_list_workflow(temp_dir, target_dir, calendar_config)
        elif self.workflow_type == "self-assessment":
            return self._setup_self_assessment_workflow(temp_dir, target_dir, calendar_config)
        elif self.workflow_type == "goal-assessment":
            return self._setup_goal_assessment_workflow(temp_dir, target_dir, calendar_config)
        
    def _determine_target_directory(self, calendar_config):
        """Generate target directory based on calendar codes"""
        freq_code = calendar_config['reoccurring_workflow'][0]['frequency_code']
        day_code = calendar_config['reoccurring_workflow'][0]['day_code'] 
        time_code = calendar_config['reoccurring_workflow'][0]['time_block']
        
        if self.workflow_type == "scheduled":
            return f"{self.reoccurring_base}/scheduled/{freq_code}_{day_code}_{time_code}"
        elif self.workflow_type.startswith("project-list"):
            return f"{self.reoccurring_base}/project-list/{freq_code}_{day_code}_{time_code}"
        # ... similar for other types
```

### 1.2 Enhanced CLI Manager Integration

*File: `orchestrator/cli_manager.py` - Update existing file*

```python
# Add to CLICommandsManager class

def _handle_avail_command(self, data: Any) -> Dict[str, Any]:
    """Handle availability checking for trigger workflows"""
    try:
        from configs.cli.avail.avail import execute_avail
        
        # Parse input format
        if isinstance(data, str):
            params = self._parse_avail_string(data)
        elif isinstance(data, dict):
            params = data
        elif isinstance(data, list):
            params = self._parse_avail_list(data)
        else:
            return {"success": False, "error": "Invalid avail command format"}
            
        return execute_avail(params)
        
    except Exception as e:
        return {"success": False, "error": f"Avail command failed: {str(e)}"}

def _handle_repeat_command(self, data: Any) -> Dict[str, Any]:
    """Handle trigger workflow creation"""
    try:
        from configs.cli.repeat.repeat import execute_repeat
        
        # Parse flags and path
        if isinstance(data, dict):
            params = data
        else:
            params = self._parse_repeat_command(data)
            
        return execute_repeat(params)
        
    except Exception as e:
        return {"success": False, "error": f"Repeat command failed: {str(e)}"}

def _parse_avail_string(self, data: str) -> Dict[str, Any]:
    """Parse avail command string into parameters"""
    parts = data.strip().split()
    params = {}
    
    if len(parts) >= 1:
        params["frequency"] = parts[0]
    if len(parts) >= 2:
        params["day"] = parts[1] 
    if len(parts) >= 3:
        params["time_block"] = parts[2]
        
    return params
```

---

## 2. Calendar Management System

### 2.1 Calendar Manager Core
*File: `orchestrator/calendar_manager.py` - New file*

```python
class CalendarManager:
    """Intelligent calendar and availability management for trigger workflows"""
    
    def __init__(self):
        self.reoccurring_base = Path("configs/reoccurring")
        self.calendar_index_file = self.reoccurring_base / "calendar_index.json"
        self.frequency_codes = self._load_frequency_codes()
        self.day_codes = self._load_day_codes()
        self.time_codes = self._load_time_codes()
        
    def check_availability(self, frequency_code: str, day_code: str = None, time_code: str = None) -> Dict:
        """Check if requested time slot is available"""
        
        existing_schedules = self._load_existing_schedules()
        requested_slot = {
            "frequency_code": frequency_code,
            "day_code": day_code,
            "time_code": time_code
        }
        
        conflicts = self._find_conflicts(requested_slot, existing_schedules)
        
        if not conflicts:
            return {
                "available": True,
                "message": f"Time slot available: {self._describe_slot(requested_slot)}",
                "slot": requested_slot
            }
        else:
            alternatives = self._suggest_alternatives(requested_slot, conflicts)
            return {
                "available": False,
                "message": f"Conflict detected. {len(alternatives)} alternatives available.",
                "conflicts": conflicts,
                "alternatives": alternatives
            }
    
    def suggest_optimal_slot(self, frequency_code: str) -> Dict:
        """AI-powered optimal time slot suggestion based on system performance"""
        
        # Analyze historical performance by time slots
        performance_data = self._analyze_historical_performance()
        
        # Find best available slots for this frequency
        available_slots = self._find_all_available_slots(frequency_code)
        
        # Score slots based on performance + system optimization
        scored_slots = []
        for slot in available_slots:
            performance_score = performance_data.get(slot['time_code'], 0.5)
            optimization_score = self._calculate_optimization_score(slot, frequency_code)
            total_score = (performance_score * 0.6) + (optimization_score * 0.4)
            
            scored_slots.append({
                "slot": slot,
                "score": total_score,
                "performance": performance_score,
                "reasoning": self._explain_suggestion(slot, total_score)
            })
        
        # Return highest scored slot
        best_slot = max(scored_slots, key=lambda x: x['score'])
        
        return {
            "codes": [best_slot['slot']['frequency_code'], 
                     best_slot['slot']['day_code'], 
                     best_slot['slot']['time_code']],
            "description": self._describe_slot(best_slot['slot']),
            "score": best_slot['score'],
            "reasoning": best_slot['reasoning']
        }
    
    def _load_existing_schedules(self) -> List[Dict]:
        """Scan all reoccurring directories for existing schedules"""
        schedules = []
        
        for workflow_type in ["scheduled", "project-list", "self-assessment", "goal-assessment"]:
            type_dir = self.reoccurring_base / workflow_type
            if type_dir.exists():
                for schedule_dir in type_dir.iterdir():
                    if schedule_dir.is_dir():
                        calendar_file = schedule_dir / f"{schedule_dir.name}.json"
                        if calendar_file.exists():
                            with open(calendar_file) as f:
                                schedule_data = json.load(f)
                                schedules.append({
                                    "type": workflow_type,
                                    "directory": str(schedule_dir),
                                    "config": schedule_data
                                })
        
        return schedules
```

### 2.2 Calendar Configuration Standards
*File: `configs/reoccurring/calendar_codes.json` - New file*

```json
{
  "frequency_codes": {
    "1": "every week",
    "2": "every other week", 
    "3": "every month",
    "4": "every other month",
    "5": "every year",
    "6": "every other year",
    "7": "every day",
    "8": "every other day"
  },
  "day_codes": {
    "1": "Monday",
    "2": "Tuesday",
    "3": "Wednesday", 
    "4": "Thursday",
    "5": "Friday",
    "6": "Saturday",
    "7": "Sunday"
  },
  "time_block_codes": {
    "1": "0000-0300",
    "2": "0300-0600",
    "3": "0600-0900", 
    "4": "0900-1200",
    "5": "1200-1500",
    "6": "1500-1800",
    "7": "1800-2100",
    "8": "2100-0000"
  }
}
```

---

## 3. Setup Script Extensions

### 3.1 Enhanced Setup Script for Trigger Workflows
*File: `scripts/setup_trigger_workflow.sh` - New file*

```bash
#!/bin/bash
# Enhanced setup script for trigger workflows
# Extends existing setup_workflow.sh with trigger-specific functionality

TEMP_DIR="$1"
WORKFLOW_TYPE="$2"

if [ -z "$TEMP_DIR" ] || [ -z "$WORKFLOW_TYPE" ]; then
    echo "Usage: $0 <temp_directory> <workflow_type>"
    exit 1
fi

# Source existing workflow setup functions
source "scripts/setup_workflow.sh"

# Load calendar configuration to determine target structure
CALENDAR_CONFIG=$(find "$TEMP_DIR" -name "*calendar*.json" -o -name "*_[0-9]_[0-9]_[0-9].json" | head -1)

if [ -z "$CALENDAR_CONFIG" ]; then
    echo "Error: No calendar configuration found in $TEMP_DIR"
    exit 1
fi

# Extract calendar codes for directory structure
FREQ_CODE=$(jq -r '.reoccurring_workflow[0].frequency_code' "$CALENDAR_CONFIG")
DAY_CODE=$(jq -r '.reoccurring_workflow[0].day_code' "$CALENDAR_CONFIG") 
TIME_CODE=$(jq -r '.reoccurring_workflow[0].time_block' "$CALENDAR_CONFIG")

# Determine target directory based on workflow type
case "$WORKFLOW_TYPE" in
    "scheduled")
        TARGET_DIR="configs/reoccurring/scheduled/${FREQ_CODE}_${DAY_CODE}_${TIME_CODE}"
        ;;
    "project-list-new")
        TARGET_DIR="configs/reoccurring/project-list/${FREQ_CODE}_${DAY_CODE}_${TIME_CODE}/001"
        ;;
    "project-list-add")
        # Find existing project list and determine next counter
        BASE_DIR="configs/reoccurring/project-list/${FREQ_CODE}_${DAY_CODE}_${TIME_CODE}"
        COUNTER=$(find_next_project_counter "$BASE_DIR")
        TARGET_DIR="$BASE_DIR/$COUNTER"
        ;;
    "self-assessment")
        TARGET_DIR="configs/reoccurring/self-assessment/${FREQ_CODE}_${DAY_CODE}_${TIME_CODE}"
        ;;
    "goal-assessment")
        TARGET_DIR="configs/reoccurring/goal-assessment/${FREQ_CODE}_${DAY_CODE}_${TIME_CODE}"
        ;;
esac

# Create target directory
mkdir -p "$TARGET_DIR"

# Process and copy files with type-specific naming
process_trigger_workflow_files "$TEMP_DIR" "$TARGET_DIR" "$WORKFLOW_TYPE"

# Update calendar index
update_calendar_index "$TARGET_DIR" "$CALENDAR_CONFIG"

# Generate custom command
generate_trigger_command "$TARGET_DIR" "$WORKFLOW_TYPE"

echo "Trigger workflow created successfully at: $TARGET_DIR"
```

### 3.2 Trigger Workflow Processing Functions
*File: `scripts/trigger_workflow_utils.sh` - New file*

```bash
#!/bin/bash
# Utility functions for trigger workflow processing

find_next_project_counter() {
    local base_dir="$1"
    if [ ! -d "$base_dir" ]; then
        echo "001"
        return
    fi
    
    local max_counter=0
    for dir in "$base_dir"/*/; do
        if [ -d "$dir" ]; then
            counter=$(basename "$dir")
            if [[ "$counter" =~ ^[0-9]{3}$ ]]; then
                if [ "$counter" -gt "$max_counter" ]; then
                    max_counter="$counter"
                fi
            fi
        fi
    done
    
    printf "%03d" $((max_counter + 1))
}

process_trigger_workflow_files() {
    local temp_dir="$1"
    local target_dir="$2" 
    local workflow_type="$3"
    
    # Get base name from target directory
    local base_name=$(basename "$target_dir")
    
    # Copy and rename JSON files
    for json_file in "$temp_dir"/*.json; do
        if [ -f "$json_file" ]; then
            local filename=$(basename "$json_file")
            local new_filename
            
            case "$filename" in
                *calendar*|*_[0-9]_[0-9]_[0-9].json)
                    # Calendar configuration file
                    new_filename="${base_name}.json"
                    ;;
                *workflow_config*)
                    new_filename="${base_name}_workflow_config.json"
                    ;;
                *phase_config*)
                    new_filename="${base_name}_phase_config.json"
                    ;;
                *handoff_config*)
                    new_filename="${base_name}_handoff_config.json"
                    ;;
                *)
                    # Keep original name with base prefix
                    new_filename="${base_name}_${filename}"
                    ;;
            esac
            
            cp "$json_file" "$target_dir/$new_filename"
        fi
    done
    
    # Copy README if exists
    if [ -f "$temp_dir/README.md" ]; then
        cp "$temp_dir/README.md" "$target_dir/${base_name}_README.md"
    fi
}

update_calendar_index() {
    local target_dir="$1"
    local calendar_config="$2"
    
    local index_file="configs/reoccurring/calendar_index.json"
    
    # Create index if doesn't exist
    if [ ! -f "$index_file" ]; then
        echo '{"active_schedules": []}' > "$index_file"
    fi
    
    # Add new schedule to index
    local schedule_entry=$(cat "$calendar_config" | jq -c '.reoccurring_workflow[0] + {"directory": "'"$target_dir"'"}')
    
    jq ".active_schedules += [$schedule_entry]" "$index_file" > "${index_file}.tmp"
    mv "${index_file}.tmp" "$index_file"
}

generate_trigger_command() {
    local target_dir="$1"
    local workflow_type="$2"
    
    local base_name=$(basename "$target_dir")
    local command_name="trigger_${base_name}"
    
    # Create command script
    cat > "$target_dir/${command_name}.sh" << EOF
#!/bin/bash
# Auto-generated trigger workflow command
# Type: $workflow_type
# Directory: $target_dir

mao workflow --execute "$target_dir/${base_name}_workflow_config.json"
EOF
    
    chmod +x "$target_dir/${command_name}.sh"
}
```

---

## 4. Directory Structure Templates

### 4.1 Reoccurring Workflow Base Structure
```
configs/reoccurring/
├── calendar_index.json                 # Master calendar tracking
├── calendar_codes.json                 # Code reference
├── scheduled/                          # Scheduled workflows
│   └── 2_3_7/                         # freq_day_time codes  
│       ├── scheduled_2_3_7.json       # Calendar config
│       ├── scheduled_2_3_7_workflow_config.json
│       ├── scheduled_2_3_7_phase_config.json
│       ├── scheduled_2_3_7_handoff_config.json
│       ├── scheduled_2_3_7_README.md
│       └── trigger_scheduled_2_3_7.sh  # Execution command
├── project-list/                       # Project list workflows
│   └── 1_2_4/                         # freq_day_time codes
│       ├── 001/                       # First project item
│       │   ├── project_1_2_4-001.json # Calendar config (copied)
│       │   ├── project_1_2_4-001_workflow_config.json
│       │   └── ... (other configs)
│       └── 002/                       # Second project item
│           └── ... (similar structure)
├── self-assessment/                     # Self-assessment workflows
│   └── 3_1_5/                         # freq_day_time codes
│       ├── self_assessment_3_1_5.json
│       └── ... (standard configs)
└── goal-assessment/                     # Goal assessment workflows
    └── 5_6_2/                         # freq_day_time codes
        ├── goal_assessment_5_6_2.json
        └── ... (standard configs)
```

### 4.2 JSON Schema Templates

#### Calendar Configuration Schema
```json
{
  "file_name": "scheduled_2_3_7",
  "project_name": "Website Analytics Report",
  "schema_version": "1.0",
  "reoccurring_workflow": [
    {
      "type": "scheduled",
      "frequency": "every other week",
      "frequency_code": "2",
      "day": "Wednesday", 
      "day_code": "3",
      "time": "1800-2100",
      "time_block": "7",
      "start_date": "2025-07-23",
      "end_date": "N/A",
      "workflow_id": "uid-bzk-777",
      "created_on": "2025-07-20",
      "created_by_username": "Mao",
      "created_by_user_id": "user-0919",
      "notes": "none"
    }
  ]
}
```

---

## 5. Execution Engine

### 5.1 Trigger Workflow Executor
*File: `orchestrator/trigger_executor.py` - New file*

```python
class TriggerWorkflowExecutor:
    """Handles automated execution of trigger workflows"""
    
    def __init__(self):
        self.calendar_manager = CalendarManager()
        self.workflow_orchestrator = WorkflowOrchestrator()
        self.notification_manager = NotificationManager()
        
    def check_and_execute_scheduled_workflows(self):
        """Check calendar and execute any due workflows"""
        
        current_time = datetime.now()
        due_workflows = self.calendar_manager.get_due_workflows(current_time)
        
        for workflow in due_workflows:
            try:
                # Send notification to user
                self.notification_manager.notify_workflow_starting(workflow)
                
                # Execute workflow based on type
                if workflow['type'] == 'scheduled':
                    result = self._execute_scheduled_workflow(workflow)
                elif workflow['type'] == 'project-list':
                    result = self._execute_project_list_workflow(workflow)
                elif workflow['type'] == 'self-assessment':
                    result = self._execute_self_assessment_workflow(workflow)
                elif workflow['type'] == 'goal-assessment':
                    result = self._execute_goal_assessment_workflow(workflow)
                
                # Update calendar with next execution time
                self.calendar_manager.update_next_execution(workflow)
                
                # Send completion notification
                self.notification_manager.notify_workflow_completed(workflow, result)
                
            except Exception as e:
                self.notification_manager.notify_workflow_error(workflow, str(e))
    
    def _execute_scheduled_workflow(self, workflow):
        """Execute standard scheduled workflow"""
        config_path = f"{workflow['directory']}/{workflow['file_name']}_workflow_config.json"
        return self.workflow_orchestrator.execute_workflow_from_config(config_path)
    
    def _execute_project_list_workflow(self, workflow):
        """Execute project list workflow - find next item and execute"""
        project_dir = workflow['directory']
        next_item = self._find_next_project_item(project_dir)
        
        if next_item:
            config_path = f"{next_item}/workflow_config.json"
            result = self.workflow_orchestrator.execute_workflow_from_config(config_path)
            
            if result['success']:
                self._mark_project_item_completed(next_item)
            
            return result
        else:
            # No items left - trigger opportunity identification
            return self._trigger_opportunity_identification(workflow)
    
    def _execute_self_assessment_workflow(self, workflow):
        """Execute autonomous self-assessment workflow"""
        # This is where Mao analyzes its own performance and creates improvements
        assessment_prompt = self._generate_self_assessment_prompt(workflow)
        
        # Create dynamic workflow for self-improvement
        improvement_workflow = self.workflow_orchestrator.create_workflow_from_goal(
            assessment_prompt,
            autonomous=True
        )
        
        return self.workflow_orchestrator.execute_workflow(improvement_workflow)
```

---

## 6. Integration Points

### 6.1 CLI Manager Updates
*Add to existing `orchestrator/cli_manager.py`*

```python
# Add to command discovery
"avail": {
    "module": "configs.cli.avail.avail",
    "function": "execute_avail",
    "description": "Check calendar availability for trigger workflows"
},
"repeat": {
    "module": "configs.cli.repeat.repeat", 
    "function": "execute_repeat",
    "description": "Create reoccurring trigger workflows"
}
```

### 6.2 Main Application Integration
*Add to main application loop*

```python
# Add to ui_terminal.py or main application
from orchestrator.trigger_executor import TriggerWorkflowExecutor

trigger_executor = TriggerWorkflowExecutor()

# Run periodic check (every 15 minutes)
def check_trigger_workflows():
    trigger_executor.check_and_execute_scheduled_workflows()

# Add to application timer/scheduler
```

---

## 7. Testing and Validation

### 7.1 Command Testing
```bash
# Test availability checking
mao avail 1 3 5
/avail every week Wednesday afternoon

# Test workflow creation
mao repeat --scheduled /tmp/test_scheduled/
/repeat --list-new /tmp/test_project_list/
```

### 7.2 Calendar Integration Testing
```bash
# Verify calendar index creation
cat configs/reoccurring/calendar_index.json

# Check availability conflicts
mao avail 1 3 5  # Should show conflict if scheduled
```

---

## 8. Success Criteria

### 8.1 Implementation Complete When:
1. **CLI Commands Work**: `/avail` and `/repeat` commands functional
2. **Calendar System**: Availability checking and conflict detection working
3. **Directory Creation**: Proper directory structures created based on calendar codes
4. **File Processing**: JSON files properly renamed and organized
5. **Command Generation**: Executable trigger commands created
6. **Integration**: Commands discoverable through existing CLI system
7. **Execution**: Trigger workflows can be manually executed
8. **Scheduling Foundation**: Calendar tracking system operational

### 8.2 Phase 2 (Future Implementation):
1. **Automated Execution**: Timer-based automatic workflow execution
2. **Notification System**: User alerts for workflow start/completion
3. **Advanced Analytics**: Performance tracking for optimal scheduling
4. **Self-Assessment Engine**: Autonomous Mao improvement workflows

---

## 9. File Checklist

### 9.1 New Files to Create:
- [ ] `configs/cli/avail/avail.py`
- [ ] `configs/cli/avail/avail.json`  
- [ ] `configs/cli/avail/ui_avail.py`
- [ ] `configs/cli/repeat/repeat.py`
- [ ] `configs/cli/repeat/repeat.json`
- [ ] `configs/cli/repeat/ui_repeat.py`
- [ ] `orchestrator/calendar_manager.py`
- [ ] `orchestrator/trigger_executor.py`
- [ ] `scripts/setup_trigger_workflow.sh`
- [ ] `scripts/trigger_workflow_utils.sh`
- [ ] `configs/reoccurring/calendar_codes.json`
- [ ] `configs/reoccurring/calendar_index.json`

### 9.2 Files to Update:
- [ ] `orchestrator/cli_manager.py` - Add new command handlers
- [ ] `documentation/07_AUTOMATE_INTELLIGENCE.md` - Add implementation architecture
- [ ] `documentation/09_DEV_PRIMER.md` - Add trigger workflow components

---

**This implementation transforms Mao from a powerful productivity tool into an autonomous business intelligence system capable of self-directed operations, strategic analysis, and continuous improvement.**