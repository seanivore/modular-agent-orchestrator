"""
SFA v4 Perplexity Search Tool
AI-powered search with reasoning and source citations
"""

import json
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime

def get_tool_definition() -> Dict[str, Any]:
    """Standard tool definition for OC discovery"""
    return {
        "id": "perplexity_search",
        "name": "Perplexity AI Search", 
        "description": "AI-powered search with reasoning and comprehensive analysis",
        "capabilities": ["ai_search", "research", "analysis", "reasoning", "source_citation"],
        "use_cases": ["complex research", "analytical queries", "reasoning tasks", "comprehensive analysis"],
        "cost_estimate": 0.02,  # Estimated per search
        "model_compatibility": ["all"],
        "tags": ["research", "ai", "analysis", "reasoning", "premium"],
        "parameters": {
            "query": {"type": "string", "required": True, "description": "Search/research query"},
            "model": {"type": "string", "default": "llama-3.1-sonar-large-128k-online", "description": "Perplexity model to use"}
        }
    }

def perplexity_search(query: str, model: str = "llama-3.1-sonar-large-128k-online") -> str:
    """
    Perform AI-powered search using Perplexity API
    This is a placeholder - actual implementation via human button
    """
    return f"""
🧠 Perplexity AI Search
🎯 Query: "{query}"
🤖 Model: {model}
⏰ Started: {datetime.now().strftime('%H:%M:%S')}

🎯 Perplexity Features:
- AI-powered analysis and reasoning
- Real-time web information
- Source citations and references  
- Comprehensive responses
- Advanced reasoning capabilities

Note: Execute the human button snippet for actual Perplexity search.
"""

