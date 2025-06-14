"""
Think Tool - Human Button Generators
Simple executable snippets for AI thinking operations
"""

from typing import Dict, Any
import json

def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable snippet for AI thinking
    
    Args:
        params: Thinking parameters
        model: Target model for execution
        
    Returns:
        Executable code snippet
    """
    topic = params.get("topic", "")
    thinking_approach = params.get("thinking_approach", "systematic analysis")
    thinking_focus = params.get("thinking_focus", "comprehensive insights")
    context = params.get("context", "")
    save_results = params.get("save_results", True)
    
    # Build thinking prompt
    prompt_parts = [f"Think about this topic: {topic}"]
    
    if thinking_approach != "systematic analysis":
        prompt_parts.append(f"Approach: {thinking_approach}")
    
    if thinking_focus != "comprehensive insights":
        prompt_parts.append(f"Focus on: {thinking_focus}")
    
    if context:
        prompt_parts.append(f"Context: {context}")
    
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
    
    thinking_prompt = "\n".join(prompt_parts)
    
    return f'''
# AI Thinking Session
import anthropic
from datetime import datetime
import json

# Initialize client
client = anthropic.Anthropic()

# Thinking parameters
topic = "{topic}"
thinking_approach = "{thinking_approach}"
thinking_focus = "{thinking_focus}"
context = "{context}"
save_results = {save_results}

print("🧠 Starting AI thinking session...")
print(f"📋 Topic: {{topic}}")
print(f"🎯 Approach: {{thinking_approach}}")
print(f"🔍 Focus: {{thinking_focus}}")
if context:
    print(f"📝 Context: {{context}}")
print("=" * 60)

try:
    # Perform AI thinking
    response = client.messages.create(
        model="{model}",
        max_tokens=4000,
        messages=[{{
            "role": "user",
            "content": """{thinking_prompt}"""
        }}]
    )
    
    # Extract thinking results
    thinking_output = response.content[0].text
    
    # Display results
    print("🎯 THINKING RESULTS")
    print("=" * 60)
    print(thinking_output)
    print("\\n" + "=" * 60)
    print("✅ Thinking session completed")
    
    # Save results if requested
    if save_results:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save thinking data
        thinking_data = {{
            "topic": topic,
            "thinking_approach": thinking_approach,
            "thinking_focus": thinking_focus,
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "thinking_output": thinking_output,
            "model_used": "{model}"
        }}
        
        # Save JSON data
        json_file = f"thinking_session_{{timestamp}}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(thinking_data, f, indent=2, ensure_ascii=False)
        
        # Save formatted report
        report_file = f"thinking_report_{{timestamp}}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# Thinking Session Report\\n\\n")
            f.write(f"**Topic:** {{topic}}\\n")
            f.write(f"**Approach:** {{thinking_approach}}\\n")
            f.write(f"**Focus:** {{thinking_focus}}\\n")
            f.write(f"**Date:** {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}\\n")
            if context:
                f.write(f"**Context:** {{context}}\\n")
            f.write(f"**Model:** {model}\\n\\n")
            f.write("## Thinking Results\\n\\n")
            f.write(thinking_output)
        
        print(f"💾 Data saved: {{json_file}}")
        print(f"📄 Report saved: {{report_file}}")
    
    print(f"💡 Thinking completed for: {{topic}}")
    
except Exception as e:
    print(f"❌ Thinking session failed: {{str(e)}}")
    print("💡 Check your API key and connection")
'''

def create_prompt_enhancement_button(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable snippet for prompt enhancement
    
    Args:
        params: Enhancement parameters
        model: Target model for execution
        
    Returns:
        Executable code snippet
    """
    base_topic = params.get("base_topic", "")
    enhancement_approach = params.get("enhancement_approach", "add depth and structure")
    enhancement_focus = params.get("enhancement_focus", "actionable insights")
    
    return f'''
# AI Prompt Enhancement
import anthropic
from datetime import datetime

# Initialize client
client = anthropic.Anthropic()

# Enhancement parameters
base_topic = "{base_topic}"
enhancement_approach = "{enhancement_approach}"
enhancement_focus = "{enhancement_focus}"

print("✨ Starting prompt enhancement...")
print(f"📝 Original topic: {{base_topic}}")
print(f"🎯 Enhancement approach: {{enhancement_approach}}")
print(f"🔍 Enhancement focus: {{enhancement_focus}}")
print("=" * 60)

try:
    # Enhance the prompt
    enhancement_prompt = f"""Please enhance this thinking prompt to make it more effective:

Original prompt: "{{base_topic}}"

Enhancement approach: {{enhancement_approach}}
Enhancement focus: {{enhancement_focus}}

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
    
    # Display enhancement results
    enhancement_output = response.content[0].text
    
    print("✨ PROMPT ENHANCEMENT RESULTS")
    print("=" * 60)
    print(enhancement_output)
    print("\\n" + "=" * 60)
    print("✅ Prompt enhancement completed")
    
    # Save enhancement
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"prompt_enhancement_{{timestamp}}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# Prompt Enhancement\\n\\n")
        f.write(f"**Original:** {{base_topic}}\\n")
        f.write(f"**Enhancement Approach:** {{enhancement_approach}}\\n")
        f.write(f"**Enhancement Focus:** {{enhancement_focus}}\\n")
        f.write(f"**Date:** {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}\\n")
        f.write(f"**Model:** {model}\\n\\n")
        f.write("## Enhancement Results\\n\\n")
        f.write(enhancement_output)
    
    print(f"💾 Enhancement saved: {{filename}}")
    
except Exception as e:
    print(f"❌ Prompt enhancement failed: {{str(e)}}")
    print("💡 Check your API key and connection")
'''

