# Native Python Memory System with Cloud Sync
*Complete Implementation Guide - From Local JSON to Global User Memory*

---

## High-Level Objective

Build a native Python memory system that replaces the Memory MCP dependency with a clean, integrated solution featuring local JSON storage, PostgreSQL cloud sync, user authentication, and team collaboration. Include complete cloud infrastructure setup and deployment guide.

## Mid-Level Objectives

- **Replace Memory MCP** with native Python classes integrated directly into Mao
- **Local JSON Storage** for offline functionality and fast reads
- **PostgreSQL Cloud Database** for sync, backup, and team features
- **Supabase Integration** for authentication and real-time features
- **Analytics Foundation** with proper database schema for user behavior tracking
- **Team Workspaces** with role-based permissions and sharing
- **Complete Deployment Guide** for cloud infrastructure setup

## Implementation Notes

### Technology Stack Decisions

**Database:** PostgreSQL with JSON columns (via Supabase)
- Native JSON support for flexible entity/observation storage
- ACID transactions for data consistency
- Built-in full-text search capabilities
- Excellent Python integration with `asyncpg`
- Analytics-friendly with time-series capabilities

**Cloud Platform:** Supabase (Free tier → $25/month Pro)
- PostgreSQL database included
- Built-in authentication and user management
- Real-time subscriptions for live sync
- Auto-generated REST API
- Python client library
- Row Level Security (RLS) for data privacy

**Web Hosting:** Railway ($5/month)
- Easy Python deployment
- Automatic HTTPS
- Environment variable management
- Git-based deployments
- Database connectivity included

**Alternative Stack (Budget Option):**
- **PlanetScale** - MySQL with free tier
- **Render** - Free web service hosting
- **Total Cost:** $0/month for development, ~$10/month production

## Context

### Beginning Context
- **Current:** Mao depends on external Memory MCP (TypeScript)
- **Storage:** Local `memory.json` file only
- **Sync:** None - memories trapped on single device
- **Analytics:** No data collection infrastructure
- **Teams:** No collaboration features

### Ending Context
- **Native:** Pure Python memory system integrated into Mao
- **Hybrid Storage:** Local JSON + PostgreSQL cloud sync
- **Multi-Device:** Seamless memory access across devices
- **Analytics:** Comprehensive usage tracking and insights
- **Teams:** Full workspace collaboration with permissions
- **Deployment:** Production-ready cloud infrastructure

## Low-Level Tasks

### Task 1: Native Python Memory Manager
```
Replace Memory MCP with pure Python implementation
File: CREATE orchestrator/memory_manager.py
Class: NativeMemoryManager
Function: create_entities(), add_observations(), search_nodes()
Details: Exact API compatibility with current Memory MCP calls
```

**Complete Code Implementation:**

