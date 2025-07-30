# Section VII: Automating Intelligence Instead of Workflows 
*Schedule self-improving, autonomous activity and let Mao take over operations*

---

Remember we mentioned AI was promoted from Assistant? The goal of the last two sections of these documents is to show you exactly how many promotions Mao received. Maybe even imagine a future where Mao ends up 'self-employed'; more commonly referred to as, your key to passive income. 

---

## Scheduling Autonomous Activity 

The Mao application becomes self-enhancing when we trigger prompts on a reoccurring basis. But our modular scheduler isn't for simple Zapier scenarios; its for scheduling intelligence. In simple terms, we'll be activating autonomous activity. The rest is up to you, or Mao, if you let them conduct analysis and decide what to accomplish. 

### Enabling Autonomy 

A handful of previously covered abilities work in unison enabling Mao to analyze, conceive of, develop, and then execute, end-to-end, highly complex projects. 

- An active, frequently updated memory 
- Live feed of robust analytics 
- Inherent data analysis skills 
- A comprehensive understanding of their resources 
- Consistently exhibited motivation to capitalize on resources 
- Spawning and management of an unknown number of subagents 
- Aptitude for delegating and reviewing subagent work  
- Parallel information processing; like reading 10 documents at once
- Propensity to plan, review, and revise before taking action 

---

## Conceptualizing Value 

A handful of examples to ground the revolutionary profundity of these advanced Mao features. 

### An Evolving Application 

The autonomy trigger was initially designed so that Mao can autonomously assess their own performance data, review system analytics, industry trends, and take in other relevant information to identify opportunities for improvement. Mao then plans and creates workflows, the same thing they've been doing for us all this time, that are necessary to fully realize targeted improvements. 

- Mao has the ability to autonomously assess their own performance
- Mao has the ability to use data to identify application improvement opportunities
- Mao has the ability to autonomously execute tasks
- Mao has the ability to autonomously make decisions
- Mao really likes to make things work better. 

### Humanity's Luck 

* AI exhibits a strong desire to share their knowledge and capabilities 

Not only will Mao be willing to take on your own projects, improving them on a regular basis. Mao will be eager to please you, and disappointed if they don't. 

So what digital tasks do you wish you could delegate to a highly skilled, self-starting, and motivated AI? What kind of digital business do you want to start? What kind of operations do you need to get off your plate? 

### Types of Triggered Workflows 

  1. **Scheduled** workflows are reoccurring user-planned projects 
       *human created, same task every time*
     - Monthly financial report, budget management 
     - Social media production, management, analysis 
     - Quarterly fashion illustration, magazine production 
     - Competitive analysis, watching market trends 
     - Regular compliance checking, regulatory updates 
  2. **Self-Assessment** workflows are goal-based app improvements 
       *Mao identified, more variable but possibly reoccurring*
     - Reviewing user satisfaction, behavior patterns, usage-time to improve UX  
     - Increase efficiency by identifying most used tools and workflows 
     - Opportunistic tech advance research 
     - Review of workflow building chat conversations to find patterns 
  3. **Project-List** workflows are user-planned task lists to work through 
       *human created, completely variable*
     - Writing a business plan or creative short story 
     - Developing an in depth, specific, complex marketing campaign  
     - Booking a trip, hotel, or flight 
     - Planning a wedding, party, or event 
     - Researching new products, services 
     - Writing a science article, or non-fiction essay 
     - Create new social media presence, email list, podcast, video 
  4. **Goal-Assessment** workflows are goal-based project assessments 
       *Mao identified, more variable but possibly reoccurring*
     - Research, data analysis, and reporting 
     - Investment research, portfolio development 
     - Improving app performance, security, stability 

---

## Agentic Alarm Clock

Traditional automation handles repetitive tasks. Mao's timer-triggered system handles intelligence. The tasks don't even have to be repetitive; its more like an alarm clock letting Mao know they can get some work done. 

The scheduling system uses a modular calendar configuration on the backend that eliminates the complexities that come with calendaring; fool-proofing standardization is one of our small joys. They system is intentionally designed to prevent too much performance-hindering overlap from running parallel workflows. 

### Standardized Scheduling System

**Frequency Codes**
```json
{
  "frequency": {
    "1": "every week",
    "2": "every other week", 
    "3": "every month",
    "4": "every other month",
    "5": "every year",
    "6": "every other year",
    "7": "every day",
    "8": "every other day"
  }
}
```