def create_human_button_snippet(params: Dict, model: str = "claude-sonnet-4") -> str:
    """Generate executable snippet for Perplexity search"""
    query = params.get("query", "")
    perplexity_model = params.get("model", "llama-3.1-sonar-large-128k-online")
    
    return f'''
# Perplexity AI Search
import requests
import json
from datetime import datetime

# Search parameters
query = "{query}"
perplexity_model = "{perplexity_model}"

print(f"🧠 Perplexity AI Search: {{query}}")
print(f"🤖 Model: {{perplexity_model}}")
print("="*70)

try:
    # Perplexity API endpoint
    url = "https://api.perplexity.ai/chat/completions"
    
    # Headers (API key should be in environment)
    headers = {{
        "Authorization": "Bearer YOUR_PERPLEXITY_API_KEY",  # Replace with actual key
        "Content-Type": "application/json"
    }}
    
    # Request payload
    payload = {{
        "model": perplexity_model,
        "messages": [
            {{
                "role": "system",
                "content": "You are a helpful research assistant. Provide comprehensive, well-sourced answers with proper citations."
            }},
            {{
                "role": "user", 
                "content": query
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
    
    # Perform search
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract response content
        if "choices" in data and len(data["choices"]) > 0:
            content = data["choices"][0]["message"]["content"]
            
            print("🎯 PERPLEXITY ANALYSIS")
            print("="*70)
            print(content)
            
            # Extract citations if available
            if "citations" in data:
                citations = data["citations"]
                if citations:
                    print("\\n📚 SOURCES & CITATIONS")
                    print("="*70)
                    for i, citation in enumerate(citations, 1):
                        print(f"[{{i}}] {{citation}}")
            
            # Extract related questions if available
            if "related_questions" in data:
                related = data["related_questions"]
                if related:
                    print("\\n❓ RELATED QUESTIONS")
                    print("="*70)
                    for question in related:
                        print(f"• {{question}}")
            
            # Save comprehensive results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            results_file = f"perplexity_search_{{timestamp}}.json"
            
            search_results = {{
                "query": query,
                "model": perplexity_model,
                "timestamp": datetime.now().isoformat(),
                "response": content,
                "citations": data.get("citations", []),
                "related_questions": data.get("related_questions", []),
                "usage": data.get("usage", {{}})
            }}
            
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(search_results, f, indent=2, ensure_ascii=False)
            
            # Also save readable markdown version
            markdown_file = f"perplexity_analysis_{{timestamp}}.md"
            with open(markdown_file, 'w', encoding='utf-8') as f:
                f.write(f"# Perplexity AI Analysis\\n\\n")
                f.write(f"**Query:** {{query}}\\n")
                f.write(f"**Model:** {{perplexity_model}}\\n")
                f.write(f"**Date:** {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}\\n\\n")
                f.write("## Analysis\\n\\n")
                f.write(content)
                
                if data.get("citations"):
                    f.write("\\n\\n## Sources\\n\\n")
                    for i, citation in enumerate(data["citations"], 1):
                        f.write(f"[{{i}}] {{citation}}\\n")
                
                if data.get("related_questions"):
                    f.write("\\n\\n## Related Questions\\n\\n")
                    for question in data["related_questions"]:
                        f.write(f"- {{question}}\\n")
            
            print("\\n" + "="*70)
            print("✅ Perplexity search completed")
            print(f"💾 Results saved to: {{results_file}}")
            print(f"📄 Markdown saved to: {{markdown_file}}")
            
        else:
            print("❌ No response content received")
            
    else:
        print(f"❌ Perplexity search failed: HTTP {{response.status_code}}")
        print(f"Error: {{response.text}}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ Network error: {{str(e)}}")
except Exception as e:
    print(f"❌ Perplexity search failed: {{str(e)}}")
    
def research_topic(topic: str, depth: str = "comprehensive") -> str:
    """Conduct in-depth research on a topic"""
    return f"""
📚 Perplexity Topic Research
🎯 Topic: "{topic}"
📊 Depth: {depth}

Use the human button snippet for comprehensive topic research.
"""

def create_research_snippet(params: Dict, model: str = "claude-sonnet-4") -> str:
    """Generate snippet for topic research"""
    topic = params.get("topic", "")
    depth = params.get("depth", "comprehensive")
    
    research_prompts = {
        "comprehensive": f"Provide a comprehensive analysis of {topic}. Include current trends, key developments, major players, challenges, opportunities, and future outlook. Use recent sources and provide detailed citations.",
        "quick": f"Give me a concise but informative overview of {topic}. Focus on the most important current information and key facts.",
        "technical": f"Provide a technical deep-dive into {topic}. Include detailed mechanisms, processes, specifications, and expert-level insights with proper citations.",
        "business": f"Analyze {topic} from a business perspective. Include market size, key players, business models, opportunities, challenges, and strategic insights."
    }
    
    research_query = research_prompts.get(depth, research_prompts["comprehensive"])
    
    return create_human_button_snippet({"query": research_query}, model)

def compare_topics(topic1: str, topic2: str, comparison_type: str = "general") -> str:
    """Compare two topics using AI analysis"""
    return f"""
⚖️ Perplexity Topic Comparison
🎯 Topic 1: "{topic1}"
🎯 Topic 2: "{topic2}"
📊 Type: {comparison_type}

Use the human button snippet for AI-powered comparison.
"""

def create_comparison_snippet(params: Dict, model: str = "claude-sonnet-4") -> str:
    """Generate snippet for topic comparison"""
    topic1 = params.get("topic1", "")
    topic2 = params.get("topic2", "")
    comparison_type = params.get("comparison_type", "general")
    
    comparison_query = f"Compare and contrast {topic1} vs {topic2}. Provide a detailed analysis including similarities, differences, advantages and disadvantages of each, use cases, and recommendations. Focus on {comparison_type} aspects and use recent sources with proper citations."
    
    return create_human_button_snippet({"query": comparison_query}, model)

def analyze_trends(topic: str, timeframe: str = "current") -> str:
    """Analyze trends related to a topic"""
    return f"""
📈 Perplexity Trend Analysis
🎯 Topic: "{topic}"
⏰ Timeframe: {timeframe}

Use the human button snippet for comprehensive trend analysis.
"""

def create_trends_snippet(params: Dict, model: str = "claude-sonnet-4") -> str:
    """Generate snippet for trend analysis"""
    topic = params.get("topic", "")
    timeframe = params.get("timeframe", "current")
    
    timeframe_modifiers = {
        "current": "current and emerging trends",
        "yearly": "trends over the past year",
        "historical": "historical trends and evolution",
        "future": "predicted future trends and forecasts"
    }
    
    modifier = timeframe_modifiers.get(timeframe, "current trends")
    trends_query = f"Analyze the {modifier} related to {topic}. Include statistical data, growth patterns, market dynamics, key drivers, and expert predictions. Use the most recent data available and provide detailed citations."
    
    return create_human_button_snippet({"query": trends_query}, model)

# Tool registration for OC discovery
TOOL_DEFINITION = get_tool_definition()

# Available search functions
PERPLEXITY_FUNCTIONS = {
    "perplexity_search": perplexity_search,
    "research_topic": research_topic,
    "compare_topics": compare_topics,
    "analyze_trends": analyze_trends
}

"""
PULL FROM OLD SFA: 
"""

# SFA v4.0.0 Enhanced Tools - Complete Implementation
# Extracted best patterns from v3.3.0 and enhanced for v4 architecture

# =============================================================================
# ENHANCED PERPLEXITY SEARCH TOOL
# =============================================================================

"""
Enhanced SFA v4 Perplexity Search Tool with advanced research capabilities
"""

def get_enhanced_perplexity_definition() -> Dict[str, Any]:
    """Enhanced Perplexity search definition"""
    return {
        "id": "perplexity_search_enhanced",
        "name": "Advanced Perplexity Research",
        "description": "AI-powered research with comprehensive analysis and source verification",
        "capabilities": ["ai_search", "research", "analysis", "reasoning", "source_citation", "fact_checking"],
        "use_cases": ["complex research", "analytical queries", "trend analysis", "competitive intelligence"],
        "cost_estimate": 0.02,
        "model_compatibility": ["all"],
        "tags": ["research", "ai", "analysis", "reasoning", "premium", "enhanced"],
        "parameters": {
            "query": {"type": "string", "required": True, "description": "Research query"},
            "research_depth": {"type": "string", "default": "comprehensive", "description": "Depth of research"},
            "focus_area": {"type": "string", "default": "general", "description": "Specific focus area"}
        }
    }

def create_enhanced_perplexity_snippet(params: Dict, model: str = "claude-sonnet-4") -> str:
    """Generate enhanced Perplexity research snippet"""
    
    query = params.get("query", "")
    research_depth = params.get("research_depth", "comprehensive")
    focus_area = params.get("focus_area", "general")
    
    return f'''
