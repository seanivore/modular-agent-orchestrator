# Memvid - Video-Based AI Memory

## Quick Summary
Python library that compresses text into QR codes → MP4 videos for AI memory storage. Achieves 10x compression vs vector databases with semantic search capabilities.

**Core Concept:** Text → QR Codes → Video Compression → Searchable Knowledge Base

## Key URLs
- **GitHub:** https://github.com/Olow304/memvid.git
- **PyPI:** https://pypi.org/project/memvid/
- **Twitter Thread:** https://x.com/illyism/status/1930888284877521249
- **Creator:** @illyism (Ilias)

## Installation
```bash
pip install memvid
# For PDF support:
pip install memvid PyPDF2
```

## Basic Usage
```python
from memvid import MemvidEncoder, MemvidRetriever

# Create memory video
encoder = MemvidEncoder()
encoder.add_chunks(["text chunk 1", "text chunk 2"])
encoder.build_video("memory.mp4", "memory_index.json")

# Search memory
retriever = MemvidRetriever("memory.mp4", "memory_index.json")
results = retriever.search("query", top_k=5)
```

## MAO Integration Concept

### As Direct Module
```python
# mao/modules/memory/memvid_memory.py
class MemvidMemory:
    def __init__(self, config):
        self.video_path = config['video_path']
        self.index_path = config['index_path']
        self.retriever = MemvidRetriever(self.video_path, self.index_path)
    
    def search(self, query, top_k=5):
        return self.retriever.search(query, top_k)
```

### Config Schema
```json
{
  "memory": {
    "type": "memvid",
    "video_path": "agent_knowledge.mp4",
    "index_path": "agent_knowledge_index.json",
    "chunk_size": 512,
    "search_params": {
      "top_k": 5,
      "score_threshold": 0.7
    }
  }
}
```

### As MCP Tool (Future)
```python
# tools/memvid_tool.py
@tool
def create_memory_video(texts: List[str], output_name: str):
    """Convert text chunks to compressed video memory"""
    encoder = MemvidEncoder()
    encoder.add_chunks(texts)
    return encoder.build_video(f"{output_name}.mp4", f"{output_name}_index.json")

@tool  
def search_memory_video(video_path: str, index_path: str, query: str):
    """Search compressed video memory"""
    retriever = MemvidRetriever(video_path, index_path)
    return retriever.search(query, top_k=5)
```

## When to Consider

### Good For:
- Agent knowledge transfer between deployments
- Offline/edge agent operation
- Massive knowledge bases (>1M tokens)
- Agent knowledge marketplace
- Resource-constrained environments

### Not Needed For:
- Knowledge that fits in Claude context
- Frequently updated content
- Real-time collaborative knowledge
- Standard MAO operations

## Dependencies
```
qrcode[pil]==8.2
opencv-python==4.11.0.86
sentence-transformers==4.1.0
faiss-cpu==1.7.4
tqdm==4.67.1
```

## Status
**Backlog Item** - Interesting tech, not immediate MAO priority. Revisit if:
- Agent deployment scenarios require offline operation
- Knowledge bases exceed context limits
- Agent knowledge sharing becomes important

---
*Evaluated June 2025 - Cool compression innovation, file for later*