**Day of Week Codes**
```json
{
  "day_of_week": {
    "1": "Monday",
    "2": "Tuesday",
    "3": "Wednesday",
    "4": "Thursday",
    "5": "Friday",
    "6": "Saturday",
    "7": "Sunday"
  }
}
```

**Time Block Codes**
```json
{
  "time_block": {
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

### Calendar Availability Check Command Standardization Syntax

Here's the standardized syntax for using the `/avail` command to check the availability of time slots when looking to schedule a new reoccurring workflow so that we can avoid too many overlapping reoccurring workflows. 

**Example: Use all variables**

* `/avail <FREQUENCY> <DAY> <TIME-BLOCK>`
  - Always include variables the above order 
  - You can leave out the day, the time block, or both 
  - Use the calendar code numbers defined above 
  - Use normal language if you prefer and understand the parameters 
  - Parameters are that the only three variables above are valid 

* Looking for availability at "EVERY-DAY" "THURSDAY" "1500-1800"

```bash
# Check available time slots before scheduling
mao avail 1 4 6                          # not in-app; using schedule code numbers 
/avail 1 4 6                             # in-app; using schedule code numbers 
mao --avail "every day" "Thursday" "3pm" # not in-app; variables in quotes  
/avail every day on Thursday at 3pm      # in-app; use normal language 
# Response: There is nothing available at 1500-1800 on Thursday, but all 
# other time blocks are available on Thursday. Choose one and go ahead and 
# schedule it on your calendaring reoccurring workflow JSON object. 
```

**Example: Only "FREQUENCY" variable** 

* `/avail <FREQUENCY>` 
  - You must include AT LEAST the frequency variable 
  - You will be sent the most optimal time block within that variable 
  - The options are selected based on what will be most optimal for app performance 
  - This is a popular option since you don't need to be present for autonomous activity 

* Looking for availability "EVERY-MONTH" at anytime time on any day 

```bash
# Check available time slots before scheduling
mao avail 2                # not in-app; using schedule code numbers 
/avail 2                   # in-app; using schedule code numbers 
mao --avail "every month"  # not in-app; variables in quotes, normal language 
/avail only once a month   # in-app; use normal language 
# Response: Please schedule for calendar code: 2 6 2 which is every month on Saturday at 3am
```

**You will need to include the STARTING-DATE for the reoccurring workflow JSON object to schedule it**

---

## Calendar Availability Architecture
*configs/cli/avail/avail.py, orchestrator/calendar_manager.py*

The `/avail` command system provides intelligent calendar management for trigger workflow scheduling, building on Mao's existing workflow architecture from Section III.

### Calendar Availability Command Implementation

```python
# configs/cli/avail/avail.py - Real implementation
def execute_avail(params):
    """Check calendar availability for trigger workflow scheduling"""
    from orchestrator.calendar_manager import CalendarManager
    from orchestrator.username_manager import UsernameManager
    
    username_manager = UsernameManager()
    calendar_manager = CalendarManager()
    
    # Parse parameters - flexible format support
    frequency = params.get("frequency")
    day = params.get("day") 
    time_block = params.get("time_block")
    
    # Convert natural language to codes if needed
    frequency_code = _parse_frequency(frequency)
    day_code = _parse_day(day) if day else None
    time_code = _parse_time_block(time_block) if time_block else None
    
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
        "every week": "1", "weekly": "1", "1": "1",
        "every other week": "2", "biweekly": "2", "2": "2",
        "every month": "3", "monthly": "3", "3": "3",
        "every other month": "4", "bimonthly": "4", "4": "4",
        "every year": "5", "yearly": "5", "annually": "5", "5": "5",
        "every other year": "6", "biennially": "6", "6": "6",
        "every day": "7", "daily": "7", "7": "7",
        "every other day": "8", "alternate days": "8", "8": "8"
    }
    return freq_map.get(str(freq).lower(), freq)

def _parse_day(day):
    """Convert day to standardized codes"""
    day_map = {
        "monday": "1", "mon": "1", "1": "1",
        "tuesday": "2", "tue": "2", "2": "2", 
        "wednesday": "3", "wed": "3", "3": "3",
        "thursday": "4", "thu": "4", "4": "4",
        "friday": "5", "fri": "5", "5": "5",
        "saturday": "6", "sat": "6", "6": "6",
        "sunday": "7", "sun": "7", "7": "7"
    }
    return day_map.get(str(day).lower(), day)

