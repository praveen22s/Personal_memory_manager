"""
Neo4j database interface for diary entries
"""

from neo4j import AsyncGraphDatabase
import os
import json
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime
from diary.graph_processor import GraphProcessor


class DiaryDatabase:
    """Neo4j database manager for diary entries"""
    
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        self.database = os.getenv("NEO4J_DATABASE", "neo4j")
        self.driver = None
        self.graph_processor = GraphProcessor()
    
    async def connect(self):
        """Connect to Neo4j database"""
        self.driver = AsyncGraphDatabase.driver(
            self.uri,
            auth=(self.user, self.password)
        )
        
        # Verify connectivity
        try:
            await self.driver.verify_connectivity()
            print("[OK] Connected to Neo4j")
        except Exception as e:
            print(f"[ERROR] Failed to connect to Neo4j: {e}")
            raise
        
        # Create constraints and indexes
        await self._setup_schema()
    
    async def _setup_schema(self):
        """Set up database schema, constraints, and indexes"""
        async with self.driver.session(database=self.database) as session:
            # Create constraints
            await session.run(
                "CREATE CONSTRAINT entry_id IF NOT EXISTS "
                "FOR (e:Entry) REQUIRE e.id IS UNIQUE"
            )
            
            # Create constraints for new node types
            try:
                await session.run(
                    "CREATE CONSTRAINT concept_name IF NOT EXISTS "
                    "FOR (c:Concept) REQUIRE c.name IS UNIQUE"
                )
                await session.run(
                    "CREATE CONSTRAINT entity_name IF NOT EXISTS "
                    "FOR (ent:Entity) REQUIRE ent.name IS UNIQUE"
                )
                await session.run(
                    "CREATE CONSTRAINT topic_name IF NOT EXISTS "
                    "FOR (t:Topic) REQUIRE t.name IS UNIQUE"
                )
                await session.run(
                    "CREATE CONSTRAINT person_name IF NOT EXISTS "
                    "FOR (p:Person) REQUIRE p.name IS UNIQUE"
                )
                await session.run(
                    "CREATE CONSTRAINT place_name IF NOT EXISTS "
                    "FOR (pl:Place) REQUIRE pl.name IS UNIQUE"
                )
            except Exception as e:
                print(f"[INFO] Some constraints may already exist: {e}")
            
            # Create full-text indexes for better search
            await session.run(
                "CREATE INDEX entry_text IF NOT EXISTS "
                "FOR (e:Entry) ON (e.text)"
            )
            
            await session.run(
                "CREATE INDEX entry_timestamp IF NOT EXISTS "
                "FOR (e:Entry) ON (e.timestamp)"
            )
            
            # Create indexes for graph nodes
            await session.run(
                "CREATE INDEX concept_name IF NOT EXISTS "
                "FOR (c:Concept) ON (c.name)"
            )
            
            await session.run(
                "CREATE INDEX keyword_name IF NOT EXISTS "
                "FOR (k:Keyword) ON (k.name)"
            )
            
            await session.run(
                "CREATE INDEX entity_name IF NOT EXISTS "
                "FOR (e:Entity) ON (e.name)"
            )
            
            # Create vector index for embeddings (Neo4j 5.x+)
            try:
                await session.run(
                    "CREATE VECTOR INDEX entry_embedding IF NOT EXISTS "
                    "FOR (e:Entry) ON e.embedding "
                    "OPTIONS {indexConfig: {`vector.dimensions`: 384, `vector.similarity_function`: 'cosine'}}"
                )
            except Exception as e:
                print(f"Note: Vector index may not be available: {e}")
    
    async def close(self):
        """Close database connection"""
        if self.driver:
            await self.driver.close()
    
    async def create_entry(self, entry_data: Dict) -> Dict:
        """Create a new diary entry in Neo4j"""
        async with self.driver.session(database=self.database) as session:
            # Generate unique ID
            import uuid
            entry_id = str(uuid.uuid4())
            
            # Prepare embedding for storage
            embedding = entry_data.get("embedding")
            if embedding is not None:
                embedding = list(embedding)  # Convert numpy array to list
            
            # Create entry node
            query = """
            CREATE (e:Entry {
                id: $id,
                title: $title,
                text: $text,
                timestamp: $timestamp,
                audio_path: $audio_path,
                image_path: $image_path,
                embedding: $embedding
            })
            RETURN e.id as id, e.title as title, e.text as text,
                   e.timestamp as timestamp, e.audio_path as audio_path,
                   e.image_path as image_path
            """
            
            result = await session.run(
                query,
                id=entry_id,
                title=entry_data.get("title", "Untitled"),
                text=entry_data.get("text"),
                timestamp=entry_data.get("timestamp", datetime.utcnow().isoformat()),
                audio_path=entry_data.get("audio_path"),
                image_path=entry_data.get("image_path"),
                embedding=embedding
            )
            
            # Don't need to use the result - we'll return our own dict
            
            # Create tags and relationships
            tags = entry_data.get("tags", [])
            if tags:
                await session.run(
                    """
                    MATCH (e:Entry {id: $entry_id})
                    UNWIND $tags AS tag_name
                    MERGE (t:Tag {name: tag_name})
                    CREATE (e)-[:HAS_TAG]->(t)
                    """,
                    entry_id=entry_id,
                    tags=tags
                )
            
            # Extract graph components from text
            entry_text = entry_data.get("text", "") or entry_data.get("title", "")
            if entry_text:
                graph_data = self.graph_processor.process_entry(entry_text)
                
                # Create Concept nodes and link to entry
                concepts = graph_data.get('concepts', [])
                if concepts:
                    await session.run(
                        """
                        MATCH (e:Entry {id: $entry_id})
                        UNWIND $concepts AS concept_name
                        MERGE (c:Concept {name: concept_name})
                        CREATE (e)-[:MENTIONS_CONCEPT]->(c)
                        """,
                        entry_id=entry_id,
                        concepts=concepts[:20]  # Limit to prevent too many nodes
                    )
                
                # Create Entity nodes and link to entry
                entities = graph_data.get('entities', [])
                if entities:
                    await session.run(
                        """
                        MATCH (e:Entry {id: $entry_id})
                        UNWIND $entities AS entity_name
                        MERGE (ent:Entity {name: entity_name})
                        CREATE (e)-[:MENTIONS_ENTITY]->(ent)
                        """,
                        entry_id=entry_id,
                        entities=entities[:10]  # Limit entities
                    )
                
                # Create Keyword nodes and link to entry
                keywords = graph_data.get('keywords', [])
                if keywords:
                    await session.run(
                        """
                        MATCH (e:Entry {id: $entry_id})
                        UNWIND $keywords AS keyword_name
                        MERGE (k:Keyword {name: keyword_name})
                        CREATE (e)-[:HAS_KEYWORD]->(k)
                        """,
                        entry_id=entry_id,
                        keywords=keywords[:15]  # Limit keywords
                    )
                
                # Create relationships extracted from text
                relationships = graph_data.get('relationships', [])
                for rel in relationships[:10]:  # Limit relationships
                    if rel.get('object'):
                        await session.run(
                            """
                            MATCH (e:Entry {id: $entry_id})
                            MERGE (obj:Concept {name: $object})
                            CREATE (e)-[:RELATES_TO {type: $relation}]->(obj)
                            """,
                            entry_id=entry_id,
                            relation=rel.get('relation', 'relates'),
                            object=rel.get('object', '')[:50]
                        )
            
            # Link to entries with shared concepts/keywords
            await self._link_shared_concepts(entry_id)
            
            # Create similarity relationships with existing entries (if embeddings available)
            if embedding:
                await self._create_similarity_relationships(entry_id, embedding, 0.85)
            
            # Return created entry
            return {
                "id": entry_id,
                "title": entry_data.get("title", "Untitled"),
                "text": entry_data.get("text"),
                "timestamp": entry_data.get("timestamp"),
                "audio_path": entry_data.get("audio_path"),
                "image_path": entry_data.get("image_path"),
                "tags": tags
            }
    
    async def _link_shared_concepts(self, entry_id: str):
        """Link entry to other entries that share concepts, keywords, or entities"""
        async with self.driver.session(database=self.database) as session:
            # Link entries sharing concepts
            query = """
            MATCH (e1:Entry {id: $entry_id})-[:MENTIONS_CONCEPT]->(c:Concept)<-[:MENTIONS_CONCEPT]-(e2:Entry)
            WHERE e1 <> e2
            WITH e1, e2, count(c) as shared_concepts
            WHERE shared_concepts >= 1
            MERGE (e1)-[r:SHARES_CONCEPT {count: shared_concepts}]->(e2)
            RETURN count(*) as linked
            """
            await session.run(query, entry_id=entry_id)
            
            # Link entries sharing keywords
            query = """
            MATCH (e1:Entry {id: $entry_id})-[:HAS_KEYWORD]->(k:Keyword)<-[:HAS_KEYWORD]-(e2:Entry)
            WHERE e1 <> e2
            WITH e1, e2, count(k) as shared_keywords
            WHERE shared_keywords >= 2
            MERGE (e1)-[r:SHARES_KEYWORD {count: shared_keywords}]->(e2)
            RETURN count(*) as linked
            """
            await session.run(query, entry_id=entry_id)
            
            # Link entries sharing entities
            query = """
            MATCH (e1:Entry {id: $entry_id})-[:MENTIONS_ENTITY]->(ent:Entity)<-[:MENTIONS_ENTITY]-(e2:Entry)
            WHERE e1 <> e2
            WITH e1, e2, count(ent) as shared_entities
            WHERE shared_entities >= 1
            MERGE (e1)-[r:SHARES_ENTITY {count: shared_entities}]->(e2)
            RETURN count(*) as linked
            """
            await session.run(query, entry_id=entry_id)
    
    async def _create_similarity_relationships(self, entry_id: str, embedding: List[float], threshold: float):
        """Create SIMILAR_TO relationships with similar entries"""
        async with self.driver.session(database=self.database) as session:
            query = """
            MATCH (e1:Entry {id: $entry_id})
            MATCH (e2:Entry)
            WHERE e1 <> e2 AND e2.embedding IS NOT NULL
            WITH e1, e2, 
                cosineSimilarity(e1.embedding, e2.embedding) as similarity
            WHERE similarity > $threshold
            CREATE (e1)-[:SIMILAR_TO {score: similarity}]->(e2)
            RETURN COUNT(*) as count
            """
            
            await session.run(query, entry_id=entry_id, threshold=threshold)
    
    async def get_all_entries(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get all diary entries ordered by timestamp"""
        async with self.driver.session(database=self.database) as session:
            query = """
            MATCH (e:Entry)
            OPTIONAL MATCH (e)-[:HAS_TAG]->(t:Tag)
            WITH e, collect(t.name) as tags
            ORDER BY e.timestamp DESC
            SKIP $skip
            LIMIT $limit
            RETURN e.id as id, e.title as title, e.text as text, 
                   e.timestamp as timestamp, e.audio_path as audio_path,
                   e.image_path as image_path, tags
            """
            
            result = await session.run(query, skip=skip, limit=limit)
            
            entries = []
            async for record in result:
                entries.append(dict(record))
            
            return entries
    
    async def get_entry_by_id(self, entry_id: str) -> Optional[Dict]:
        """Get a specific entry by ID"""
        async with self.driver.session(database=self.database) as session:
            query = """
            MATCH (e:Entry {id: $id})
            OPTIONAL MATCH (e)-[:HAS_TAG]->(t:Tag)
            WITH e, collect(t.name) as tags
            RETURN e.id as id, e.title as title, e.text as text, 
                   e.timestamp as timestamp, e.audio_path as audio_path,
                   e.image_path as image_path, tags
            """
            
            result = await session.run(query, id=entry_id)
            record = await result.single()
            
            return dict(record) if record else None
    
    async def semantic_search(self, query_embedding: np.ndarray, limit: int = 10) -> List[Dict]:
        """Perform semantic search using vector similarity"""
        async with self.driver.session(database=self.database) as session:
            # Convert to list
            query_vec = list(query_embedding)
            
            # Use vector similarity search
            query = """
            MATCH (e:Entry)
            WHERE e.embedding IS NOT NULL
            WITH e, cosineSimilarity(e.embedding, $query_vector) as similarity
            WHERE similarity > 0.5
            OPTIONAL MATCH (e)-[:HAS_TAG]->(t:Tag)
            WITH e, similarity, collect(t.name) as tags
            ORDER BY similarity DESC
            LIMIT $limit
            RETURN e.id as id, e.title as title, e.text as text, 
                   e.timestamp as timestamp, e.audio_path as audio_path,
                   e.image_path as image_path, tags, similarity
            """
            
            result = await session.run(query, query_vector=query_vec, limit=limit)
            
            entries = []
            async for record in result:
                entries.append(dict(record))
            
            return entries
    
    async def text_search(self, query_text: str, limit: int = 10) -> List[Dict]:
        """Perform text-based search as fallback when embeddings unavailable"""
        async with self.driver.session(database=self.database) as session:
            # Simple text search using CONTAINS
            query = """
            MATCH (e:Entry)
            WHERE e.text IS NOT NULL 
            AND (toLower(e.text) CONTAINS toLower($query_text)
                 OR toLower(e.title) CONTAINS toLower($query_text))
            OPTIONAL MATCH (e)-[:HAS_TAG]->(t:Tag)
            WITH e, collect(t.name) as tags
            ORDER BY e.timestamp DESC
            LIMIT $limit
            RETURN e.id as id, e.title as title, e.text as text, 
                   e.timestamp as timestamp, e.audio_path as audio_path,
                   e.image_path as image_path, tags
            """
            
            result = await session.run(query, query_text=query_text, limit=limit)
            
            entries = []
            async for record in result:
                entries.append(dict(record))
            
            return entries
    
    async def delete_entry(self, entry_id: str) -> bool:
        """Delete an entry and its relationships"""
        async with self.driver.session(database=self.database) as session:
            query = """
            MATCH (e:Entry {id: $id})
            DETACH DELETE e
            RETURN COUNT(*) as deleted
            """
            
            result = await session.run(query, id=entry_id)
            record = await result.single()
            
            return record["deleted"] > 0