```python
#!/usr/bin/env python3
\"\"\"
Native Memory Manager - Pure Python replacement for Memory MCP
Provides local JSON storage with cloud sync capabilities
\"\"\"

import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import uuid
import os

@dataclass
class Entity:
    \"\"\"Memory entity with observations\"\"\"
    name: str
    entity_type: str
    observations: List[str]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

@dataclass  
class Relation:
    \"\"\"Relationship between entities\"\"\"
    from_entity: str
    to_entity: str
    relation_type: str
    created_at: Optional[str] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

@dataclass
class KnowledgeGraph:
    \"\"\"Complete knowledge graph structure\"\"\"
    entities: List[Entity]
    relations: List[Relation]
    metadata: Dict[str, Any]

class NativeMemoryManager:
    \"\"\"
    Native Python memory manager with local JSON and cloud sync
    Drop-in replacement for Memory MCP with enhanced capabilities
    \"\"\"
    
    def __init__(self, user_id: str, memory_file: Optional[str] = None):
        self.user_id = user_id
        self.memory_file = Path(memory_file or f\"./configs/user/{user_id}/memory.json\")
        self.cloud_sync_enabled = os.getenv('CLOUD_SYNC_ENABLED', 'true').lower() == 'true'
        
        # Ensure directory exists
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize cloud sync if enabled
        if self.cloud_sync_enabled:
            from .cloud_sync import CloudSyncManager
            self.cloud_sync = CloudSyncManager(user_id)
        
        # Initialize analytics
        from .analytics_tracker import AnalyticsTracker
        self.analytics = AnalyticsTracker(user_id)
    
    def create_entities(self, entities_data: List[Dict[str, Any]]) -> List[Entity]:
        \"\"\"Create multiple new entities in the knowledge graph\"\"\"
        graph = self._load_local_graph()
        new_entities = []
        
        for entity_data in entities_data:
            # Check if entity already exists
            existing = next((e for e in graph.entities if e.name == entity_data['name']), None)
            if existing:
                continue
                
            entity = Entity(
                name=entity_data['name'],
                entity_type=entity_data.get('entityType', entity_data.get('entity_type', 'general')),
                observations=entity_data.get('observations', [])
            )
            
            graph.entities.append(entity)
            new_entities.append(entity)
        
        # Save locally
        self._save_local_graph(graph)
        
        # Track analytics
        asyncio.create_task(self.analytics.track_memory_event(\"entities_created\", {
            \"count\": len(new_entities),
            \"entity_types\": [e.entity_type for e in new_entities]
        }))
        
        # Sync to cloud asynchronously
        if self.cloud_sync_enabled:
            asyncio.create_task(self.cloud_sync.sync_entities(new_entities))
        
        return new_entities
    
    def create_relations(self, relations_data: List[Dict[str, Any]]) -> List[Relation]:
        \"\"\"Create multiple new relations between entities\"\"\"
        graph = self._load_local_graph()
        new_relations = []
        
        for relation_data in relations_data:
            # Check if relation already exists
            existing = next((r for r in graph.relations 
                           if r.from_entity == relation_data['from'] 
                           and r.to_entity == relation_data['to']
                           and r.relation_type == relation_data['relationType']), None)
            if existing:
                continue
                
            relation = Relation(
                from_entity=relation_data['from'],
                to_entity=relation_data['to'],
                relation_type=relation_data.get('relationType', relation_data.get('relation_type'))
            )
            
            graph.relations.append(relation)
            new_relations.append(relation)
        
        self._save_local_graph(graph)
        
        # Track analytics
        asyncio.create_task(self.analytics.track_memory_event(\"relations_created\", {
            \"count\": len(new_relations),
            \"relation_types\": [r.relation_type for r in new_relations]
        }))
        
        if self.cloud_sync_enabled:
            asyncio.create_task(self.cloud_sync.sync_relations(new_relations))
        
        return new_relations
    
    def add_observations(self, observations_data: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        \"\"\"Add new observations to existing entities\"\"\"
        graph = self._load_local_graph()
        results = {}
        
        for obs_data in observations_data:
            entity_name = obs_data['entityName']
            new_contents = obs_data.get('contents', [])
            
            entity = next((e for e in graph.entities if e.name == entity_name), None)
            if not entity:
                raise ValueError(f\"Entity '{entity_name}' not found\")
            
            # Add only new observations
            added_observations = []
            for content in new_contents:
                if content not in entity.observations:
                    entity.observations.append(content)
                    added_observations.append(content)
            
            entity.updated_at = datetime.now().isoformat()
            results[entity_name] = added_observations
        
        self._save_local_graph(graph)
        
        # Track analytics
        total_added = sum(len(obs_list) for obs_list in results.values())
        asyncio.create_task(self.analytics.track_memory_event(\"observations_added\", {
            \"entities_updated\": len(results),
            \"observations_added\": total_added
        }))
        
        if self.cloud_sync_enabled:
            asyncio.create_task(self.cloud_sync.sync_observations(observations_data))
        
        return results
    
    def search_nodes(self, query: str) -> KnowledgeGraph:
        \"\"\"Search for entities matching query\"\"\"
        graph = self._load_local_graph()
        query_lower = query.lower()
        
        # Track search analytics
        asyncio.create_task(self.analytics.track_memory_event(\"memory_search\", {
            \"query_length\": len(query),
            \"has_special_chars\": any(c in query for c in ['@', '#', '$'])
        }))
        
        # Find matching entities
        matching_entities = []
        for entity in graph.entities:
            if (query_lower in entity.name.lower() or 
                query_lower in entity.entity_type.lower() or
                any(query_lower in obs.lower() for obs in entity.observations)):
                matching_entities.append(entity)
        
        # Find relations between matching entities
        entity_names = {e.name for e in matching_entities}
        matching_relations = [r for r in graph.relations 
                            if r.from_entity in entity_names and r.to_entity in entity_names]
        
        return KnowledgeGraph(
            entities=matching_entities,
            relations=matching_relations,
            metadata={\"query\": query, \"total_matches\": len(matching_entities)}
        )
    
    def read_graph(self) -> KnowledgeGraph:
        \"\"\"Read the complete knowledge graph\"\"\"
        return self._load_local_graph()
    
    def _load_local_graph(self) -> KnowledgeGraph:
        \"\"\"Load knowledge graph from local JSON file\"\"\"
        if not self.memory_file.exists():
            return KnowledgeGraph(entities=[], relations=[], metadata={})
        
        try:
            with open(self.memory_file, 'r') as f:
                data = json.load(f)
            
            entities = [Entity(**e) for e in data.get('entities', [])]
            relations = [Relation(**r) for r in data.get('relations', [])]
            metadata = data.get('metadata', {})
            
            return KnowledgeGraph(entities=entities, relations=relations, metadata=metadata)
        
        except (json.JSONDecodeError, KeyError) as e:
            # Backup corrupted file and start fresh
            backup_file = self.memory_file.with_suffix('.backup.json')
            self.memory_file.rename(backup_file)
            return KnowledgeGraph(entities=[], relations=[], metadata={})
    
    def _save_local_graph(self, graph: KnowledgeGraph):
        \"\"\"Save knowledge graph to local JSON file\"\"\"
        graph.metadata['last_updated'] = datetime.now().isoformat()
        graph.metadata['user_id'] = self.user_id
        
        data = {
            'entities': [asdict(e) for e in graph.entities],
            'relations': [asdict(r) for r in graph.relations],
            'metadata': graph.metadata
        }
        
        # Atomic write to prevent corruption
        temp_file = self.memory_file.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        temp_file.rename(self.memory_file)
```

