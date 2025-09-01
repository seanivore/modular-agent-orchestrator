#!/usr/bin/env python3
"""
Button Snippet Generator
Creates executable code snippets for any model / provider combo to avoid SDK hell
"""

import json
import os
from typing import Dict, List, Optional, Any
from .manager_models import ModelManager

# Standard Mao imports
from .cache.cache_system import CacheManager
from .error_handling import handle_errors, APIError

# Standard cache instance
cache = CacheManager()


class ButtonManager:
    """
    CORE SNIPPET GENERATOR
    Generates executable code snippets that Claude 4 can run via Code Execution Tool
    """
    
    def __init__(self, model_manager: ModelManager):
        self.models = model_manager
    
    def estimate_cost(self, params: Dict[str, Any] = None) -> float:
        """REQUIRED: Estimate operation cost for budget planning"""
        return 0.001  # Button generation is very low cost
        
    @handle_errors(operation_name="create_api_call_snippet", return_dict=True)
    def create_api_call_snippet(
        self, 
        model_name: str, 
        prompt: str, 
        system_message: Optional[str] = None,
        tools: Optional[List[Dict]] = None,
        max_tokens: int = 8192,
        temperature: float = 0.3
    ) -> str:
        """
        PRIMARY BUTTON GENERATOR
        Generate executable code snippet for ANY model / provider combo
        """
        model = self.models.get_model_config(model_name)
        provider = self.models.get_provider_for_model(model_name)
        
        if not model or not provider:
            return f"# ERROR: Model '{model_name}' not found in configs"
        
        # Generate the appropriate snippet based on provider type
        if provider.api_type == "anthropic":
            return self._create_anthropic_snippet(
                model, provider, prompt, system_message, tools, max_tokens, temperature
            )
        elif provider.api_type == "openai":
            return self._create_openai_snippet(
                model, provider, prompt, system_message, tools, max_tokens, temperature
            )
        elif provider.api_type == "gemini":
            return self._create_gemini_snippet(
                model, provider, prompt, system_message, tools, max_tokens, temperature
            )
        else:
            return f"# ERROR: Unsupported API type '{provider.api_type}'"
    
    def _create_anthropic_snippet(
        self, model, provider, prompt, system_message, tools, max_tokens, temperature
    ) -> str:
        """PROVIDER: Generate Anthropic API snippet"""
        
        snippet = f'''
# PRIMARY BUTTON: {model.display_name}
import anthropic
import os
import json

# Initialize client
client = anthropic.Anthropic(api_key=os.getenv("{provider.env_var}"))

# Prepare messages
messages = [{{"role": "user", "content": "{prompt}"}}]

# Request parameters
params = {{
    "model": "{model.model_id}",
    "messages": messages,
    "max_tokens": {max_tokens},
    "temperature": {temperature}
}}
'''

        if system_message:
            snippet += f'''
# Add system message
params["system"] = "{system_message}"
'''

        if tools:
            snippet += f'''
# Add tools
params["tools"] = {json.dumps(tools, indent=2)}
'''

        if model.capabilities.caching:
            snippet += f'''
# Enable caching for Claude 4
params["extra_headers"] = {{"anthropic-beta": "prompt-caching-2024-07-31"}}
'''

        snippet += f'''
# Make the API call
try:
    response = client.messages.create(**params)
    
    # Extract result
    content = response.content[0].text if response.content else ""
    
    # Calculate cost
    input_tokens = response.usage.input_tokens if hasattr(response.usage, 'input_tokens') else 0
    output_tokens = response.usage.output_tokens if hasattr(response.usage, 'output_tokens') else 0
    input_cost = (input_tokens / 1_000_000) * {model.input_price}
    output_cost = (output_tokens / 1_000_000) * {model.output_price}
    total_cost = input_cost + output_cost
    
    # Print results
    print(f"🎯 Model: {model.display_name}")
    print(f"💰 Cost: ${{total_cost:.6f}} ({{input_tokens:,}} in, {{output_tokens:,}} out)")
    print(f"📝 Response:")
    print(content)
    
    # Extract tool calls if any
    tool_calls = []
    if hasattr(response, 'content'):
        for block in response.content:
            if hasattr(block, 'type') and block.type == 'tool_use':
                tool_calls.append({{
                    "id": block.id,
                    "name": block.name,
                    "input": block.input
                }})
    
    if tool_calls:
        print(f"🔧 Tool calls: {{len(tool_calls)}}")
        for call in tool_calls:
            print(f"  - {{call['name']}}({{call['input']}})")
    
    # Return structured result
    result = {{
        "content": content,
        "tool_calls": tool_calls,
        "usage": {{
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_cost": total_cost
        }},
        "model": "{model.name}",
        "provider": "{provider.name}"
    }}
    
except Exception as e:
    print(f"❌ Error: {{str(e)}}")
    result = {{"error": str(e), "model": "{model.name}"}}

# SUCCESS! 🎉
result
'''
        return snippet.strip()
    
    def _create_openai_snippet(
        self, model, provider, prompt, system_message, tools, max_tokens, temperature
    ) -> str:
        """PROVIDER: Generate OpenAI-compatible snippet (Requesty, LM Studio, etc.)"""
        
        snippet = f'''
# PRIMARY BUTTON: {model.display_name} via {provider.display_name}
import openai
import os
import json

# Initialize client
client = openai.OpenAI(
    base_url="{provider.base_url}",
'''
        
        if provider.env_var:
            snippet += f'    api_key=os.getenv("{provider.env_var}"),\n'
        else:
            snippet += '    api_key="not-needed"  # Local server\n'
        
        snippet += ''')

# Prepare messages
messages = []
'''

        if system_message:
            snippet += f'''
messages.append({{"role": "system", "content": "{system_message}"}})
'''

        snippet += f'''
messages.append({{"role": "user", "content": "{prompt}"}})

# Request parameters
params = {{
    "model": "{model.model_id}",
    "messages": messages,
    "max_tokens": {max_tokens},
    "temperature": {temperature}
}}
'''

        if tools:
            snippet += f'''
# Convert tools to OpenAI format
openai_tools = []
for tool in {json.dumps(tools, indent=2)}:
    openai_tools.append({{
        "type": "function",
        "function": {{
            "name": tool["name"],
            "description": tool["description"],
            "parameters": tool["input_schema"]
        }}
    }})
params["tools"] = openai_tools
'''

        snippet += f'''
# Make the API call
try:
    response = client.chat.completions.create(**params)
    
    # Extract result
    content = response.choices[0].message.content or ""
    
    # Calculate cost
    input_tokens = response.usage.prompt_tokens if hasattr(response.usage, 'prompt_tokens') else 0
    output_tokens = response.usage.completion_tokens if hasattr(response.usage, 'completion_tokens') else 0
    input_cost = (input_tokens / 1_000_000) * {model.input_price}
    output_cost = (output_tokens / 1_000_000) * {model.output_price}
    total_cost = input_cost + output_cost
    
    # Print results
    print(f"🎯 Model: {model.display_name}")
    print(f"💰 Cost: ${{total_cost:.6f}} ({{input_tokens:,}} in, {{output_tokens:,}} out)")
    print(f"📝 Response:")
    print(content)
    
    # Extract tool calls if any
    tool_calls = []
    if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            try:
                tool_calls.append({{
                    "id": tool_call.id,
                    "name": tool_call.function.name,
                    "input": json.loads(tool_call.function.arguments)
                }})
            except:
                pass
    
    if tool_calls:
        print(f"🔧 Tool calls: {{len(tool_calls)}}")
        for call in tool_calls:
            print(f"  - {{call['name']}}({{call['input']}})")
    
    # Return structured result
    result = {{
        "content": content,
        "tool_calls": tool_calls,
        "usage": {{
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_cost": total_cost
        }},
        "model": "{model.name}",
        "provider": "{provider.name}"
    }}
    
except Exception as e:
    print(f"❌ Error: {{str(e)}}")
    result = {{"error": str(e), "model": "{model.name}"}}

# SUCCESS! 🎉
result
'''
        return snippet.strip()
    
    def _create_gemini_snippet(
        self, model, provider, prompt, system_message, tools, max_tokens, temperature
    ) -> str:
        """PROVIDER: Generate Gemini SDK snippet"""
        
        snippet = f'''
# PRIMARY BUTTON: {model.display_name}
import google.generativeai as genai
import os
import json

# Configure Gemini
genai.configure(api_key=os.getenv("{provider.env_var}"))

# Initialize model
model = genai.GenerativeModel("{model.model_id}")

# Prepare content
content = "{prompt}"
'''

        if system_message:
            snippet += f'''
# Add system instruction
content = f"{system_message}\\n\\n" + content
'''

        snippet += f'''
# Make the API call
try:
    response = model.generate_content(
        content,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens={max_tokens},
            temperature={temperature}
        )
    )
    
    # Extract result
    result_text = response.text
    
    # Calculate cost (Gemini is often free!)
    # Note: Actual token counting would need Gemini's tokenizer
    estimated_input_tokens = len(content.split()) * 1.3  # Rough estimate
    estimated_output_tokens = len(result_text.split()) * 1.3
    input_cost = (estimated_input_tokens / 1_000_000) * {model.input_price}
    output_cost = (estimated_output_tokens / 1_000_000) * {model.output_price}
    total_cost = input_cost + output_cost
    
    # Print results
    print(f"🎯 Model: {model.display_name}")
    print(f"💰 Cost: ${{total_cost:.6f}} (Est. {{int(estimated_input_tokens):,}} in, {{int(estimated_output_tokens):,}} out)")
    print(f"📝 Response:")
    print(result_text)
    
    # Return structured result
    result = {{
        "content": result_text,
        "tool_calls": [],  # Tool support would need additional implementation
        "usage": {{
            "input_tokens": int(estimated_input_tokens),
            "output_tokens": int(estimated_output_tokens),
            "total_cost": total_cost
        }},
        "model": "{model.name}",
        "provider": "{provider.name}"
    }}
    
except Exception as e:
    print(f"❌ Error: {{str(e)}}")
    result = {{"error": str(e), "model": "{model.name}"}}

# SUCCESS! 🎉
result
'''
        return snippet.strip()
    
    @handle_errors(operation_name="create_workflow_snippet", return_dict=True)  
    def create_workflow_snippet(self, workflow_plan: Dict[str, Any]) -> str:
        """
        WORKFLOW: Generate complete workflow execution snippet
        """
        snippet = '''
# CORE WORKFLOW ORCHESTRATION
import asyncio
import json
from datetime import datetime

async def execute_workflow():
    """Execute complete multi-model workflow"""
    
    workflow_results = {}
    total_cost = 0.0
    
    print(f"WORKFLOW: Starting workflow: {workflow_plan.get('name', 'Unnamed')}")
    print(f"TIMESTAMP: Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
'''
        
        for phase_name, phase_config in workflow_plan.get("phases", {}).items():
            model_name = phase_config.get("model")
            prompt = phase_config.get("prompt", "")
            
            snippet += f'''
    
    # PHASE: {phase_name}
    print(f"\\nEXECUTING: {phase_name} with {model_name}")
    
    {self.create_api_call_snippet(model_name, prompt).replace("result", f"{phase_name}_result")}
    
    workflow_results["{phase_name}"] = {{phase_name}}_result
    if "usage" in {{phase_name}}_result:
        total_cost += {{phase_name}}_result["usage"].get("total_cost", 0)
    
    print(f"COMPLETED: {phase_name}")
'''
        
        snippet += f'''
    
    print("-" * 50)
    print(f"SUCCESS: Workflow completed!")
    print(f"COST: Total cost: ${{{total_cost:.6f}}}")
    print(f"TIMESTAMP: Finished at: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
    
    return workflow_results

# Execute the workflow
workflow_results = await execute_workflow()
workflow_results
'''
        return snippet.strip()
    
    @handle_errors(operation_name="create_tool_execution_snippet", return_dict=True)
    def create_tool_execution_snippet(self, tool_name: str, params: Dict[str, Any]) -> str:
        """
        TOOL: Generate tool execution snippet
        """
        return f'''
# TOOL EXECUTION: {tool_name}
import json

def execute_{tool_name}():
    """Execute {tool_name} with parameters"""
    
    params = {json.dumps(params, indent=4)}
    
    try:
        # Tool-specific implementation would go here
        # This is a placeholder for the actual tool logic
        
        if "{tool_name}" == "web_search":
            import requests
            query = params.get("query", "")
            response = requests.get("https://api.brave.com / search", 
                                  params={{"q": query}})
            result = response.json()
            
        elif "{tool_name}" == "file_operation":
            operation = params.get("operation", "read")
            file_path = params.get("file_path", "")
            
            if operation == "read":
                with open(file_path, 'r') as f:
                    result = f.read()
            elif operation == "write":
                content = params.get("content", "")
                with open(file_path, 'w') as f:
                    f.write(content)
                result = f"Written to {{file_path}}"
            else:
                result = f"Unknown operation: {{operation}}"
                
        else:
            result = f"Tool '{{tool_name}}' execution placeholder"
        
        print(f"TOOL: {{tool_name}} executed successfully")
        print(f"RESULT: {{result}}")
        
        return {{
            "success": True,
            "result": result,
            "tool": "{tool_name}",
            "params": params
        }}
        
    except Exception as e:
        print(f"ERROR: Tool {{tool_name}} failed: {{str(e)}}")
        return {{
            "success": False,
            "error": str(e),
            "tool": "{tool_name}",
            "params": params
        }}

# Execute the tool
tool_result = execute_{tool_name}()
tool_result
'''

    def get_execution_summary(self, model_name: str) -> str:
        """
        SUMMARY: Get a summary of what executing this model will do
        """
        model = self.models.get_model_config(model_name)
        provider = self.models.get_provider_for_model(model_name)
        
        if not model or not provider:
            return f"ERROR: Model '{model_name}' not found"
        
        summary = f"""
EXECUTION SUMMARY: {model.display_name}

Provider: {provider.display_name} ({provider.api_type})
Context Window: {model.context_window:,} tokens
Max Output: {model.max_output:,} tokens
Cost: ${model.input_price}/M input, ${model.output_price} / M output

Capabilities:
{"SUPPORTED" if model.capabilities.tools else "NOT SUPPORTED"} Tools
{"SUPPORTED" if model.capabilities.vision else "NOT SUPPORTED"} Vision  
{"SUPPORTED" if model.capabilities.caching else "NOT SUPPORTED"} Caching
{"SUPPORTED" if model.capabilities.code_execution else "NOT SUPPORTED"} Code Execution

Optimal for: {", ".join(model.optimal_use_cases)}
"""
        
        if model.privacy_note:
            summary += f"\nPRIVACY: {model.privacy_note}"
        
        return summary.strip()


# Example usage and testing
if __name__ == "__main__":
    from .manager_models import ModelManager
    
    # Initialize
    manager = ModelManager()
    buttons = ButtonManager(manager)
    
    print("BUTTON GENERATOR EXAMPLES:")
    print("=" * 50)
    
    # Example 1: General model usage
    available_models = manager.get_available_models()
    if available_models:
        example_model = available_models[0]['name']
        print(f"\\nTEST: Button Generation ({example_model}):")
        snippet = buttons.create_api_call_snippet(
            example_model, 
            "Test prompt for button generation"
        )
        print(snippet[:200] + "...")
        
        # Example 2: Execution summary
        print(f"\\nSUMMARY: Execution Details:")
        print(buttons.get_execution_summary(example_model))
    else:
        print("No models available for testing")