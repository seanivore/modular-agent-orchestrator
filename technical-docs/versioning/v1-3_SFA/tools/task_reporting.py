import os
import json
import datetime
from typing import Dict, Any, List, Optional, Union

def task_report(content: Optional[str] = None,
                file_paths: Optional[List[str]] = None,
                report: str = "",
                next_steps: str = "",
                decision: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Generate a comprehensive task report with token verification.
    
    Args:
        content: Optional content to save to file(s)
        file_paths: Optional list of paths where content will be saved
        report: Summary of what was accomplished (required)
        next_steps: Suggested next steps or path forward (required)
        decision: Decision output if this phase involved making a choice
        
    Returns:
        Dictionary with task report results and success status
    """
    try:
        # Check if token_counter is available for content
        token_result = None
        if content and "token_counter" in globals().get("available_tools", {}):
            token_result = globals()["available_tools"]["token_counter"](text=content)
            print(f"[blue]Token count:[/blue] {token_result['token_count']}")
            
            if not token_result["is_safe"]:
                return {
                    "success": False,
                    "error": f"Content exceeds token limit ({token_result['token_count']} tokens). Please revise before completing.",
                    "token_count": token_result["token_count"],
                    "limit": 7000
                }
        
        # Create a standardized report
        phase_summary = {
            "timestamp": str(datetime.datetime.now()),
            "token_count": token_result["token_count"] if token_result else "not checked",
            "report": report,  # Required detailed summary
            "next_steps": next_steps,  # Required specific actions
            "files_saved": []
        }
        
        # Add decision data if provided
        if decision:
            phase_summary["decision"] = decision
        
        # Save content to files if provided
        if content and file_paths:
            for file_path in file_paths:
                try:
                    # Create directory if it doesn't exist
                    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"[green]Saved to:[/green] {file_path}")
                    phase_summary["files_saved"].append(file_path)
                    
                    # Add to saved outputs tracking if the global is available
                    if "output_path" in globals() and "saved_outputs" in globals():
                        if file_path in globals()["output_path"]:
                            globals()["saved_outputs"].add(file_path)
                except Exception as e:
                    print(f"[red]Error saving to {file_path}:[/red] {str(e)}")
        
        # Save the report as JSON
        # Use the phase number from args if available
        phase_number = getattr(globals().get("args", None), "phase", 0)
        report_file = f"task_report_phase_{phase_number}.json"
        
        with open(report_file, 'w') as f:
            json.dump(phase_summary, f, indent=2)
        
        print(f"[green]Phase summary saved to:[/green] {report_file}")
        
        # Signal task completion
        if "task_complete" in globals():
            globals()["task_complete"] = True
        
        return {
            "success": True,
            "message": "Phase summary created and saved. Phase completion triggered.",
            "report_file": report_file
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def get_tool_definition():
    """Return the tool definition for SFA integration."""
    return {
        "name": "task_report",
        "description": "Create a phase summary report that includes token counts, accomplishments, and next steps. This will trigger phase completion.",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Optional content to save to files"
                },
                "file_paths": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of file paths where content will be saved"
                },
                "report": {
                    "type": "string",
                    "description": "Summary of what was accomplished in this phase"
                },
                "next_steps": {
                    "type": "string",
                    "description": "Recommendations for the next phase"
                },
                "decision": {
                    "type": "object",
                    "description": "Decision output if this phase involved making a choice",
                    "properties": {
                        "options": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of options that were considered"
                        },
                        "choice": {
                            "type": "string",
                            "description": "The selected option"
                        },
                        "reasoning": {
                            "type": "string",
                            "description": "Explanation for the decision"
                        }
                    }
                }
            },
            "required": ["report", "next_steps"]
        },
        "function": task_report
    }