### Task 2: Cloud Sync Manager
```
PostgreSQL synchronization with conflict resolution
File: CREATE orchestrator/cloud_sync.py
Class: CloudSyncManager  
Function: sync_entities(), resolve_conflicts(), push_to_cloud()
Details: Bidirectional sync with intelligent conflict resolution
```

**Complete Code Implementation:**

```python
#!/usr/bin/env python3
\"\"\"
Cloud Sync Manager - PostgreSQL synchronization for memory data
Handles bidirectional sync, conflict resolution, and team workspaces
\"\"\"

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import asyncpg
from dataclasses import asdict
import logging

logger = logging.getLogger(__name__)

class CloudSyncManager:
    \"\"\"
    Manages synchronization between local memory and PostgreSQL cloud database
    \"\"\"
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.db_pool = None
        self._connection_lock = asyncio.Lock()
        
    async def initialize(self):
        \"\"\"Initialize database connection pool\"\"\"
        if self.db_pool:
            return
            
        async with self._connection_lock:
            if self.db_pool:  # Double-check after acquiring lock
                return
                
            database_url = os.getenv('DATABASE_URL')
            if not database_url:
                raise ValueError(\"DATABASE_URL environment variable not set\")
                
            self.db_pool = await asyncpg.create_pool(database_url, min_size=2, max_size=10)
            
            # Ensure user record exists
            await self._ensure_user_exists()
    
    async def sync_entities(self, entities: List['Entity']):
        \"\"\"Upload entity changes to cloud\"\"\"
        if not self.db_pool:
            await self.initialize()
        
        try:
            async with self.db_pool.acquire() as conn:
                for entity in entities:
                    await conn.execute(\"\"\"
                        INSERT INTO user_entities (user_id, entity_name, entity_type, observations, created_at, updated_at)
                        VALUES ($1, $2, $3, $4, $5, $6)
                        ON CONFLICT (user_id, entity_name) 
                        DO UPDATE SET 
                            observations = $4,
                            updated_at = $6
                    \"\"\", self.user_id, entity.name, entity.entity_type, 
                        json.dumps(entity.observations), entity.created_at, entity.updated_at)
                        
            logger.info(f\"Synced {len(entities)} entities to cloud for user {self.user_id}\")
            
        except Exception as e:
            logger.error(f\"Failed to sync entities: {e}\")
            # Don't raise - sync failures shouldn't break user experience
    
    async def sync_relations(self, relations: List['Relation']):
        \"\"\"Upload relation changes to cloud\"\"\"
        if not self.db_pool:
            await self.initialize()
            
        try:
            async with self.db_pool.acquire() as conn:
                for relation in relations:
                    await conn.execute(\"\"\"
                        INSERT INTO user_relations (user_id, from_entity, to_entity, relation_type, created_at)
                        VALUES ($1, $2, $3, $4, $5)
                        ON CONFLICT (user_id, from_entity, to_entity, relation_type) DO NOTHING
                    \"\"\", self.user_id, relation.from_entity, relation.to_entity, 
                        relation.relation_type, relation.created_at)
                        
            logger.info(f\"Synced {len(relations)} relations to cloud for user {self.user_id}\")
            
        except Exception as e:
            logger.error(f\"Failed to sync relations: {e}\")
    
    async def sync_observations(self, observations_data: List[Dict[str, Any]]):
        \"\"\"Upload observation changes to cloud\"\"\"
        if not self.db_pool:
            await self.initialize()
            
        try:
            async with self.db_pool.acquire() as conn:
                for obs_data in observations_data:
                    entity_name = obs_data['entityName']
                    new_contents = obs_data.get('contents', [])
                    
                    # Get current observations from cloud
                    row = await conn.fetchrow(\"\"\"
                        SELECT observations FROM user_entities 
                        WHERE user_id = $1 AND entity_name = $2
                    \"\"\", self.user_id, entity_name)
                    
                    if row:
                        current_obs = json.loads(row['observations'])
                        # Merge observations
                        merged_obs = list(set(current_obs + new_contents))
                        
                        await conn.execute(\"\"\"
                            UPDATE user_entities 
                            SET observations = $1, updated_at = $2
                            WHERE user_id = $3 AND entity_name = $4
                        \"\"\", json.dumps(merged_obs), datetime.now().isoformat(),
                            self.user_id, entity_name)
                        
        except Exception as e:
            logger.error(f\"Failed to sync observations: {e}\")
    
    async def pull_from_cloud(self) -> 'KnowledgeGraph':
        \"\"\"Download latest memory data from cloud\"\"\"
        if not self.db_pool:
            await self.initialize()
        
        from .memory_manager import Entity, Relation, KnowledgeGraph
        
        async with self.db_pool.acquire() as conn:
            # Get entities
            entity_rows = await conn.fetch(\"\"\"
                SELECT entity_name, entity_type, observations, created_at, updated_at
                FROM user_entities 
                WHERE user_id = $1
            \"\"\", self.user_id)
            
            entities = []
            for row in entity_rows:
                entities.append(Entity(
                    name=row['entity_name'],
                    entity_type=row['entity_type'],
                    observations=json.loads(row['observations']),
                    created_at=row['created_at'].isoformat() if row['created_at'] else None,
                    updated_at=row['updated_at'].isoformat() if row['updated_at'] else None
                ))
            
            # Get relations  
            relation_rows = await conn.fetch(\"\"\"
                SELECT from_entity, to_entity, relation_type, created_at
                FROM user_relations
                WHERE user_id = $1  
            \"\"\", self.user_id)
            
            relations = []
            for row in relation_rows:
                relations.append(Relation(
                    from_entity=row['from_entity'],
                    to_entity=row['to_entity'],
                    relation_type=row['relation_type'],
                    created_at=row['created_at'].isoformat() if row['created_at'] else None
                ))
            
            return KnowledgeGraph(
                entities=entities,
                relations=relations,
                metadata={\"sync_time\": datetime.now().isoformat()}
            )
    
    async def intelligent_merge(self, local_graph: 'KnowledgeGraph', cloud_graph: 'KnowledgeGraph') -> 'KnowledgeGraph':
        \"\"\"Merge local and cloud changes with conflict resolution\"\"\"
        merged_entities = {}
        merged_relations = set()
        
        # Merge entities - last write wins for observations
        for entity in local_graph.entities + cloud_graph.entities:
            if entity.name not in merged_entities:
                merged_entities[entity.name] = entity
            else:
                existing = merged_entities[entity.name]
                if entity.updated_at and existing.updated_at and entity.updated_at > existing.updated_at:
                    # Merge observations from both versions
                    combined_observations = list(set(existing.observations + entity.observations))
                    entity.observations = combined_observations
                    merged_entities[entity.name] = entity
        
        # Merge relations - combine all unique relations
        for relation in local_graph.relations + cloud_graph.relations:
            relation_key = (relation.from_entity, relation.to_entity, relation.relation_type)
            merged_relations.add(relation_key)
        
        from .memory_manager import KnowledgeGraph
        final_relations = []
        for from_e, to_e, rel_type in merged_relations:
            # Find the relation with the earliest created_at
            candidates = [r for r in local_graph.relations + cloud_graph.relations
                         if r.from_entity == from_e and r.to_entity == to_e and r.relation_type == rel_type]
            if candidates:
                final_relations.append(min(candidates, key=lambda x: x.created_at or ''))
        
        return KnowledgeGraph(
            entities=list(merged_entities.values()),
            relations=final_relations,
            metadata={\"merged_at\": datetime.now().isoformat()}
        )
    
    async def _ensure_user_exists(self):
        \"\"\"Ensure user record exists in cloud database\"\"\"
        async with self.db_pool.acquire() as conn:
            await conn.execute(\"\"\"
                INSERT INTO users (user_id, created_at, last_sync)
                VALUES ($1, $2, $3)
                ON CONFLICT (user_id) DO UPDATE SET last_sync = $3
            \"\"\", self.user_id, datetime.now(), datetime.now())
```