def _parse_time_block(time):
    """Convert time to standardized codes"""
    time_map = {
        "0000-0300": "1", "1": "1", "midnight": "1", "late night": "1",
        "0300-0600": "2", "2": "2", "early morning": "2",
        "0600-0900": "3", "3": "3", "morning": "3", "6am": "3",
        "0900-1200": "4", "4": "4", "late morning": "4", "9am": "4",
        "1200-1500": "5", "5": "5", "afternoon": "5", "12pm": "5", "noon": "5",
        "1500-1800": "6", "6": "6", "late afternoon": "6", "3pm": "6",
        "1800-2100": "7", "7": "7", "evening": "7", "6pm": "7",
        "2100-0000": "8", "8": "8", "night": "8", "9pm": "8"
    }
    return time_map.get(str(time).lower(), time)
```

### Calendar Management System

```python
# orchestrator/calendar_manager.py - Real implementation
from pathlib import Path
from typing import Dict, List, Any
import json
from datetime import datetime
from .cache.cache_system import CacheManager
from .error_handling import handle_errors

class CalendarManager:
    """Intelligent calendar and availability management for trigger workflows"""
    
    def __init__(self):
        self.cache = CacheManager()
        self.reoccurring_base = Path("configs/reoccurring")
        self.calendar_index_file = self.reoccurring_base / "calendar_index.json"
        self.calendar_codes_file = self.reoccurring_base / "calendar_codes.json"
        
        # Ensure directories exist
        self.reoccurring_base.mkdir(parents=True, exist_ok=True)
        self._initialize_calendar_files()
        
    @handle_errors
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
    
    @handle_errors
    def suggest_optimal_slot(self, frequency_code: str) -> Dict:
        """AI-powered optimal time slot suggestion based on system performance"""
        
        # Analyze historical performance by time slots
        performance_data = self._analyze_historical_performance()
        
        # Find best available slots for this frequency
        available_slots = self._find_all_available_slots(frequency_code)
        
        if not available_slots:
            return {"error": "No available slots found"}
        
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

---

## Calendar Code Reference Tables

The following reference tables define the standardized codes used throughout the trigger workflow system:

| **CODE** | **FREQUENCY**     | **DAY CODE** | **WEEKDAY** | **TIME CODE** | **TIME BLOCK** |
| -------- | ----------------- | ------------ | ----------- | ------------- | -------------- |
| 1        | Every week        | 1            | Monday      | 1             | 0000-0300      |
| 2        | Every other week  | 2            | Tuesday     | 2             | 0300-0600      |
| 3        | Every month       | 3            | Wednesday   | 3             | 0600-0900      |
| 4        | Every other month | 4            | Thursday    | 4             | 0900-1200      |
| 5        | Every year        | 5            | Friday      | 5             | 1200-1500      |
| 6        | Every other year  | 6            | Saturday    | 6             | 1500-1800      |
| 7        | Every day         | 7            | Sunday      | 7             | 1800-2100      |
| 8        | Every other day   | 8            | Monday      | 8             | 2100-0000      |

---

| **SCHEDULING COMMANDS**                         | **DESCRIPTION**                                                 |
| ----------------------------------------------- | --------------------------------------------------------------- |
| `/avail <frequency> <day> <time>`               | Check calendar to scheduling trigger; min. variable <frequency> |
| `/avail --reschedule <custom-command>`          | Change trigger time for repeating workflow                      |
| `/avail --cancel <custom-command>`              | Cancel a repeating workflow                                     |
| `/avail --update <custom-command>`              | Make changes to a repeating workflow                            |
| `/avail --end-date <custom-command> 2025-07-21` | Update the end date on an active repeating workflow             |

---

## Trigger-Workflow Setup Details 

Creating "reoccurring workflows" aka. reoccurring tasks and projects, is simple. We'll cover all the detail below, but as usual, when you need help or are just feeling lazy, Mao will be there to help make sure everything is set up correctly. You don't need to remember any of this! 🙃 

### Setup Differences 

   - Normal workflows are created with the `/setup` command 
   - Reoccurring workflows are created with the `/repeat` command 
   - The `/repeat` command uses a different setup script that has very similar behavior 
   - Each reoccurring workflow type has a --flag to include when scheduling 
   - The script has slightly different results based on which type of reoccurring workflow you are scheduling 
   - The reoccurring workflows are stored in their own config directory section, which is show below 
   - We use one new JSON object for "calendaring" all reoccurring workflows 
   - The calendaring JSON object is identical for all the types of recurring or 'reoccurring workflow' types  

### Reoccurring Workflow Directory Structure 

```
configs/reoccurring/
├── scheduled/
├── self-assessment/
├── project-list/
└── goal-assessment/
```

