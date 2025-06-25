"""
Think Tool - Human Button Generator
Standardized Single Entry Point
"""

from typing import Dict, Any
import json
from tools.think.think import (
    perform_thinking, enhance_thinking_prompt, validate_thinking_setup, estimate_cost
)


def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable snippet for AI thinking operations
    
    Args:
        params: Thinking parameters
        model: Target model for execution
        
    Returns:
        Executable code snippet using MAO logic functions
    """
    operation = params.get("operation", "perform_thinking")
    
    if operation == "perform_thinking":
        return _create_thinking_snippet(params, model)
    elif operation == "enhance_thinking_prompt":
        return _create_enhancement_snippet(params, model)
    elif operation == "validate_thinking_setup":
        return _create_validation_snippet(params, model)
    else:
        return _create_thinking_snippet(params, model)  # Default


def _create_thinking_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate thinking session snippet using MAO logic functions"""
    topic = params.get("topic", "")
    thinking_approach = params.get("thinking_approach", "systematic analysis")
    thinking_focus = params.get("thinking_focus", "comprehensive insights")
    context = params.get("context", "")
    save_results = params.get("save_results", True)
    
    escaped_topic = json.dumps(topic)
    escaped_context = json.dumps(context)
    
    return f'''
# AI Thinking Session - Using MAO Logic Functions
import anthropic
import json
from datetime import datetime
from tools.think.think import perform_thinking, estimate_cost
from tools.think.ui_think import display_thinking_session

def execute_thinking_session():
    """Execute AI thinking session using MAO logic functions"""
    
    params = {{
        "topic": {escaped_topic},
        "thinking_approach": "{thinking_approach}",
        "thinking_focus": "{thinking_focus}",
        "context": {escaped_context},
        "save_results": {save_results}
    }}
    
    print("🧠 AI Thinking Session")
    print(f"📋 Topic: {{params['topic']}}")
    print(f"🎯 Approach: {{params['thinking_approach']}}")
    print(f"🔍 Focus: {{params['thinking_focus']}}")
    if params["context"]:
        print(f"📝 Context: {{params['context']}}")
    print("="*60)
    
    try:
        # Use MAO logic function to prepare thinking session
        session_result = perform_thinking(**params)
        
        # Display session preparation using MAO UI function
        display_thinking_session(session_result, verbose=True)
        
        if session_result.get("status") == "ready":
            session_data = session_result.get("session_data", {{}})
            
            # Build AI thinking prompt
            prompt_parts = [f"Think about this topic: {{session_data.get('topic')}}"]
            
            if session_data.get("thinking_approach") != "systematic analysis":
                prompt_parts.append(f"Approach: {{session_data.get('thinking_approach')}}")
            
            if session_data.get("thinking_focus") != "comprehensive insights":
                prompt_parts.append(f"Focus on: {{session_data.get('thinking_focus')}}")
            
            if session_data.get("context"):
                prompt_parts.append(f"Context: {{session_data.get('context')}}")
            
            prompt_parts.extend([
                "",
                "Please provide structured thinking that includes:",
                "1. Understanding of the topic",
                "2. Key factors and considerations", 
                "3. Analysis and insights",
                "4. Conclusions and implications",
                "5. Actionable recommendations or next steps",
                "",
                "Be thorough, clear, and practical in your thinking."
            ])
            
            thinking_prompt = "\\n".join(prompt_parts)
            
            # Execute AI thinking
            print("\\n🤖 Executing AI thinking...")
            client = anthropic.Anthropic()
            
            response = client.messages.create(
                model="{model}",
                max_tokens=4000,
                messages=[{{
                    "role": "user",
                    "content": thinking_prompt
                }}]
            )
            
            thinking_output = response.content[0].text
            
            # Display results
            print("\\n🎯 THINKING RESULTS")
            print("="*60)
            print(thinking_output)
            print("\\n" + "="*60)
            print("✅ Thinking session completed")
            
            # Save results if requested
            if session_data.get("save_results"):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                # Save thinking data
                thinking_data = {{
                    "topic": session_data.get("topic"),
                    "thinking_approach": session_data.get("thinking_approach"),
                    "thinking_focus": session_data.get("thinking_focus"),
                    "context": session_data.get("context"),
                    "timestamp": datetime.now().isoformat(),
                    "thinking_output": thinking_output,
                    "model_used": "{model}",
                    "session_id": session_data.get("session_id")
                }}
                
                # Save JSON data
                json_file = f"thinking_session_{{timestamp}}.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(thinking_data, f, indent=2, ensure_ascii=False)
                
                # Save formatted report
                report_file = f"thinking_report_{{timestamp}}.md"
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(f"# Thinking Session Report\\n\\n")
                    f.write(f"**Topic:** {{session_data.get('topic')}}\\n")
                    f.write(f"**Approach:** {{session_data.get('thinking_approach')}}\\n")
                    f.write(f"**Focus:** {{session_data.get('thinking_focus')}}\\n")
                    f.write(f"**Date:** {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}\\n")
                    if session_data.get("context"):
                        f.write(f"**Context:** {{session_data.get('context')}}\\n")
                    f.write(f"**Model:** {model}\\n")
                    f.write(f"**Session ID:** {{session_data.get('session_id')}}\\n\\n")
                    f.write("## Thinking Results\\n\\n")
                    f.write(thinking_output)
                
                print(f"💾 Data saved: {{json_file}}")
                print(f"📄 Report saved: {{report_file}}")
            
            print(f"💰 Estimated cost: ${estimate_cost(params):.4f}")
            print(f"💡 Thinking completed for: {{session_data.get('topic')}}")
            
        else:
            print("❌ Thinking session preparation failed")
    
    except Exception as e:
        print(f"❌ Thinking session failed: {{str(e)}}")
        print("💡 Check your API key, connection, and MAO modules")

execute_thinking_session()
'''


