"""
PERPLEXITY SEARCH
Human Button Generators
"""

from typing import Dict, Any, List
import json

def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for Perplexity search operations
    Universal model compatibility via code generation
    
    Args:
        params: Perplexity search parameters
        model: Target model for code generation
        
    Returns:
        Executable code snippet for Claude 4 Code Execution Tool
    """
    operation = params.get("operation", "perplexity_search")
    
    if operation == "perplexity_search":
        return _create_basic_search_snippet(params, model)
    elif operation == "enhanced_perplexity_research":
        return _create_enhanced_research_snippet(params, model)
    elif operation == "perplexity_query_validation":
        return _create_validation_snippet(params, model)
    elif operation == "perplexity_research_suggestions":
        return _create_suggestions_snippet(params, model)
    elif operation == "api_configuration_check":
        return _create_api_check_snippet(params, model)
    else:
        return _create_generic_perplexity_snippet(params, model)

def _create_basic_search_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for basic Perplexity search"""
    query = params.get("query", "")
    perplexity_model = params.get("model", "llama-3.1-sonar-large-128k-online")
    search_context = params.get("search_context", "general")
    
    # Escape query for safe inclusion in code
    escaped_query = json.dumps(query)
    
    snippet = f'''
# Perplexity AI Search - Basic Search
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/Mao')

from tools.perplexity_search_modular import perform_perplexity_search
from interfaces.ui_tools.ui_perplexity_search import display_perplexity_result, display_search_execution_status
import requests
import json
import os
from datetime import datetime

# Prepare search configuration
search_config = perform_perplexity_search(
    query={escaped_query},
    model="{perplexity_model}",
    search_context="{search_context}"
)

# Display search preparation
display_perplexity_result(search_config, verbose=True)

if search_config.get("status") == "ready_for_execution":
    print("\\n🧠 Executing Perplexity AI Search...")
    display_search_execution_status(search_config["query"], "executing")
    
    try:
        # Check API key
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            print("❌ Perplexity API key not found")
            print("💡 Set PERPLEXITY_API_KEY environment variable")
            print("🔗 Get your API key at: https://www.perplexity.ai/settings/api")
        else:
            # Configure API request
            url = "https://api.perplexity.ai/chat/completions"
            headers = {{
                "Authorization": f"Bearer {{api_key}}",
                "Content-Type": "application/json"
            }}
            
            # Create context-aware prompt
            context_prompts = {{
                "general": f"Search for and analyze: {escaped_query}\\n\\nProvide comprehensive information with source citations, key insights, and practical implications.",
                "research": f"Conduct thorough research on: {escaped_query}\\n\\nFocus on authoritative sources, expert opinions, statistical data, and evidence-based insights. Include proper citations.",
                "analysis": f"Analyze and evaluate: {escaped_query}\\n\\nProvide multi-perspective analysis, pros and cons, implications, and expert viewpoints with source citations.",
                "current": f"Find current information about: {escaped_query}\\n\\nFocus on recent developments, latest news, and up-to-date information with publication dates.",
                "technical": f"Provide technical analysis of: {escaped_query}\\n\\nInclude technical specifications, implementation details, expert technical opinions, and credible technical sources.",
                "business": f"Analyze from business perspective: {escaped_query}\\n\\nInclude market analysis, business implications, industry trends, and strategic insights with reliable sources."
            }}
            
            search_prompt = context_prompts.get("{search_context}", context_prompts["general"])
            
            # API payload
            payload = {{
                "model": "{perplexity_model}",
                "messages": [
                    {{
                        "role": "system",
                        "content": "You are an expert AI research assistant. Provide comprehensive, well-sourced answers with proper citations. Focus on accuracy, credibility, and actionable insights."
                    }},
                    {{
                        "role": "user", 
                        "content": search_prompt
                    }}
                ],
                "max_tokens": 4000,
                "temperature": 0.1,
                "top_p": 0.9,
                "return_citations": True,
                "search_domain_filter": ["perplexity.ai"],
                "return_images": False,
                "return_related_questions": True,
                "search_recency_filter": "month",
                "top_k": 0,
                "stream": False,
                "presence_penalty": 0,
                "frequency_penalty": 1
            }}
            
            # Perform search with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = requests.post(url, headers=headers, json=payload, timeout=120)
                    
                    if response.status_code == 200:
                        break
                    elif response.status_code == 429:
                        if attempt < max_retries - 1:
                            print(f"⏱️ Rate limited, waiting {{(attempt + 1) * 10}} seconds...")
                            import time
                            time.sleep((attempt + 1) * 10)
                            continue
                    else:
                        print(f"⚠️ HTTP {{response.status_code}}: {{response.text[:200]}}")
                        if attempt < max_retries - 1:
                            import time
                            time.sleep(5)
                            continue
                            
                except requests.exceptions.Timeout:
                    print(f"⏱️ Request timeout (attempt {{attempt + 1}}/{{max_retries}})")
                    if attempt < max_retries - 1:
                        continue
                except Exception as req_error:
                    print(f"🌐 Request error: {{str(req_error)}}")
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(3)
                        continue
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract response content
                if "choices" in data and len(data["choices"]) > 0:
                    content = data["choices"][0]["message"]["content"]
                    
                    print("\\n" + "="*70)
                    print("🧠 PERPLEXITY AI ANALYSIS")
                    print("="*70)
                    print(f"Query: {{search_config['query']}}")
                    print(f"Model: {{search_config['model']}}")
                    print(f"Context: {{search_config['search_context'].title()}}")
                    print("="*70)
                    print(content)
                    
                    # Extract and display citations
                    citations = data.get("citations", [])
                    if citations:
                        print("\\n📚 SOURCES & CITATIONS")
                        print("="*70)
                        for i, citation in enumerate(citations, 1):
                            print(f"[{{i}}] {{citation}}")
                    
                    # Extract and display related questions
                    related_questions = data.get("related_questions", [])
                    if related_questions:
                        print("\\n❓ RELATED RESEARCH QUESTIONS")
                        print("="*70)
                        for question in related_questions:
                            print(f"• {{question}}")
                    
                    # Save comprehensive results
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    
                    search_results = {{
                        "query": search_config["query"],
                        "model": search_config["model"],
                        "search_context": search_config["search_context"],
                        "timestamp": datetime.now().isoformat(),
                        "response_content": content,
                        "citations": citations,
                        "related_questions": related_questions,
                        "usage": data.get("usage", {{}}),
                        "estimated_cost": search_config.get("estimated_cost", 0.025)
                    }}
                    
                    # Save JSON data
                    json_file = f"perplexity_search_{{search_config['search_context']}}_{{timestamp}}.json"
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(search_results, f, indent=2, ensure_ascii=False)
                    
                    # Save formatted report
                    report_file = f"perplexity_report_{{search_config['search_context']}}_{{timestamp}}.md"
                    with open(report_file, 'w', encoding='utf-8') as f:
                        f.write(f"# Perplexity AI Search Report\\n\\n")
                        f.write(f"**Query:** {{search_config['query']}}\\n")
                        f.write(f"**Model:** {{search_config['model']}}\\n")
                        f.write(f"**Context:** {{search_config['search_context'].title()}}\\n")
                        f.write(f"**Date:** {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}\\n\\n")
                        f.write("## AI Analysis\\n\\n")
                        f.write(content)
                        
                        if citations:
                            f.write("\\n\\n## Sources\\n\\n")
                            for i, citation in enumerate(citations, 1):
                                f.write(f"[{{i}}] {{citation}}\\n")
                        
                        if related_questions:
                            f.write("\\n\\n## Related Questions\\n\\n")
                            for question in related_questions:
                                f.write(f"- {{question}}\\n")
                    
                    print("\\n" + "="*70)
                    display_search_execution_status(search_config["query"], "completed")
                    print(f"💾 Results saved: {{json_file}}")
                    print(f"📄 Report saved: {{report_file}}")
                    print(f"💰 Estimated cost: ${{search_config.get('estimated_cost', 0.025):.3f}}")
                    
                else:
                    print("❌ No response content received")
                    
            else:
                display_search_execution_status(search_config["query"], "failed")
                print(f"❌ Search failed after {{max_retries}} attempts")
                
    except Exception as e:
        display_search_execution_status(search_config["query"], "failed")
        print(f"❌ Perplexity search failed: {{str(e)}}")

print("\\n" + "="*50)
print("PERPLEXITY SEARCH OPERATION COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def _create_enhanced_research_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for enhanced Perplexity research"""
    query = params.get("query", "")
    research_approach = params.get("research_approach", "comprehensive")
    analysis_focus = params.get("analysis_focus", "general")
    perplexity_model = params.get("model", "llama-3.1-sonar-large-128k-online")
    
    snippet = f'''