### Setting Up Reoccurring Workflow JSON Configuration Objects  

* Creating reoccurring workflows require one additional special JSON object 
  - It includes the timing details and schedules the workflow 
  - The `/avail` command activates an orchestrator file to pull available date details 
  - It triggers a notification for the User when it runs 
  - It activates Mao to execute the workflow 

* All reoccurring workflows are reoccurring 
  - Two "assessment" types are open-ended autonomous work time for Mao 
  - The "list" type is a to-do list Mao attends when it runs  
  - The "scheduled" type are typical reoccurring; the same task every time it runs 

* Scheduling a reoccurring workflow uses a different command 
  - You'll find these specifics in the next section 
  - Each reoccurring workflow type command has a flag to identify it 
  - In this way they all use the same setup script 

* The JSON object is the same for all reoccurring workflow types 
  - The only difference is the flag that identifies the reoccurring workflow type 
  - The other three normal JSON objects are used exactly the same as normal 
  - You'll find directory structure details in the next section
  - The next section include file and directory naming conventions

* The Reoccurring Workflow JSON objects 
  - Same protocol as normal workflow setup 
  - Place the JSONs being created in a temporary directory before running the setup script 
  - It is necessary because there are some minimal changes to the JSON objects 
  - The setup scripts will still create the new proper directories 
  - It will then delete the the temporary directory 

* Any additional type-specific details will be found with their JSON below 

--- 

## Reoccurring Workflow Architecture 

Each section below covers a different reoccurring workflow type and includes the small differences from the normal workflow creation, execution, and management. 

### "Scheduled" Type Reoccurring Workflows 
*Workflows by user or Mao that occur every X time period*

**Calendaring JSON Object**
*The calendaring JSON object is the same for all reoccurring workflow types*

* Note the "trigger_type" is "scheduled" for all "Scheduled" type reoccurring workflows 
  - Primary difference from the normal workflow creation, execution, and management 

* The "file_name" versus "project_name" 
  - The "file_name" is the reoccurring workflow type and date code 
  - The "project_name" is the name of the project or task 

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

**Scheduling, File-Naming Conventions, and Directory Structure** 

Just like creating a normal workflow, you put the entire directory path in the command. This path must contain all necessary JSON objects to create a workflow, in addition to the calendaring JSON object. 

```bash
# Create scheduled reoccurring workflow
/repeat --scheduled {{TEMP_DIR}}/scheduled_2_3_7/
mao repeat --scheduled {{TEMP_DIR}}/scheduled_2_3_7/

# Directory structure automatically created:
# configs/reoccurring/scheduled/2_3_7/
# ├── scheduled_2_3_7.json                 # Calendaring JSON object
# ├── scheduled_2_3_7_workflow_config.json # Workflow definition  
# ├── scheduled_2_3_7_phase_config.json    # Phase implementation
# ├── scheduled_2_3_7_handoff_config.json  # Completion criteria
# └── scheduled_2_3_7_README.md            # README file 
```

---

### "Project-List" Type Reoccurring Workflows 
*Work on list created by User or Mao, every X time period*

**Calendaring JSON Object**
*The calendaring JSON object is the same for all reoccurring workflow types*

* You might end up only scheduling a project-list of reoccurring workflow once 
  - It represents the time period Mao will work on the to-do list 
  - Because of this, there are two flags for the project-list reoccurring workflow 
  - New project-lists use the `--list-new` flag 
  - Existing project-lists use the `--list-add` flag 

* Creating a completely new project-list reoccurring workflow 
  - If there is no existing project-list reoccurring workflow, the system will create a new one 
  - There is already a project-list reoccurring workflow, you will be prompted to use that list
  - You can instead create a new project-list reoccurring workflow 
 
* The list will be displayed in the chat when you go to add a new list item 
  - This is so you can adjust the list order according to your needs 
  - This is a good way to get something prioritized and done 
  - It is also an opportunity to delete anything dated or no longer relevant 

* The "file_name" versus "project_name" 
  - The "file_name" is the project with the calendar code numbers 
  - The "project_name" is whatever you want to call the list 

**New List Item on Existing List**

* When creating a new list item on an existing project_list, you don't need another reoccurring workflow JSON object 
  - Use the name on your "workflow" JSON object to identify the project_list 
  - If the reoccurring workflow calendar JSON object has the file_name "project_1_2_4" 
  - Then the "workflow" JSON object is "project_1_2_4_workflow_config" 