### Task 3: Complete Database Schema
```
PostgreSQL schema for memory, users, teams, and analytics
File: CREATE database/schema.sql
Tables: users, user_entities, user_relations, teams, team_memberships, analytics_events
Details: Complete database design with indexes and constraints
```

**Complete Database Schema:**

```sql
-- Complete PostgreSQL schema for Mao memory system
-- Deploy to Supabase or any PostgreSQL database

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";
CREATE EXTENSION IF NOT EXISTS \"pg_trgm\";

-- Users table
CREATE TABLE users (
    user_id VARCHAR(20) PRIMARY KEY,  -- meid generated user-#### format
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_sync TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    subscription_type VARCHAR(50) DEFAULT 'free',  -- free, pro, team
    settings JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT true
);

-- User entities (personal memory)
CREATE TABLE user_entities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(20) REFERENCES users(user_id) ON DELETE CASCADE,
    entity_name VARCHAR(255) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    observations JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, entity_name)
);

-- User relations (personal memory relationships)
CREATE TABLE user_relations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(20) REFERENCES users(user_id) ON DELETE CASCADE,
    from_entity VARCHAR(255) NOT NULL,
    to_entity VARCHAR(255) NOT NULL,
    relation_type VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, from_entity, to_entity, relation_type)
);

-- Teams/workspaces for shared memory
CREATE TABLE teams (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner_user_id VARCHAR(20) REFERENCES users(user_id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    settings JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT true
);

-- Team memberships and permissions
CREATE TABLE team_memberships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    team_id UUID REFERENCES teams(id) ON DELETE CASCADE,
    user_id VARCHAR(20) REFERENCES users(user_id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'member',  -- owner, admin, member, readonly
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true,
    
    UNIQUE(team_id, user_id)
);

-- Team shared entities
CREATE TABLE team_entities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    team_id UUID REFERENCES teams(id) ON DELETE CASCADE,
    entity_name VARCHAR(255) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    observations JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_by VARCHAR(20) REFERENCES users(user_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(team_id, entity_name)
);

-- Team shared relations
CREATE TABLE team_relations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    team_id UUID REFERENCES teams(id) ON DELETE CASCADE,
    from_entity VARCHAR(255) NOT NULL,
    to_entity VARCHAR(255) NOT NULL,
    relation_type VARCHAR(100) NOT NULL,
    created_by VARCHAR(20) REFERENCES users(user_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(team_id, from_entity, to_entity, relation_type)
);

-- Analytics events for usage tracking
CREATE TABLE analytics_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(20) REFERENCES users(user_id) ON DELETE SET NULL,
    event_type VARCHAR(100) NOT NULL,  -- memory_create, memory_search, workflow_start, etc.
    event_data JSONB DEFAULT '{}'::jsonb,
    session_id UUID,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Workflow analytics (from main Mao system)
CREATE TABLE workflow_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(20) REFERENCES users(user_id) ON DELETE SET NULL,
    workflow_id VARCHAR(50),
    workflow_name VARCHAR(255),
    tools_used JSONB DEFAULT '[]'::jsonb,
    total_cost DECIMAL(10,4),
    duration_seconds INTEGER,
    success BOOLEAN,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User sessions for tracking active usage
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(20) REFERENCES users(user_id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    ip_address INET,
    user_agent TEXT
);

-- Create indexes for performance
CREATE INDEX idx_user_entities_user_id ON user_entities(user_id);
CREATE INDEX idx_user_entities_type ON user_entities(entity_type);
CREATE INDEX idx_user_entities_updated ON user_entities(updated_at DESC);
CREATE INDEX idx_user_entities_search ON user_entities USING gin(to_tsvector('english', entity_name || ' ' || observations::text));

CREATE INDEX idx_user_relations_user_id ON user_relations(user_id);
CREATE INDEX idx_user_relations_from ON user_relations(from_entity);
CREATE INDEX idx_user_relations_to ON user_relations(to_entity);

CREATE INDEX idx_team_entities_team_id ON team_entities(team_id);
CREATE INDEX idx_team_entities_updated ON team_entities(updated_at DESC);
CREATE INDEX idx_team_relations_team_id ON team_relations(team_id);

CREATE INDEX idx_analytics_events_user_id ON analytics_events(user_id);
CREATE INDEX idx_analytics_events_type ON analytics_events(event_type);
CREATE INDEX idx_analytics_events_created ON analytics_events(created_at DESC);
CREATE INDEX idx_analytics_events_session ON analytics_events(session_id);

CREATE INDEX idx_workflow_analytics_user_id ON workflow_analytics(user_id);
CREATE INDEX idx_workflow_analytics_created ON workflow_analytics(created_at DESC);
CREATE INDEX idx_workflow_analytics_success ON workflow_analytics(success);

CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_user_sessions_activity ON user_sessions(last_activity DESC);

-- Create GIN index for JSONB columns for faster queries
CREATE INDEX idx_user_entities_observations ON user_entities USING gin(observations);
CREATE INDEX idx_team_entities_observations ON team_entities USING gin(observations);
CREATE INDEX idx_analytics_events_data ON analytics_events USING gin(event_data);
CREATE INDEX idx_workflow_analytics_tools ON workflow_analytics USING gin(tools_used);

-- Row Level Security (RLS) policies for data privacy
ALTER TABLE user_entities ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_relations ENABLE ROW LEVEL SECURITY;
ALTER TABLE team_entities ENABLE ROW LEVEL SECURITY;
ALTER TABLE team_relations ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE workflow_analytics ENABLE ROW LEVEL SECURITY;

-- Users can only access their own data
CREATE POLICY user_entities_policy ON user_entities FOR ALL 
USING (user_id = current_setting('app.current_user_id'));

CREATE POLICY user_relations_policy ON user_relations FOR ALL 
USING (user_id = current_setting('app.current_user_id'));

-- Team members can access team data
CREATE POLICY team_entities_policy ON team_entities FOR`
}