def create_thinking_validation_button(model: str = "claude-sonnet-4") -> str:
    """
    Generate executable snippet for thinking tool validation
    
    Args:
        model: Target model for execution
        
    Returns:
        Executable code snippet
    """
    return f'''
# Think Tool Validation
import anthropic
import os
from datetime import datetime

print("🔍 Validating Think Tool setup...")
print("=" * 60)

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

print("\\n" + "=" * 60)

# Overall status
if "✅" in api_key_status and "✅" in api_connection_status:
    print("✅ Think Tool validation PASSED")
    print("🚀 Ready for AI thinking operations!")
else:
    print("❌ Think Tool validation FAILED")
    print("💡 Check API key and connection settings")

print(f"⏰ Validation completed: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
'''

def create_thinking_capabilities_button(model: str = "claude-sonnet-4") -> str:
    """
    Generate executable snippet for displaying thinking capabilities
    
    Args:
        model: Target model for execution
        
    Returns:
        Executable code snippet
    """
    return f'''
# Think Tool Capabilities
from datetime import datetime

print("🚀 Think Tool Capabilities")
print("=" * 60)

# Core operations
print("🔧 CORE OPERATIONS:")
operations = [
    "perform_thinking - Structured AI thinking sessions",
    "enhance_thinking_prompt - Improve thinking prompts", 
    "validate_thinking_setup - Check tool readiness",
    "get_thinking_capabilities - Display this information"
]

for op in operations:
    print(f"  • {{op}}")

print("\\n🎯 THINKING FEATURES:")
features = [
    "Flexible thinking approaches (user-defined)",
    "Context-aware thinking sessions", 
    "Automatic result saving and documentation",
    "Cost estimation and tracking",
    "Universal model compatibility"
]

for feature in features:
    print(f"  • {{feature}}")

print("\\n✨ FLEXIBILITY:")
flexibility = [
    "No hardcoded frameworks or templates",
    "User-defined thinking approaches",
    "Adaptable to any domain or use case", 
    "Natural language thinking instructions"
]

for flex in flexibility:
    print(f"  • {{flex}}")

print("\\n🤖 MODEL COMPATIBILITY:")
models = [
    "claude-3-5-sonnet",
    "claude-sonnet-4",
    "gpt-4", 
    "gpt-4-turbo",
    "gemini-pro"
]

for model_name in models:
    print(f"  • {{model_name}}")

print("\\n💰 COST STRUCTURE:")
print("  • Base cost: ~$0.01 per thinking session")
print("  • Factors: topic complexity, context length, model choice")

print("\\n" + "=" * 60)
print("✅ Think Tool ready for flexible AI thinking!")
print(f"⏰ {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
''' 