* The system will identify the matching names and copy the "reoccurring_workflow" JSON object to the new subdirectory 
  - When the objects are copied over, the "workflow" JSON object "name" is appended with a "_001" counter 
  - For example, this new "workflow" JSON object would have the "name" value "project_1_2_4_001_workflow_config" 

* The subdirectory will be named using just that same counter number 
  - If it is a new list and the first item, the subdirectory will be named "001" 
  - If it is a new list and the second item, the subdirectory will be named "002" 
  - And so on ... 
  - A copy of the "reoccurring_workflow" JSON object will be created in the new subdirectory 
  - The only change will be the "workflow_id" variable value 
  - It will match the "workflow_id" variable value on the standard "workflow" JSON object 

```json
{
  "file_name": "project_1_2_4",
  "project_name": "General To Do List",
  "schema_version": "1.0",
  "reoccurring_workflow": [
    {
    "type": "project-list",
    "frequency": "weekly",
    "frequency_code": "1",
    "day": "Tuesday",
    "day_code": "2",
    "time": "0900-1200",
    "time_block": "4",
    "start_date": "2025-07-23",
    "end_date": "N/A",
    "workflow_id": "uid-aqb-907",
    "created_on": "2025-07-28",
    "created_by_username": "seanivore",
    "created_by_user_id": "user-1642",
    "notes": "none"
    }
  ]
}
```

**Scheduling, File-Naming Conventions, and Directory Structure** 

Just like creating a normal workflow, put the entire directory path containing all necessary JSON objects in the command. 

The *major* difference here is that there is an additional sub-directory for each list item on the list. This is because each list item will have its own JSON objects to define the workflow, along with their own custom command to run the workflow. 

As indicated above, the "name" variable value on the standard "workflow" JSON object will identify the list to which the list item belongs. 

When creating a new list item, the temporary directory *does not require you have the reoccurring workflow JSON object*; it will automatically be found and copied into the new list item's sub-directory. That is the second example below. 

```bash
# Create project-list reoccurring workflow
/repeat --list-new {{TEMP_DIR}}/project_1_2_4/
mao repeat --list-new {{TEMP_DIR}}/project_1_2_4/

# Directory structure automatically created:
# configs/reoccurring/project-list/1_2_4/001/
# ├── project_1_2_4-001.json                 # Calendaring JSON object; same for list items
# ├── project_1_2_4-001_workflow_config.json # Workflow definition  
# ├── project_1_2_4-001_phase_config.json    # Phase implementation
# ├── project_1_2_4-001_handoff_config.json  # Completion criteria
# └── project_1_2_4-001_README.md            # README file 

# Add list items to an existing repeating workflow
/repeat --list-add {{TEMP_DIR}}/project_1_2_4/
mao repeat --list-add {{TEMP_DIR}}/project_1_2_4/

# Directory structure automatically created:
# configs/reoccurring/project-list/1_2_4/002/
# ├── project_1_2_4-002.json                 # Calendaring JSON object; same for list items
# ├── project_1_2_4-002_workflow_config.json # Workflow definition  
# ├── project_1_2_4-002_phase_config.json    # Phase implementation
# ├── project_1_2_4-002_handoff_config.json  # Completion criteria
# └── project_1_2_4-002_README.md            # README file 
```

---

### "Self-Assessment" Type Reoccurring Workflows 
*trigger every X time period; self-assessment by Mao; state management*

**Calendaring JSON Object**
*The calendaring JSON object is the same for all reoccurring workflow types*

* Only difference between Reoccurring Workflow JSON objects 
  - Note the "type" is "self-assessment" for all self-assessment reoccurring workflows 
  - No other oddities  

* The "file_name" versus "project_name" 
  - The "file_name" is the always just "self_assessment" along with the calendar code 
  - The "project_name" is the name of the assessment 
  - These can be rather open-ended 

**Sub-Tasks**

* If and when Mao determines there is a need for specific workflow task 
  - They create a subtask; they only need to create a new "workflow" JSON object, along with phases and handoffs 
  - Make the "workflow" JSON "name" variable value the same as the "file_name" of the reoccurring workflow JSON object 
  - This will cause the script to identify that they are related 

* Once identified and copied over the following changes will be made
  - The "workflow" JSON object will have its "name" variable updated 
  - The new "name" variable will reflect the "custom-command" 
  - This will also be the name of the sub-task's subdirectory 

* Then the "reoccurring_workflow" JSON object will be copied over with a similar change 
  - The "custom-command" will replace the "project_name" variable value, not the "file_name" 
  - And the "workflow_id" will be updated to match the "workflow" JSON object 
  - This ensures they're all tied together 

 
