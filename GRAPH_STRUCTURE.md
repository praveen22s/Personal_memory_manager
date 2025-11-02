# Graph Structure Documentation

## Overview

The Personal Semantic Diary now creates a rich graph structure in Neo4j by parsing input sentences and extracting semantic components.

## Graph Components

### Node Types

1. **Entry** - Diary entries (main nodes)
2. **Concept** - Semantic concepts extracted from text
3. **Entity** - Named entities (people, places, etc.)
4. **Keyword** - Important keywords from text
5. **Tag** - User-defined tags

### Relationship Types

1. **MENTIONS_CONCEPT** - Entry → Concept
   - Created when entry mentions a concept
   
2. **MENTIONS_ENTITY** - Entry → Entity
   - Created when entry mentions a named entity
   
3. **HAS_KEYWORD** - Entry → Keyword
   - Created when entry contains important keywords
   
4. **RELATES_TO** - Entry → Concept (with type property)
   - Created from extracted relationships (e.g., "I went to Paris")
   
5. **SHARES_CONCEPT** - Entry → Entry (with count)
   - Links entries that share concepts
   
6. **SHARES_KEYWORD** - Entry → Entry (with count)
   - Links entries that share keywords (2+ shared)
   
7. **SHARES_ENTITY** - Entry → Entry (with count)
   - Links entries that share entities
   
8. **SIMILAR_TO** - Entry → Entry (with score)
   - Links semantically similar entries (via embeddings)
   
9. **HAS_TAG** - Entry → Tag
   - User-defined tags

## Example Graph Structure

```
Entry1 "I went to Paris and felt happy"
    ├─→ Concept: "paris"
    ├─→ Concept: "happy"
    ├─→ Keyword: "went"
    ├─→ Keyword: "felt"
    └─→ RELATES_TO {type: "went"} → Concept: "paris"

Entry2 "Paris was beautiful, I loved it"
    ├─→ Concept: "paris"
    ├─→ Concept: "beautiful"
    ├─→ Keyword: "loved"
    └─→ SHARES_CONCEPT {count: 1} → Entry1
```

## How It Works

### 1. Text Processing

When you create an entry, the text is processed by `GraphProcessor`:

- **Keywords**: Extracts important words (filtering stop words)
- **Concepts**: Combines keywords with emotional/activity concepts
- **Entities**: Extracts named entities (people, places)
- **Relationships**: Extracts subject-verb-object patterns

### 2. Graph Creation

The extracted components create nodes and relationships:

```python
Entry Text: "I went to Paris and felt happy"

Extracted:
- Keywords: ["went", "paris", "felt", "happy"]
- Concepts: ["paris", "happy", "travel", "emotion"]
- Entities: ["Paris"]
- Relationships: [{subject: "entry", relation: "went", object: "paris"}]

Creates:
- Entry node
- Concept nodes: paris, happy, travel, emotion
- Entity node: Paris
- Keyword nodes: went, felt
- Relationships: Entry-[:MENTIONS_CONCEPT]->Concept
                Entry-[:MENTIONS_ENTITY]->Entity
                Entry-[:HAS_KEYWORD]->Keyword
                Entry-[:RELATES_TO {type:"went"}]->Concept(paris)
```

### 3. Cross-Entry Linking

Entries are automatically linked when they share:
- **Concepts** (1+ shared)
- **Keywords** (2+ shared)
- **Entities** (1+ shared)

## Query Examples

### Find all entries about "Paris":
```cypher
MATCH (e:Entry)-[:MENTIONS_CONCEPT]->(c:Concept {name: "paris"})
RETURN e
```

### Find entries connected to a specific entry:
```cypher
MATCH (e1:Entry {id: "..."})-[r:SHARES_CONCEPT|SHARES_KEYWORD|SHARES_ENTITY]-(e2:Entry)
RETURN e2, type(r), r.count
```

### Find the concept graph:
```cypher
MATCH (c:Concept)<-[:MENTIONS_CONCEPT]-(e:Entry)
RETURN c, collect(e) as entries
```

### Find entry relationships:
```cypher
MATCH path = (e1:Entry)-[*1..2]-(e2:Entry)
WHERE e1 <> e2
RETURN path
LIMIT 50
```

## Visualization

You can visualize the graph in Neo4j Browser:

1. Open Neo4j Desktop
2. Click "Open" on your database
3. Run: `MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 100`

This shows the graph structure with all relationships!

## Benefits

✅ **Automatic Linking**: Entries are connected without manual tags
✅ **Semantic Understanding**: Concepts create meaning-based connections
✅ **Discover Relationships**: Find related memories automatically
✅ **Graph Traversal**: Navigate from one memory to related ones
✅ **Better Search**: Search by concepts, not just keywords

---

**Your diary entries now form a rich, interconnected graph!** 🕸️