def _create_enhancement_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate prompt enhancement snippet using MAO logic functions"""
    base_topic = params.get("base_topic", "")
    enhancement_approach = params.get("enhancement_approach", "add depth and structure")
    enhancement_focus = params.get("enhancement_focus", "actionable insights")
    
    escaped_topic = json.dumps(base_topic)
    
    return f'''
# AI Prompt Enhancement - Using MAO Logic Functions
import anthropic
import json
from datetime import datetime
from tools.think.think import enhance_thinking_prompt, estimate_cost
from tools.think.ui_think import display_prompt_enhancement

def execute_prompt_enhancement():
    """Execute prompt enhancement using MAO logic functions"""
    
    params = {{
        "base_topic": {escaped_topic},
        "enhancement_approach": "{enhancement_approach}",
        "enhancement_focus": "{enhancement_focus}"
    }}
    
    print("✨ AI Prompt Enhancement")
    print(f"📝 Original topic: {{params['base_topic']}}")
    print(f"🎯 Enhancement approach: {{params['enhancement_approach']}}")
    print(f"🔍 Enhancement focus: {{params['enhancement_focus']}}")
    print("="*60)
    
    try:
        # Use MAO logic function to prepare enhancement
        enhancement_result = enhance_thinking_prompt(**params)
        
        # Display enhancement preparation using MAO UI function
        display_prompt_enhancement(enhancement_result, verbose=True)
        
        if enhancement_result.get("status") == "ready":
            enhancement_data = enhancement_result.get("enhancement_data", {{}})
            
            # Execute AI enhancement
            print("\\n🤖 Executing AI enhancement...")
            client = anthropic.Anthropic()
            
            enhancement_prompt = f"""Please enhance this thinking prompt to make it more effective:

Original prompt: "{{enhancement_data.get('original_topic')}}"

Enhancement approach: {{enhancement_data.get('enhancement_approach')}}
Enhancement focus: {{enhancement_data.get('enhancement_focus')}}

Please provide:
1. An enhanced version of the prompt that is more specific and actionable
2. Explanation of what improvements were made
3. Suggestions for how to use the enhanced prompt effectively