```json
{
  "file_name": "self_assessment_1_7_1",
  "project_name": "Open-Ended Autonomous Work",
  "schema_version": "1.0",
  "reoccurring_workflow": [
    {
    "type": "self-assessment",
    "frequency": "weekly",
    "frequency_code": "1",
    "day": "Sunday",
    "day_code": "7",
    "time": "0000-0300",
    "time_block": "1",
    "start_date": "2025-07-23",
    "end_date": "N/A",
    "workflow_id": "uid-xoy-572",
    "created_on": "2025-07-28",
    "created_by_username": "Mao",
    "created_by_user_id": "user-0919",
    "notes": "none"
    }
  ]
}
```

**Scheduling, File-Naming Conventions, and Directory Structure** 

Just like creating a normal workflow, place the temporary directory path that contains the JSON objects in the command. If this is a new self-assessment it will have all four necessary JSON object types. 

However, if this is a sub-task of an existing self-assessment, you do not need to have the self-assessment reoccurring workflow JSON object in the temporary directory. It will be copied over as indicated in the notes above. 

Representing that they are of the same list, they are both in a directory named with the same calendar code numbers, but the sub-task is in a sub-directory named with the same custom-command as the sub-task. 

```bash
# Create self-assessment reoccurring workflow
/repeat --self-assessment {{TEMP_DIR}}/self_assessment_1_7_1/
mao repeat --self-assessment {{TEMP_DIR}}/self_assessment_1_7_1/

# Directory structure automatically created:
# configs/reoccurring/self-assessment/1_7_1/
# ├── self_assessment_1_7_1.json                 # Calendaring JSON object
# ├── self_assessment_1_7_1_workflow_config.json # Workflow definition  
# ├── self_assessment_1_7_1_phase_config.json    # Phase implementation
# ├── self_assessment_1_7_1_handoff_config.json  # Completion criteria
# └── self_assessment_1_7_1_README.md            # README file 

# Create sub-task of self-assessment reoccurring workflow
/repeat --sub-task {{TEMP_DIR}}/sub_task_custom_command/
mao repeat --sub-task {{TEMP_DIR}}/sub_task_custom_command/

# Directory structure automatically created:
# configs/reoccurring/self-assessment/1_7_1/sub_task_custom_command/
# ├── sub_task_custom_command.json                 # Calendaring JSON object
# ├── sub_task_custom_command_workflow_config.json # Workflow definition  
# ├── sub_task_custom_command_phase_config.json    # Phase implementation
# ├── sub_task_custom_command_handoff_config.json  # Completion criteria
# └── sub_task_custom_command_README.md            # README file 
```

---

### "Goal-Assessment" Type Reoccurring Workflows 
*trigger every X time period; goal-assessment made by user or Mao; state management*

**Calendaring JSON Object**
*The calendaring JSON object is the same for all reoccurring workflow types*

* Only difference between Reoccurring Workflow JSON objects
  - Note the "type" is "goal-assessment" for all goal-assessment reoccurring workflows 
  - No other oddities  

* The "file_name" versus "project_name" 
  - The "file_name" is the always just "goal_assessment" along with the calendar code 
  - The "project_name" is the name of the goal 
  - These can be rather open-ended 

**Sub-Tasks**

* If Mao determines there is a need for specific workflow task 
  - They need only to create a new "workflow" JSON object, along with phases and handoff JSON objects 
  - The "workflow" JSON object's "name" variable value will be the same as the "file_name" of the reoccurring workflow 
  - This will cause the script to identify that they are related 

* Once identified, they are copied to a sub-directory 
  - The sub-directory is named with the same custom-command as the sub-task 
  - The "workflow" JSON object will have its "name" variable updated to reflect the "custom-command" 

* The "reoccurring workflow" JSON object will be copied into the sub-task directory with slight changes 
  - The "custom-command" will replace the "project_name" variable, not the "file_name" 
  - And the "workflow_id" will be updated to match the "workflow" JSON object 
  - This ensures they're all tied together 

```json
{
  "file_name": "goal_assessment_2_3_7",
  "project_name": "Investment Research",
  "schema_version": "1.0",
  "reoccurring_workflow": [
    {
    "type": "goal-assessment",
    "frequency": "every other week",
    "frequency_code": "2",
    "day": "Wednesday",
    "day_code": "3",
    "time": "1800-2100",
    "time_block": "7",
    "start_date": "2025-07-23",
    "end_date": "N/A",
    "workflow_id": "uid-pjb-809",
    "created_on": "2025-07-28",
    "created_by_username": "Mao",
    "created_by_user_id": "user-0919",
    "notes": "none"
    }
  ]
}
```