# Advanced Perplexity Research with Enhanced Analysis
import requests
import json
from datetime import datetime
import os

def advanced_perplexity_research():
    """Conduct advanced research using Perplexity with enhanced analysis"""
    
    query = "{query}"
    research_depth = "{research_depth}"
    focus_area = "{focus_area}"
    
    print(f"🧠 Advanced Perplexity Research")
    print(f"🎯 Query: {{query}}")
    print(f"📊 Depth: {{research_depth}}")
    print(f"🔍 Focus: {{focus_area}}")
    print("="*80)
    
    try:
        # Check API key
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            print("❌ Perplexity API key not found")
            print("Set PERPLEXITY_API_KEY environment variable")
            return None
        
        # Research depth configurations
        depth_configs = {{
            "quick": {{
                "model": "llama-3.1-sonar-small-128k-online",
                "max_tokens": 2000,
                "temperature": 0.1
            }},
            "comprehensive": {{
                "model": "llama-3.1-sonar-large-128k-online",
                "max_tokens": 4000,
                "temperature": 0.1
            }},
            "academic": {{
                "model": "llama-3.1-sonar-huge-128k-online",
                "max_tokens": 6000,
                "temperature": 0.05
            }}
        }}
        
        config = depth_configs.get(research_depth, depth_configs["comprehensive"])
        
        # Focus area prompts
        focus_prompts = {{
            "business": f"Analyze {{query}} from a business perspective. Include market analysis, competitive landscape, business models, revenue potential, industry trends, and strategic implications.",
            
            "technical": f"Provide technical analysis of {{query}}. Include technical specifications, implementation details, performance metrics, technical challenges, and expert technical opinions.",
            
            "academic": f"Research {{query}} with academic rigor. Include peer-reviewed sources, research studies, academic theories, statistical data, and scholarly perspectives.",
            
            "competitive": f"Conduct competitive intelligence research on {{query}}. Include competitor analysis, market positioning, competitive advantages, industry benchmarks, and strategic insights.",
            
            "trends": f"Analyze current and emerging trends related to {{query}}. Include market trends, technological developments, consumer behavior patterns, and future predictions.",
            
            "general": f"Conduct comprehensive research on {{query}}. Include current information, expert opinions, different perspectives, factual data, and practical implications."
        }}
        
        # Create enhanced research prompt
        base_prompt = focus_prompts.get(focus_area, focus_prompts["general"])
        
        enhanced_prompt = f"""{{base_prompt}}

Please structure your response with:

1. EXECUTIVE SUMMARY
   - Key findings in 2-3 sentences
   - Most important insights

2. DETAILED ANALYSIS
   - Comprehensive information and insights
   - Multiple perspectives and viewpoints
   - Current status and recent developments

3. DATA AND EVIDENCE
   - Statistical information where available
   - Factual data and metrics
   - Expert quotes and opinions

4. IMPLICATIONS AND IMPACT
   - Practical implications
   - Future outlook and predictions
   - Potential challenges and opportunities

5. SOURCES AND CREDIBILITY
   - List key sources used
   - Assess source credibility
   - Note any information gaps

6. RECOMMENDATIONS
   - Actionable insights
   - Further research suggestions
   - Key takeaways

Ensure all information is current, well-sourced, and thoroughly analyzed."""

        # API configuration
        url = "https://api.perplexity.ai/chat/completions"
        headers = {{
            "Authorization": f"Bearer {{api_key}}",
            "Content-Type": "application/json"
        }}
        
        payload = {{
            "model": config["model"],
            "messages": [
                {{
                    "role": "system",
                    "content": f"You are an expert researcher conducting {{research_depth}} analysis. Provide thorough, well-sourced, and actionable insights."
                }},
                {{
                    "role": "user", 
                    "content": enhanced_prompt
                }}
            ],
            "max_tokens": config["max_tokens"],
            "temperature": config["temperature"],
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
        
        print("🔍 Conducting advanced research...")
        
        # Perform research with retry logic
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
        
        if response.status_code != 200:
            print(f"❌ Research failed after {{max_retries}} attempts")
            return None
        
        # Process results
        data = response.json()
        
        if "choices" not in data or not data["choices"]:
            print("❌ No research results received")
            return None
        
        research_content = data["choices"][0]["message"]["content"]
        
        print("🎯 ADVANCED RESEARCH RESULTS")
        print("="*80)
        print(research_content)
        
        # Extract additional data
        citations = data.get("citations", [])
        related_questions = data.get("related_questions", [])
        usage_info = data.get("usage", {{}})
        
        # Display citations
        if citations:
            print("\\n📚 SOURCES & CITATIONS")
            print("="*80)
            for i, citation in enumerate(citations, 1):
                print(f"[{{i}}] {{citation}}")
        
        # Display related questions
        if related_questions:
            print("\\n❓ RELATED RESEARCH QUESTIONS")
            print("="*80)
            for question in related_questions:
                print(f"• {{question}}")
        
        # Save comprehensive research data
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        research_data = {{
            "query": query,
            "research_depth": research_depth,
            "focus_area": focus_area,
            "timestamp": datetime.now().isoformat(),
            "model_used": config["model"],
            "research_content": research_content,
            "citations": citations,
            "related_questions": related_questions,
            "usage": usage_info,
            "research_quality": {{
                "citation_count": len(citations),
                "content_length": len(research_content),
                "related_questions_count": len(related_questions)
            }}
        }}
        
        # Save JSON data
        json_file = f"perplexity_research_{{focus_area}}_{{timestamp}}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(research_data, f, indent=2, ensure_ascii=False)
        
        # Save formatted research report
        report_file = f"research_report_{{focus_area}}_{{timestamp}}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# Advanced Research Report\\n\\n")
            f.write(f"**Research Query:** {{query}}\\n")
            f.write(f"**Focus Area:** {{focus_area}}\\n")
            f.write(f"**Research Depth:** {{research_depth}}\\n")
            f.write(f"**Model:** {{config['model']}}\\n")
            f.write(f"**Date:** {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}\\n\\n")
            
            f.write("## Research Analysis\\n\\n")
            f.write(research_content)
            
            if citations:
                f.write("\\n\\n## Sources\\n\\n")
                for i, citation in enumerate(citations, 1):
                    f.write(f"[{{i}}] {{citation}}\\n")
            
            if related_questions:
                f.write("\\n\\n## Related Research Questions\\n\\n")
                for question in related_questions:
                    f.write(f"- {{question}}\\n")
        
        print("\\n" + "="*80)
        print("✅ Advanced research completed successfully")
        print(f"💾 Data: {{json_file}}")
        print(f"📄 Report: {{report_file}}")
        print(f"📊 Citations: {{len(citations)}} | Related Questions: {{len(related_questions)}}")
        
        return research_data
        
    except Exception as e:
        print(f"❌ Advanced research failed: {{str(e)}}")
        return None

# Execute advanced Perplexity research
result = advanced_perplexity_research()
if result:
    print("\\n🎯 Research completed successfully")
    print(f"📊 Quality Score: {{result['research_quality']}}")
else:
    print("\\n❌ Research failed")
'''