Make the enhanced prompt clear, structured, and likely to produce better thinking results."""

            response = client.messages.create(
                model="{model}",
                max_tokens=3000,
                messages=[{{
                    "role": "user",
                    "content": enhancement_prompt
                }}]
            )
            
            enhancement_output = response.content[0].text
            
            # Display results
            print("\\n✨ PROMPT ENHANCEMENT RESULTS")
            print("="*60)
            print(enhancement_output)
            print("\\n" + "="*60)
            print("✅ Prompt enhancement completed")
            
            # Save enhancement
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"prompt_enhancement_{{timestamp}}.md"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Prompt Enhancement\\n\\n")
                f.write(f"**Original:** {{enhancement_data.get('original_topic')}}\\n")
                f.write(f"**Enhancement Approach:** {{enhancement_data.get('enhancement_approach')}}\\n")
                f.write(f"**Enhancement Focus:** {{enhancement_data.get('enhancement_focus')}}\\n")
                f.write(f"**Date:** {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}\\n")
                f.write(f"**Model:** {model}\\n\\n")
                f.write("## Enhancement Results\\n\\n")
                f.write(enhancement_output)
            
            print(f"💾 Enhancement saved: {{filename}}")
            print(f"💰 Estimated cost: ${estimate_cost(params):.4f}")
            
        else:
            print("❌ Prompt enhancement preparation failed")
    
    except Exception as e:
        print(f"❌ Prompt enhancement failed: {{str(e)}}")
        print("💡 Check your API key, connection, and MAO modules")

execute_prompt_enhancement()
'''


def _create_validation_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate validation snippet using MAO logic functions"""
    
    return f'''
# Think Tool Validation - Using MAO Logic Functions
import anthropic
import os
from datetime import datetime
from tools.think.think import validate_thinking_setup, estimate_cost
from tools.think.ui_think import display_thinking_validation

def execute_thinking_validation():
    """Execute thinking tool validation using MAO logic functions"""
    
    print("🔍 Think Tool Validation")
    print("="*60)
    
    try:
        # Use MAO logic function for validation
        validation_result = validate_thinking_setup()
        
        # Display validation results using MAO UI function
        display_thinking_validation(validation_result, verbose=True)
        
        if validation_result.get("status") == "success":
            # Additional API tests
            print("\\n🌐 Testing API Connection...")
            
            # Check API key
            api_key_status = "✅ Available" if os.getenv("ANTHROPIC_API_KEY") else "❌ Missing"
            print(f"🔑 Anthropic API Key: {{api_key_status}}")
            
            # Check file system access
            try:
                test_file = f"test_write_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.tmp"
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                file_system_status = "✅ Available"
            except:
                file_system_status = "❌ Limited"
            
            print(f"💾 File System: {{file_system_status}}")
            
            # Test API connection
            try:
                client = anthropic.Anthropic()
                test_response = client.messages.create(
                    model="{model}",
                    max_tokens=50,
                    messages=[{{"role": "user", "content": "Test connection - respond with 'OK'"}}]
                )
                api_connection_status = "✅ Connected"
                print(f"🌐 API Connection: {{api_connection_status}}")
                print(f"📡 Test Response: {{test_response.content[0].text.strip()}}")
            except Exception as e:
                api_connection_status = f"❌ Failed: {{str(e)}}"
                print(f"🌐 API Connection: {{api_connection_status}}")
            
            print("\\n" + "="*60)
            
            # Overall status
            if "✅" in api_key_status and "✅" in api_connection_status:
                print("✅ Think Tool validation PASSED")
                print("🚀 Ready for AI thinking operations!")
            else:
                print("❌ Think Tool validation FAILED")
                print("💡 Check API key and connection settings")
            
            print(f"💰 Estimated cost: ${estimate_cost({{}}):.4f}")
            
        else:
            print("❌ Think Tool validation failed")
    
    except Exception as e:
        print(f"❌ Validation failed: {{str(e)}}")
        print("💡 Ensure MAO modules are properly installed")
    
    print(f"⏰ Validation completed: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")

execute_thinking_validation()
'''