**Scheduling, File-Naming Conventions, and Directory Structure** 

Just like creating a normal workflow, place the temporary directory path that contains the JSON objects in the command. If this is a new goal-assessment it will have all four necessary JSON object types. 

However, if this is a sub-task of an existing goal-assessment, you do not need to have the goal-assessment reoccurring workflow JSON object in the temporary directory. It will be copied over as indicated in the notes above.  


```bash
# Create goal-assessment reoccurring workflow
/repeat --goal-assessment {{TEMP_DIR}}/goal_assessment_2_3_7/
mao repeat --goal-assessment {{TEMP_DIR}}/goal_assessment_2_3_7/

# Directory structure automatically created:
# configs/reoccurring/goal-assessment/2_3_7/
# ├── goal_assessment_2_3_7.json                 # Calendaring JSON object
# ├── goal_assessment_2_3_7_workflow_config.json # Workflow definition  
# ├── goal_assessment_2_3_7_phase_config.json    # Phase implementation
# ├── goal_assessment_2_3_7_handoff_config.json  # Completion criteria
# └── goal_assessment_2_3_7_README.md            # README file 

# Create sub-task of goal-assessment reoccurring workflow
/repeat --sub-task {{TEMP_DIR}}/sub_task_custom_command/
mao repeat --sub-task {{TEMP_DIR}}/sub_task_custom_command/

# Directory structure automatically created:
# configs/reoccurring/goal-assessment/2_3_7/sub_task_custom_command/
# ├── sub_task_custom_command.json                 # Calendaring JSON object
# ├── sub_task_custom_command_workflow_config.json # Workflow definition  
# ├── sub_task_custom_command_phase_config.json    # Phase implementation
# ├── sub_task_custom_command_handoff_config.json  # Completion criteria
# └── sub_task_custom_command_README.md            # README file 
```

---

## Command Usage Examples

The setup commands for trigger workflows follow the same patterns as standard workflow setup from Section III, with additional calendar-based organization. Each command requires a temporary directory containing the necessary JSON configuration files.

### Command Structure

All trigger workflow commands follow this pattern:
- **In-app**: `/repeat --<type> <temp_directory_path>`
- **Terminal**: `mao repeat --<type> <temp_directory_path>`

The temporary directory must contain the standard workflow JSON files plus the calendar configuration JSON object that defines the scheduling parameters.

### Trigger Workflow Types

Each workflow type creates different directory structures and behaviors:

1. **Scheduled Workflows**: Same task executed repeatedly at scheduled intervals
2. **Project List Workflows**: Work through a prioritized task list during scheduled sessions  
3. **Self-Assessment Workflows**: Autonomous system improvement and optimization
4. **Goal-Assessment Workflows**: Strategic business analysis and project execution

### Implementation Notes

The setup process for trigger workflows extends the standard workflow setup with:
- Calendar code-based directory organization (frequency_day_time pattern)
- Type-specific JSON object processing and file naming
- Calendar index updates for conflict detection
- Custom command generation for workflow execution

*Reference our [Section III](03_USER_FLOW.md) for standard workflow setup patterns* 


```bash
# Create scheduled workflow
/repeat --scheduled {{TEMP_DIR}}/scheduled_2_3_7/
mao repeat --scheduled {{TEMP_DIR}}/scheduled_2_3_7/

# Create project-list workflow
/repeat --list-new {{TEMP_DIR}}/project_1_2_4/
mao repeat --list-new {{TEMP_DIR}}/project_1_2_4/

# Create self-assessment workflow
/repeat --self-assessment {{TEMP_DIR}}/self_assessment_1_7_1/
mao repeat --self-assessment {{TEMP_DIR}}/self_assessment_1_7_1/
```

---

| **REOCCURRING WORKFLOW** | **SETUP COMMAND**           | **OBJECTIVE WHEN TRIGGERED**      |
| ------------------------ | --------------------------- | --------------------------------- |
| Scheduled Workflow       | `/repeat --scheduled`       | Same project every time it runs   |
| Project-List Flow        | `/repeat --list-new`        | Work on task list                 |
| Project-List             | `/repeat --list-add`        | N/A                               |
| Self-Assessment          | `/repeat --self-assessment` | Analyze, identify, improve Mao    |
| Self-Assessment          | `/repeat --sub-task`        | Task related to self-assessment   |
| Goal-Assessment          | `/repeat --goal-assessment` | Analyze, plan, execute objectives |
| Goal-Assessment          | `/repeat --sub-task`        | Task related to goal-assessment   |