# Perplexity AI Search - Enhanced Research
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/Mao')

from tools.perplexity_search_modular import perform_enhanced_research
from interfaces.ui_tools.ui_perplexity_search import display_perplexity_result, display_search_execution_status, display_research_progress
import requests
import json
import os
from datetime import datetime

# Prepare enhanced research
research_config = perform_enhanced_research(
    query="{query}",
    research_approach="{research_approach}",
    analysis_focus="{analysis_focus}",
    model="{perplexity_model}"
)

# Display research preparation
display_perplexity_result(research_config, verbose=True)

if research_config.get("status") == "ready_for_execution":
    print("\\n🧠 Executing Enhanced Perplexity Research...")
    display_research_progress("preparing", "Setting up enhanced research parameters")
    
    try:
        # Check API key
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            print("❌ Perplexity API key not found")
            print("💡 Set PERPLEXITY_API_KEY environment variable")
        else:
            display_research_progress("querying", "Sending research query to Perplexity AI")
            
            # Configure API request
            url = "https://api.perplexity.ai/chat/completions"
            headers = {{
                "Authorization": f"Bearer {{api_key}}",
                "Content-Type": "application/json"
            }}
            
            # Create enhanced research prompt based on approach and focus
            enhanced_prompt = f"""Conduct {{research_config['research_approach']}} research on: {{research_config['query']}}

Research Focus: {{research_config['analysis_focus']}}

Please provide a structured analysis that includes:

1. **Executive Summary**
   - Key findings and main insights
   - Most important takeaways

2. **Detailed Analysis** 
   - Comprehensive information and context
   - Multiple perspectives and viewpoints
   - Current status and recent developments

3. **Evidence and Data**
   - Statistical information where available
   - Factual data and metrics
   - Expert opinions and quotes

4. **Implications and Impact**
   - Practical implications and applications
   - Future outlook and predictions
   - Potential challenges and opportunities

5. **Sources and Credibility**
   - Key sources used in analysis
   - Assessment of source reliability
   - Areas where more research may be needed

6. **Actionable Insights**
   - Practical recommendations
   - Next steps or further research directions
   - Key takeaways for decision-making

Ensure all information is current, well-sourced, and thoroughly analyzed with proper citations."""

            # API payload with enhanced parameters
            payload = {{
                "model": "{perplexity_model}",
                "messages": [
                    {{
                        "role": "system",
                        "content": f"You are an expert research analyst conducting {{research_config['research_approach']}} research with focus on {{research_config['analysis_focus']}}. Provide thorough, well-sourced, and actionable insights with comprehensive analysis."
                    }},
                    {{
                        "role": "user", 
                        "content": enhanced_prompt
                    }}
                ],
                "max_tokens": 6000,
                "temperature": 0.05,
                "top_p": 0.9,
                "return_citations": True,
                "search_domain_filter": ["perplexity.ai"],
                "return_images": False,
                "return_related_questions": True,
                "search_recency_filter": "month",
                "top_k": 0,
                "stream": False,
                "presence_penalty": 0,
                "frequency_penalty": 1
            }}
            
            display_research_progress("analyzing", "AI is conducting comprehensive analysis")
            
            # Perform enhanced research with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = requests.post(url, headers=headers, json=payload, timeout=180)
                    
                    if response.status_code == 200:
                        break
                    elif response.status_code == 429:
                        if attempt < max_retries - 1:
                            display_research_progress("preparing", f"Rate limited, waiting {{(attempt + 1) * 15}} seconds")
                            import time
                            time.sleep((attempt + 1) * 15)
                            continue
                    else:
                        print(f"⚠️ HTTP {{response.status_code}}: {{response.text[:200]}}")
                        if attempt < max_retries - 1:
                            import time
                            time.sleep(10)
                            continue
                            
                except requests.exceptions.Timeout:
                    display_research_progress("preparing", f"Request timeout (attempt {{attempt + 1}}/{{max_retries}})")
                    if attempt < max_retries - 1:
                        continue
                except Exception as req_error:
                    print(f"🌐 Request error: {{str(req_error)}}")
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(5)
                        continue
            
            if response.status_code == 200:
                display_research_progress("citing", "Processing results and citations")
                
                data = response.json()
                
                # Extract response content
                if "choices" in data and len(data["choices"]) > 0:
                    content = data["choices"][0]["message"]["content"]
                    
                    print("\\n" + "="*80)
                    print("🧠 ENHANCED PERPLEXITY RESEARCH RESULTS")
                    print("="*80)
                    print(f"Query: {{research_config['query']}}")
                    print(f"Research Approach: {{research_config['research_approach'].title()}}")
                    print(f"Analysis Focus: {{research_config['analysis_focus'].title()}}")
                    print(f"Model: {{research_config['model']}}")
                    print("="*80)
                    print(content)
                    
                    # Extract additional data
                    citations = data.get("citations", [])
                    related_questions = data.get("related_questions", [])
                    usage_info = data.get("usage", {{}})
                    
                    # Display citations
                    if citations:
                        print("\\n📚 RESEARCH SOURCES & CITATIONS")
                        print("="*80)
                        for i, citation in enumerate(citations, 1):
                            print(f"[{{i}}] {{citation}}")
                    
                    # Display related questions
                    if related_questions:
                        print("\\n❓ RELATED RESEARCH QUESTIONS")
                        print("="*80)
                        for question in related_questions:
                            print(f"• {{question}}")
                    
                    display_research_progress("finalizing", "Saving comprehensive research data")
                    
                    # Save comprehensive research data
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    
                    research_data = {{
                        "query": research_config["query"],
                        "research_approach": research_config["research_approach"],
                        "analysis_focus": research_config["analysis_focus"],
                        "model": research_config["model"],
                        "timestamp": datetime.now().isoformat(),
                        "research_content": content,
                        "citations": citations,
                        "related_questions": related_questions,
                        "usage": usage_info,
                        "estimated_cost": research_config.get("estimated_cost", 0.025),
                        "research_quality": {{
                            "citation_count": len(citations),
                            "content_length": len(content),
                            "related_questions_count": len(related_questions)
                        }}
                    }}
                    
                    # Save JSON data
                    json_file = f"enhanced_research_{{research_config['analysis_focus']}}_{{timestamp}}.json"
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(research_data, f, indent=2, ensure_ascii=False)
                    
                    # Save formatted research report
                    report_file = f"research_report_{{research_config['analysis_focus']}}_{{timestamp}}.md"
                    with open(report_file, 'w', encoding='utf-8') as f:
                        f.write(f"# Enhanced Research Report\\n\\n")
                        f.write(f"**Query:** {{research_config['query']}}\\n")
                        f.write(f"**Research Approach:** {{research_config['research_approach'].title()}}\\n")
                        f.write(f"**Analysis Focus:** {{research_config['analysis_focus'].title()}}\\n")
                        f.write(f"**Model:** {{research_config['model']}}\\n")
                        f.write(f"**Date:** {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}\\n\\n")
                        f.write("## Research Analysis\\n\\n")
                        f.write(content)
                        
                        if citations:
                            f.write("\\n\\n## Research Sources\\n\\n")
                            for i, citation in enumerate(citations, 1):
                                f.write(f"[{{i}}] {{citation}}\\n")
                        
                        if related_questions:
                            f.write("\\n\\n## Related Research Questions\\n\\n")
                            for question in related_questions:
                                f.write(f"- {{question}}\\n")
                    
                    display_research_progress("complete")
                    print("\\n" + "="*80)
                    print("✅ Enhanced research completed successfully")
                    print(f"💾 Data saved: {{json_file}}")
                    print(f"📄 Report saved: {{report_file}}")
                    print(f"💰 Estimated cost: ${{research_config.get('estimated_cost', 0.025):.3f}}")
                    print(f"📊 Quality metrics: {{len(citations)}} citations, {{len(content)}} chars, {{len(related_questions)}} related questions")
                    
                else:
                    print("❌ No research content received")
                    
            else:
                print(f"❌ Enhanced research failed after {{max_retries}} attempts")
                
    except Exception as e:
        print(f"❌ Enhanced research failed: {{str(e)}}")

