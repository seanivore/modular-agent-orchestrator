#!/usr/bin/env python3
"""
Dual-layer Hybrid Caching System
Files API for workflow handoffs and Local cache for permanence; fingerprinting 
"""

import json
import hashlib
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict

# Standard MAO imports
from ..error_handling import handle_errors, retry_with_backoff, APIError


@dataclass
class CacheEntry:
    """A cached item with metadata"""
    content: str
    created_at: str
    content_hash: str
    cache_type: str
    expires_at: Optional[str] = None


class CacheManager:
    """🔄 Dual-layer caching: Files API + Local fingerprinting"""
    
    def __init__(self, cache_dir: str = "./.cache", verbose: bool = False):
        self.cache_dir = Path(cache_dir).expanduser()
        self.cache_dir.mkdir(exist_ok=True)
        self.verbose = verbose
        
        # Create cache subdirectories
        (self.cache_dir / "content_analysis").mkdir(exist_ok=True)
        (self.cache_dir / "tool_definitions").mkdir(exist_ok=True)
        (self.cache_dir / "workflow_memory").mkdir(exist_ok=True)
        
        # Active workflow file tracking
        self.workflow_files: Dict[str, str] = {}  # file_id -> content_hash
        self.session_memory: Dict[str, Any] = {}
        
        if self.verbose:
            print(f"💾 Cache initialized at {self.cache_dir}")
    
    def generate_content_hash(self, content: str) -> str:
        """📄 Generate fingerprint for content"""
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def generate_tool_hash(self, tool_name: str, tool_definition: Dict) -> str:
        """🔧 Generate fingerprint for tool definition"""
        tool_content = f"{tool_name}_{json.dumps(tool_definition, sort_keys=True)}"
        return hashlib.md5(tool_content.encode()).hexdigest()[:12]
    
    # ========================================================================
    # LAYER 1: LOCAL FINGERPRINT CACHE (Permanent)
    # ========================================================================
    
    @handle_errors(operation_name="cache_content_analysis", return_dict=False)
    def cache_content_analysis(self, cache_key: str, content: str, component_name: str) -> None:
        """💾 Cache content analysis using MAO standard key format"""
        key_hash = self.generate_content_hash(cache_key)
        
        cache_entry = CacheEntry(
            content=content,
            created_at=datetime.now().isoformat(),
            content_hash=key_hash,
            cache_type=component_name
        )
        
        cache_file = self.cache_dir / component_name / f"{key_hash}.json"
        cache_file.parent.mkdir(exist_ok=True)  # Ensure directory exists
        with open(cache_file, 'w') as f:
            json.dump(asdict(cache_entry), f, indent=2)
        
        if self.verbose:
            print(f"💾 Cached {cache_key} ({component_name})")
    
    def cache_content_analysis_legacy(self, content: str, analysis: str, cache_type: str = "content_analysis") -> str:
        """💾 Legacy method for backward compatibility"""
        content_hash = self.generate_content_hash(content)
        
        cache_entry = CacheEntry(
            content=analysis,
            created_at=datetime.now().isoformat(),
            content_hash=content_hash,
            cache_type=cache_type
        )
        
        cache_file = self.cache_dir / cache_type / f"{content_hash}.json"
        cache_file.parent.mkdir(exist_ok=True)  # Ensure directory exists
        with open(cache_file, 'w') as f:
            json.dump(asdict(cache_entry), f, indent=2)
        
        if self.verbose:
            print(f"💾 Cached {cache_type}: {content_hash}")
        return content_hash
    
    @handle_errors(operation_name="get_cached_analysis", return_dict=False)
    def get_cached_analysis(self, cache_key: str, component_name: str) -> Optional[str]:
        """📄 Get cached content analysis using MAO standard key format"""
        # Generate file-safe cache key hash
        key_hash = self.generate_content_hash(cache_key)
        cache_file = self.cache_dir / component_name / f"{key_hash}.json"
        
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                cache_entry = json.load(f)
            
            if self.verbose:
                print(f"💾 Cache HIT: {cache_key} ({component_name})")
            return cache_entry["content"]
        
        if self.verbose:
            print(f"💾 Cache MISS: {cache_key} ({component_name})")
        return None
    
    def get_cached_analysis_legacy(self, content: str, cache_type: str = "content_analysis") -> Optional[str]:
        """📄 Legacy method for backward compatibility"""
        content_hash = self.generate_content_hash(content)
        cache_file = self.cache_dir / cache_type / f"{content_hash}.json"
        
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                cache_entry = json.load(f)
            
            if self.verbose:
                print(f"💾 Cache HIT: {content_hash} ({cache_type})")
            return cache_entry["content"]
        
        if self.verbose:
            print(f"💾 Cache MISS: {content_hash} ({cache_type})")
        return None
    
    def cache_tool_definition(self, tool_name: str, tool_definition: Dict) -> str:
        """🔧 Cache tool definition permanently"""
        tool_hash = self.generate_tool_hash(tool_name, tool_definition)
        
        cache_entry = CacheEntry(
            content=json.dumps(tool_definition),
            created_at=datetime.now().isoformat(),
            content_hash=tool_hash,
            cache_type="tool_definition"
        )
        
        cache_file = self.cache_dir / "tool_definitions" / f"{tool_name}_{tool_hash}.json"
        with open(cache_file, 'w') as f:
            json.dump(asdict(cache_entry), f, indent=2)
        
        if self.verbose:
            print(f"🔧 Cached tool: {tool_name} ({tool_hash})")
        return tool_hash
    
    def get_cached_tool(self, tool_name: str, tool_definition: Dict) -> Optional[Dict]:
        """🔧 Get cached tool definition"""
        tool_hash = self.generate_tool_hash(tool_name, tool_definition)
        cache_file = self.cache_dir / "tool_definitions" / f"{tool_name}_{tool_hash}.json"
        
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                cache_entry = json.load(f)
            
            if self.verbose:
                print(f"🔧 Tool cache HIT: {tool_name} ({tool_hash})")
            return json.loads(cache_entry["content"])
        
        if self.verbose:
            print(f"🔧 Tool cache MISS: {tool_name} ({tool_hash})")
        return None
    
    # ========================================================================
    # LAYER 2: FILES API WORKFLOW HANDOFFS (Free Inter-Agent Communication)
    # ========================================================================
    
    @handle_errors(operation_name="store_workflow_file", return_dict=False)
    @retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(APIError,))
    async def store_workflow_file(self, content: str, filename: str, anthropic_client) -> str:
        """📁 Store content in Files API for free inter-agent handoffs"""
        try:
            # Create file in Anthropic Files API
            file_response = await anthropic_client.files.create(
                content=content.encode(),
                name=filename,
                type="text/plain"
            )
            
            file_id = file_response.id
            content_hash = self.generate_content_hash(content)
            
            # Track for this workflow session
            self.workflow_files[file_id] = content_hash
            
            if self.verbose:
                print(f"📁 Stored in Files API: {filename} (ID: {file_id[:8]}...)")
            return file_id
            
        except Exception as e:
            if self.verbose:
                print(f"❌ Files API error: {e}")
            # Fallback to session memory
            self.session_memory[filename] = content
            return f"session_{filename}"
    
    async def retrieve_workflow_file(self, file_id: str, anthropic_client) -> Optional[str]:
        """📁 Retrieve content from Files API (FREE!)"""
        if file_id.startswith("session_"):
            # Fallback session memory
            filename = file_id.replace("session_", "")
            return self.session_memory.get(filename)
        
        try:
            file_content = await anthropic_client.files.retrieve(file_id)
            if self.verbose:
                print(f"📁 Retrieved from Files API: {file_id[:8]}... (FREE!)")
            return file_content.decode()
            
        except Exception as e:
            if self.verbose:
                print(f"❌ Files API retrieval error: {e}")
            return None
    
    def build_workflow_memory(self, completed_phases: List[Dict]) -> Dict[str, Any]:
        """🧠 Build condensed workflow memory for context passing"""
        memory = {
            "workflow_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "completed_phases": [],
            "key_insights": [],
            "file_references": {}
        }
        
        for phase in completed_phases:
            phase_summary = {
                "name": phase["name"],
                "model": phase["model"],
                "key_outputs": phase.get("key_outputs", []),
                "cost": phase.get("cost", 0),
                "file_ids": phase.get("file_ids", [])
            }
            memory["completed_phases"].append(phase_summary)
            
            # Extract key insights for context
            if phase.get("insights"):
                memory["key_insights"].extend(phase["insights"])
        
        return memory
    
    # ========================================================================
    # LAYER 3: SMART CACHE DECISIONS
    # ========================================================================
    
    def should_cache_permanently(self, content_type: str, content_size: int) -> bool:
        """🎯 Decide if content should be permanently cached"""
        cache_rules = {
            "job_description": content_size > 100,  # Always cache job descriptions
            "research_results": content_size > 500,  # Cache substantial research
            "tool_definition": True,  # Always cache tool definitions
            "workflow_memory": content_size > 200,  # Cache workflow summaries
            "analysis": content_size > 300  # Cache analysis results
        }
        
        return cache_rules.get(content_type, content_size > 1000)
    
    async def smart_cache_decision(self, content: str, content_type: str, 
                                 filename: str, anthropic_client) -> Dict[str, str]:
        """🧠 Smart caching decision: permanent vs workflow-only"""
        content_size = len(content)
        
        result = {
            "permanent_cache": None,
            "workflow_file_id": None,
            "strategy": ""
        }
        
        # Decision 1: Permanent cache for reusable content
        if self.should_cache_permanently(content_type, content_size):
            content_hash = self.cache_content_analysis(content, content, content_type)
            result["permanent_cache"] = content_hash
            result["strategy"] += "permanent+"
        
        # Decision 2: Files API for workflow handoffs
        file_id = await self.store_workflow_file(content, filename, anthropic_client)
        result["workflow_file_id"] = file_id
        result["strategy"] += "workflow"
        
        if self.verbose:
            print(f"🧠 Smart cache: {content_type} → {result['strategy']}")
        return result
    
    # ========================================================================
    # CACHE MANAGEMENT
    # ========================================================================
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """📊 Get cache statistics"""
        stats = {
            "cache_dir": str(self.cache_dir),
            "total_size_mb": 0,
            "content_analysis": 0,
            "tool_definitions": 0,
            "workflow_memory": 0,
            "active_workflow_files": len(self.workflow_files)
        }
        
        for cache_type in ["content_analysis", "tool_definitions", "workflow_memory"]:
            cache_path = self.cache_dir / cache_type
            if cache_path.exists():
                files = list(cache_path.glob("*.json"))
                stats[cache_type] = len(files)
                
                # Calculate size
                for file in files:
                    stats["total_size_mb"] += file.stat().st_size
        
        stats["total_size_mb"] = round(stats["total_size_mb"] / (1024 * 1024), 2)
        return stats
    
    def cleanup_old_cache(self, days_old: int = 30):
        """Clean up old cache entries"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        cleaned = 0
        
        for cache_type in ["content_analysis", "tool_definitions", "workflow_memory"]:
            cache_path = self.cache_dir / cache_type
            if not cache_path.exists():
                continue
                
            for cache_file in cache_path.glob("*.json"):
                try:
                    with open(cache_file, 'r') as f:
                        cache_entry = json.load(f)
                    
                    created_at = datetime.fromisoformat(cache_entry["created_at"])
                    if created_at < cutoff_date:
                        cache_file.unlink()
                        cleaned += 1
                        
                except Exception as e:
                    if self.verbose:
                        print(f"Warning: Error cleaning {cache_file}: {e}")
        
        if self.verbose:
            print(f"Cleaned {cleaned} old cache entries")
        return cleaned

    @handle_errors(operation_name="estimate_cost", return_dict=True)
    def estimate_cost(self, params: Dict[str, Any] = None) -> float:
        """Estimate cache operation cost for budget planning"""
        base_cost = 0.001  # Base cache cost (very low)
        
        if params:
            operations = params.get("operations", 1)
            base_cost += operations * 0.0001
            
            cache_size = params.get("cache_size_mb", 10)
            base_cost += cache_size * 0.00001
            
            persistent_storage = params.get("persistent_storage", False)
            if persistent_storage:
                base_cost += 0.0005
        
        return base_cost


# Demo the hybrid caching system
async def demo_hybrid_caching():
    """🎭 Demo the dual-layer caching system"""
    
    print("🔄 HYBRID CACHING SYSTEM DEMO")
    print("=" * 60)
    
    cache = CacheManager(verbose=True)  # Demo should show output
    
    # Simulate job description analysis
    job_description = """Senior Software Engineer
    Python, React, AWS
    5+ years experience required
    Competitive salary and benefits"""
    
    print(r"\n📄 TESTING CONTENT FINGERPRINTING:")
    
    # First analysis (expensive)
    analysis = "Job requires: Python expertise, React skills, AWS knowledge, senior-level experience"
    cache_hash = cache.cache_content_analysis(job_description, analysis, "job_analysis")
    
    # Second analysis (cached!)
    cached_analysis = cache.get_cached_analysis(job_description, "job_analysis")
    print(f"✅ Retrieved cached analysis: {cached_analysis[:50]}...")
    
    print(r"\n🔧 TESTING TOOL DEFINITION CACHING:")
    
    # Cache tool definition
    web_search_tool = {
        "name": "web_search",
        "description": "Search the web",
        "parameters": {"query": {"type": "string"}}
    }
    
    tool_hash = cache.cache_tool_definition("web_search", web_search_tool)
    cached_tool = cache.get_cached_tool("web_search", web_search_tool)
    print(f"✅ Retrieved cached tool: {cached_tool['name']}")
    
    print(r"\n📊 CACHE STATISTICS:")
    stats = cache.get_cache_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print(r"\n🎉 Hybrid caching system working perfectly!")
    print("💰 Next workflow run will be significantly cheaper!")


if __name__ == "__main__":
    asyncio.run(demo_hybrid_caching())