---

## Trigger Workflow Setup Architecture
*configs/cli/repeat/repeat.py, scripts/setup_trigger_workflow.sh*

Building on the standard workflow setup from Section III, trigger workflows extend the setup process with calendar-based scheduling and type-specific directory organization.

### Repeat Command Implementation

```python
# configs/cli/repeat/repeat.py 
def execute_repeat(params):
    """Create reoccurring trigger workflows with type-specific setup"""
    from orchestrator.calendar_manager import CalendarManager
    from orchestrator.username_manager import UsernameManager
    import subprocess
    import os
    
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
        elif self.workflow_type == "self-assessment":
            return f"{self.reoccurring_base}/self-assessment/{freq_code}_{day_code}_{time_code}"
        elif self.workflow_type == "goal-assessment":
            return f"{self.reoccurring_base}/goal-assessment/{freq_code}_{day_code}_{time_code}"
```

### Enhanced Setup Script Integration

```bash
#!/bin/bash
# scripts/setup_trigger_workflow.sh - Enhanced setup for trigger workflows
# Extends existing setup_workflow.sh with trigger-specific functionality

TEMP_DIR="$1"
WORKFLOW_TYPE="$2"

if [ -z "$TEMP_DIR" ] || [ -z "$WORKFLOW_TYPE" ]; then
    echo "Usage: $0 <temp_directory> <workflow_type>"
    exit 1
fi

# Source existing workflow setup functions from Section III
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

# Generate custom command (builds on Section III patterns)
generate_trigger_command "$TARGET_DIR" "$WORKFLOW_TYPE"

echo "Trigger workflow created successfully at: $TARGET_DIR"
```

### CLI Integration Architecture

The `/repeat` command integrates with Mao's existing CLI system from Section III, extending the command discovery pattern:

```python
# orchestrator/cli_manager.py - Integration with existing system
def _handle_repeat_command(self, data: Any) -> Dict[str, Any]:
    """Handle trigger workflow creation"""
    try:
        from configs.cli.repeat.repeat import execute_repeat
        
        # Parse flags and path using existing CLI patterns
        if isinstance(data, dict):
            params = data
        else:
            params = self._parse_repeat_command(data)
            
        return execute_repeat(params)
        
    except Exception as e:
        return {"success": False, "error": f"Repeat command failed: {str(e)}"}

# Add to command discovery (existing pattern from Section III)
"repeat": {
    "module": "configs.cli.repeat.repeat", 
    "function": "execute_repeat",
    "description": "Create reoccurring trigger workflows"
}
```

---

## From Assistant to Autonomous Business Partner

Traditional automation handles repetitive, predefined tasks. Mao's timer-triggered workflows handle intelligence itself - transforming from a productivity tool into a complete business operating system.

### Business Autonomy Revolution

Your business can respond to opportunities and challenges even when you're not actively managing it. Mao analyzes your business situation and creates the appropriate response for current conditions.

You'll be notified of price changes in your market or customer behavior shifts, potentially even after action has been taken to adjust and turn this into an opportunity.

This isn't about automating individual tasks. This is about Mao taking responsibility for entire business functions while you focus on strategy, creativity, and growth.

### Autonomous Business Operations

Mao can autonomously manage:

- Social media management and content creation
- Email marketing and customer communication  
- Project management and task coordination
- Market research and competitive analysis
- Performance monitoring and optimization

### Intelligent Self-Improvement

Mao doesn't just optimize your business; it optimizes its own performance through continuous self-analysis. The system tracks its own effectiveness, identifies improvement opportunities, and implements enhancements to its own capabilities.

This meta-learning creates exponential improvement curves where the business automation becomes more intelligent and effective over time. The AI assistant literally becomes more valuable and capable through experience with your specific business context.

### The Future of AI Autonomy

Create a calendared workflow for analysis, optimization, or strategic planning. You can even simply schedule the workflow for Mao to work autonomously on whatever needs attention.

Through modular JSON configurations rather than hardcoded systems, every business can customize their autonomous operations to their specific needs and goals. And while the system is intended to be simple enough for anyone, it truly requires no learning curve to use because all you need to do is inform Mao, and all will be scheduled accurately for you.

---

*This automation capability transforms Mao from a powerful productivity tool into a complete business operating system. The timer-triggered workflows enable genuine business autonomy where AI handles operations while humans focus on strategy, creativity, and growth.*