print("\\n" + "="*50)
print("ENHANCED RESEARCH OPERATION COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def _create_validation_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for query validation"""
    query = params.get("query", "")
    
    snippet = f'''
# Perplexity AI Search - Query Validation
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/Mao')

from tools.perplexity_search_modular import validate_perplexity_query
from interfaces.ui_tools.ui_perplexity_search import display_perplexity_result

# Validate Perplexity query
validation_result = validate_perplexity_query("{query}")

# Display validation results
display_perplexity_result(validation_result, verbose=True)

# Additional validation insights
if validation_result.get("status") == "success":
    is_valid = validation_result.get("is_valid", False)
    issues = validation_result.get("issues", [])
    suggestions = validation_result.get("suggestions", [])
    estimated_quality = validation_result.get("estimated_quality", "unknown")
    
    print("\\n" + "="*60)
    print("PERPLEXITY QUERY VALIDATION SUMMARY")
    print("="*60)
    
    if is_valid:
        print("✅ Query is valid and optimized for Perplexity AI")
    else:
        print("❌ Query has issues that should be addressed")
    
    print(f"🎯 Estimated result quality: {{estimated_quality.title()}}")
    
    if issues:
        print("\\n⚠️ Issues identified:")
        for i, issue in enumerate(issues, 1):
            print(f"  {{i}}. {{issue}}")
    
    if suggestions:
        print("\\n💡 Optimization suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {{i}}. {{suggestion}}")
    
    print(f"\\n📊 Query analysis:")
    print(f"  • Word count: {{validation_result.get('word_count', 0)}}")
    print(f"  • Character count: {{validation_result.get('character_count', 0)}}")
    print(f"  • Question format: {{'Yes' if validation_result.get('has_question_format') else 'No'}}")
    print(f"  • Expected quality: {{estimated_quality.title()}}")
    
    print("\\n💡 Tips for better Perplexity results:")
    print("  • Frame queries as specific questions")
    print("  • Include context and background information")
    print("  • Specify the type of analysis you want")
    print("  • Ask for sources and citations")
    print("  • Be clear about the scope and depth needed")

print("\\n" + "="*50)
print("QUERY VALIDATION COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def _create_suggestions_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for research suggestions"""
    query = params.get("query", "")
    suggestion_type = params.get("suggestion_type", "enhancement")
    
    snippet = f'''
# Perplexity AI Search - Research Suggestions
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/Mao')

from tools.perplexity_search_modular import get_research_suggestions
from interfaces.ui_tools.ui_perplexity_search import display_perplexity_result

# Generate research suggestions
suggestions_result = get_research_suggestions(
    query="{query}",
    suggestion_type="{suggestion_type}"
)

# Display suggestions
display_perplexity_result(suggestions_result, verbose=True)

# Additional suggestion processing
if suggestions_result.get("status") == "success":
    suggestions = suggestions_result.get("suggestions", [])
    
    print("\\n" + "="*60)
    print("PERPLEXITY RESEARCH SUGGESTIONS SUMMARY")
    print("="*60)
    print(f"Original query: {{suggestions_result.get('original_query')}}")
    print(f"Suggestion type: {{suggestions_result.get('suggestion_type').title()}}")
    
    if suggestions:
        print(f"\\n📝 Generated {{len(suggestions)}} research suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {{i}}. {{suggestion}}")
        
        print("\\n💡 How to use these suggestions:")
        print("  • Copy any suggestion that interests you")
        print("  • Modify suggestions to fit your specific needs")
        print("  • Combine multiple suggestions for comprehensive research")
        print("  • Use different suggestion types for varied perspectives")
        
        print("\\n🎯 Available suggestion types:")
        print("  • enhancement - Improve and expand your query")
        print("  • analytical - Focus on analysis and evaluation")
        print("  • contextual - Add historical and contextual perspectives")
        print("  • practical - Focus on implementation and application")
        
    else:
        print("\\n⚠️ No suggestions could be generated for this query")
        print("💡 Try a different query or suggestion type")

print("\\n" + "="*50)
print("RESEARCH SUGGESTIONS COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def _create_api_check_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for API configuration check"""
    
    snippet = f'''
# Perplexity AI Search - API Configuration Check
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/Mao')

from tools.perplexity_search_modular import check_api_configuration, get_perplexity_capabilities
from interfaces.ui_tools.ui_perplexity_search import display_perplexity_result, display_perplexity_capabilities

# Check API configuration
config_result = check_api_configuration()

# Display configuration status
display_perplexity_result(config_result, verbose=True)

# Show capabilities
print("\\n")
capabilities = get_perplexity_capabilities()
display_perplexity_capabilities(capabilities)

# Additional setup guidance
print("\\n" + "="*60)
print("PERPLEXITY API SETUP GUIDE")
print("="*60)

if config_result.get("api_key_present"):
    print("✅ API key is configured and ready")
    print("🚀 You can now use Perplexity AI search operations")
else:
    print("❌ API key not found - setup required")
    print("\\n📋 Setup steps:")
    print("  1. Visit https://www.perplexity.ai/settings/api")
    print("  2. Create an account or sign in")
    print("  3. Generate an API key")
    print("  4. Set environment variable: export PERPLEXITY_API_KEY='your-key-here'")
    print("  5. Restart your terminal or IDE")
    
print("\\n💡 Usage tips:")
print("  • Start with basic searches to test your setup")
print("  • Use enhanced research for comprehensive analysis")
print("  • Validate queries before running expensive operations")
print("  • Monitor your API usage and costs")

print("\\n🔗 Useful links:")
print("  • API Documentation: https://docs.perplexity.ai/")
print("  • Pricing: https://www.perplexity.ai/settings/api")
print("  • Support: https://www.perplexity.ai/hub/getting-started")

print("\\n" + "="*50)
print("API CONFIGURATION CHECK COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def _create_generic_perplexity_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate generic Perplexity snippet"""
    operation = params.get("operation", "unknown")
    query = params.get("query", "")
    
    snippet = f'''
# Perplexity AI Search - Generic Operation
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/Mao')

from tools.perplexity_search_modular import *
from interfaces.ui_tools.ui_perplexity_search import display_perplexity_result, display_perplexity_capabilities

# Note: Operation '{operation}' not specifically implemented
# Available operations:
# - perplexity_search (basic AI search)
# - enhanced_perplexity_research (advanced research)
# - perplexity_query_validation (validate queries)
# - perplexity_research_suggestions (generate suggestions)
# - api_configuration_check (check API setup)

print("❌ Operation '{operation}' not recognized")
print("\\nAvailable Perplexity AI operations:")
print("• perplexity_search - Basic AI-powered search with reasoning")
print("• enhanced_perplexity_research - Advanced research with flexible approach")
print("• perplexity_query_validation - Validate query for optimal results")
print("• perplexity_research_suggestions - Generate query improvements")
print("• api_configuration_check - Check API setup and configuration")

# Show Perplexity capabilities
print("\\n🧠 Perplexity AI Capabilities:")
capabilities = get_perplexity_capabilities()
display_perplexity_capabilities(capabilities)

print("\\n" + "="*50)
print("PERPLEXITY OPERATION COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def create_multi_research_snippet(research_queries: List[Dict[str, Any]], model: str = "claude-sonnet-4") -> str:
    """
    Generate code snippet for multiple research operations
    
    Args:
        research_queries: List of research operations to perform
        model: Target model for code generation
        
    Returns:
        Executable code snippet for multiple research queries
    """
    snippet_parts = ['''
# Perplexity AI Search - Multiple Research Operations
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/Mao')

from tools.perplexity_search_modular import *
from interfaces.ui_tools.ui_perplexity_search import *
import requests
import json
import os
from datetime import datetime
import time

# Initialize research session
print("🚀 Starting Multi-Research Session")
print("="*80)

research_results = []
total_estimated_cost = 0
''']
    
    for i, research in enumerate(research_queries):
        operation = research.get("operation", "perplexity_search")
        query = research.get("query", "")
        
        snippet_parts.append(f'''
# Research {i+1}: {operation}
print(f"\\n🧠 Research {i+1}: {operation.replace('_', ' ').title()}")
print(f"Query: {query}")
''')
        
        if operation == "perplexity_search":
            perplexity_model = research.get("model", "llama-3.1-sonar-large-128k-online")
            search_context = research.get("search_context", "general")
            
            snippet_parts.append(f'''
research_config_{i} = perform_perplexity_search(
    query="{query}",
    model="{perplexity_model}",
    search_context="{search_context}"
)
display_perplexity_result(research_config_{i})
research_results.append(research_config_{i})
total_estimated_cost += research_config_{i}.get("estimated_cost", 0.025)
''')
        
        elif operation == "enhanced_perplexity_research":
            research_approach = research.get("research_approach", "comprehensive")
            analysis_focus = research.get("analysis_focus", "general")
            perplexity_model = research.get("model", "llama-3.1-sonar-large-128k-online")
            
            snippet_parts.append(f'''
research_config_{i} = perform_enhanced_research(
    query="{query}",
    research_approach="{research_approach}",
    analysis_focus="{analysis_focus}",
    model="{perplexity_model}"
)
display_perplexity_result(research_config_{i})
research_results.append(research_config_{i})
total_estimated_cost += research_config_{i}.get("estimated_cost", 0.025)
''')
    
    snippet_parts.append('''
# Session summary
print("\\n" + "="*80)
print("MULTI-RESEARCH SESSION SUMMARY")
print("="*80)
print(f"Total research queries: {len(research_results)}")
print(f"Total estimated cost: ${total_estimated_cost:.3f}")

successful_research = [r for r in research_results if r.get("status") == "ready_for_execution"]
print(f"Successful preparations: {len(successful_research)}")

if successful_research:
    print("\\n✅ All research queries prepared successfully")
    print("💡 Execute individual research snippets to perform actual research")
    print("🧠 Perplexity AI will provide comprehensive analysis with citations")
else:
    print("\\n⚠️ Some research queries had preparation issues")

print("="*80)
''')
    
    return '\\n'.join(snippet_parts).strip()

def get_model_compatibility_info() -> Dict[str, Any]:
    """
    Get information about model compatibility for Perplexity operations
    
    Returns:
        Dict with compatibility information
    """
    return {
        "supported_models": [
            "llama-3.1-sonar-small-128k-online",
            "llama-3.1-sonar-large-128k-online",
            "llama-3.1-sonar-huge-128k-online"
        ],
        "operation_costs": {
            "perplexity_search": 0.025,
            "enhanced_perplexity_research": 0.038,
            "perplexity_query_validation": 0.001,
            "perplexity_research_suggestions": 0.002,
            "api_configuration_check": 0.000
        },
        "features": {
            "ai_reasoning": True,
            "source_citations": True,
            "real_time_information": True,
            "comprehensive_analysis": True,
            "related_questions": True,
            "multi_perspective_analysis": True
        },
        "limitations": {
            "requires_api_key": True,
            "rate_limits": "subject_to_perplexity_api_limits",
            "max_query_length": 500,
            "timeout_seconds": 180,
            "max_tokens": 6000
        },
        "api_requirements": {
            "endpoint": "https://api.perplexity.ai/chat/completions",
            "authentication": "Bearer token",
            "environment_variable": "PERPLEXITY_API_KEY",
            "signup_url": "https://www.perplexity.ai/settings/api"
        }
    } 