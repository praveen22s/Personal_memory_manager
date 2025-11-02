# System Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                         │
│                      (React + Vite)                           │
│                                                               │
│  Components:                                                  │
│  ├── EntryForm: Multi-modal input                            │
│  ├── EntryList: Chronological display                        │
│  ├── EntryCard: Individual memory display                    │
│  └── SearchPanel: Natural language queries                   │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/REST API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       FastAPI Backend                         │
│                                                               │
│  Endpoints:                                                   │
│  ├── POST   /api/entries      - Create entry                 │
│  ├── GET    /api/entries      - List entries                 │
│  ├── GET    /api/entries/{id} - Get entry                    │
│  ├── POST   /api/query        - Semantic search              │
│  ├── POST   /api/search       - Basic search                 │
│  └── DELETE /api/entries/{id} - Delete entry                 │
└────────┬────────────────────────────────────────────────────┘
         │
         ├──────────────────────┬─────────────────────────┐
         │                      │                         │
         ▼                      ▼                         ▼
┌─────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│   Neo4j Graph   │   │ EmbeddingService │   │ SpeechProcessor  │
│     Database    │   │                  │   │                  │
│                 │   │ - Generate       │   │ - Whisper        │
│ Nodes:          │   │   embeddings    │   │ - Transcription  │
│  • Entry        │   │ - Cosine         │   │                  │
│  • Tag          │   │   similarity     │   │                  │
│                 │   │ - Summarization  │   │                  │
│ Relations:      │   │                  │   │                  │
│  • HAS_TAG      │   └──────────────────┘   └──────────────────┘
│  • SIMILAR_TO   │
│                 │   ┌──────────────────┐
│ Vectors:        │   │ ImageProcessor   │
│  • embedding    │   │                  │
│    [384-dim]    │   │ - OCR            │
└─────────────────┘   │ - Metadata       │
                      │ - Text extract   │
                      └──────────────────┘
```

## Component Details

### 1. Frontend (React)

**Technology**: React 18, Vite, Axios

**State Management**: React Hooks (useState, useEffect)

**Key Components**:

#### EntryForm.jsx
- **Purpose**: Multi-modal input interface
- **Features**:
  - Text input with rich textarea
  - File upload for images
  - WebRTC audio recording
  - Tag management
- **State**: Form fields, media files, recording state

#### EntryList.jsx
- **Purpose**: Display all diary entries
- **Features**:
  - Chronological ordering
  - Lazy loading support
  - Empty state handling
- **Props**: entries[], onDelete(), onRefresh()

#### EntryCard.jsx
- **Purpose**: Individual entry display
- **Features**:
  - Title and text rendering
  - Media preview (image/audio)
  - Tag display
  - Timestamp formatting
  - Delete button
- **Styling**: Card-based with hover effects

#### SearchPanel.jsx
- **Purpose**: Semantic search interface
- **Features**:
  - Natural language input
  - Results display
  - Summary generation
  - Media retrieval
- **State**: Query string, results object

### 2. Backend (FastAPI)

**Technology**: FastAPI, Uvicorn, Python 3.9+

**Architecture**: RESTful API with async/await

**Middleware**:
- CORS: Cross-origin resource sharing
- Static files: Media serving

**Key Modules**:

#### main.py
Main application entry point
- FastAPI app initialization
- Route definitions
- File upload handling
- Service integration

#### diary/models.py
Pydantic data models
- `EntryCreate`: Input validation
- `EntryResponse`: Output formatting
- `SearchQuery`: Query parameters

#### diary/database.py
Neo4j integration layer
- `DiaryDatabase` class
- Async connection management
- Cypher query execution
- Schema setup (constraints, indexes)
- Vector search operations

**Key Queries**:
```cypher
// Create entry with embedding
CREATE (e:Entry {
  id: $id, title: $title, text: $text,
  timestamp: $timestamp, embedding: $embedding
})
RETURN e

// Semantic search with vector similarity
MATCH (e:Entry)
WHERE e.embedding IS NOT NULL
WITH e, cosineSimilarity(e.embedding, $query_vector) as similarity
WHERE similarity > 0.5
RETURN e.id, e.title, e.text, similarity
ORDER BY similarity DESC
LIMIT $limit
```

#### diary/embeddings.py
Semantic understanding service
- `EmbeddingService` class
- Model: `all-MiniLM-L6-v2` (384 dimensions)
- Text embedding generation
- Cosine similarity calculation
- Summarization logic
- Batch processing

**Workflow**:
1. Load sentence-transformers model
2. Encode text to 384-dim vector
3. Store in Neo4j as vector property
4. Query with cosine similarity

#### diary/speech.py
Audio transcription service
- `SpeechProcessor` class
- Model: OpenAI Whisper (base)
- Async transcription
- Multiple audio formats
- Error handling

**Supported Formats**: mp3, wav, m4a, ogg

#### diary/image.py
Image processing service
- `ImageProcessor` class
- OCR with pytesseract
- Metadata extraction
- Fallback handling
- PIL integration

### 3. Database (Neo4j)

**Graph Structure**:

```
Node Labels:
┌──────────┐
│  Entry   │ Properties:
│          │ - id (UUID, unique)
│          │ - title
│          │ - text
│          │ - timestamp
│          │ - audio_path
│          │ - image_path
│          │ - embedding (Vector)
└────┬─────┘
     │
     ├─[:HAS_TAG]─►┌─────────┐
     │             │   Tag   │ Properties:
     └─[:SIMILAR_TO]         │ - name
      (similarity score)      │
                             └─────────┘
```

**Indexes**:
1. **Unique constraint**: Entry.id
2. **Full-text**: Entry.text
3. **Timestamp**: Entry.timestamp
4. **Vector**: Entry.embedding (384-dim, cosine)

**Relationships**:
1. **HAS_TAG**: Entry → Tag
   - Purpose: Categorization
   - Direction: Directed
2. **SIMILAR_TO**: Entry → Entry
   - Purpose: Content similarity
   - Properties: score (float)
   - Direction: Directed
   - Threshold: >0.85

**Query Patterns**:

```cypher
// Vector similarity search
MATCH (e:Entry)
WHERE e.embedding IS NOT NULL
WITH e, cosineSimilarity(e.embedding, $query_vec) as sim
WHERE sim > 0.5
RETURN e ORDER BY sim DESC

// Get related entries via SIMILAR_TO
MATCH (e1:Entry {id: $id})-[:SIMILAR_TO]->(e2:Entry)
RETURN e2 ORDER BY e1.similarity_score DESC

// Tag filtering
MATCH (e:Entry)-[:HAS_TAG]->(t:Tag {name: $tag})
RETURN e

// Timeline query
MATCH (e:Entry)
RETURN e ORDER BY e.timestamp DESC
SKIP $skip LIMIT $limit
```

## Data Flow

### Entry Creation Flow

```
User submits form (text/audio/image)
    │
    ▼
FastAPI receives multipart/form-data
    │
    ├─► If audio: SpeechProcessor.transcribe()
    │       └─► Whisper → text
    │
    ├─► If image: ImageProcessor.process_image()
    │       └─► OCR → text
    │
    ▼
Combine all text sources
    │
    ▼
EmbeddingService.embed_text()
    └─► sentence-transformers → 384-dim vector
    │
    ▼
DiaryDatabase.create_entry()
    ├─► Create Entry node in Neo4j
    ├─► Create/connect Tag nodes
    ├─► Store embedding vector
    │
    ▼
Find similar existing entries
    └─► CREATE SIMILAR_TO relationships
    │
    ▼
Return EntryResponse to frontend
    │
    ▼
Frontend displays new entry
```

### Search Flow

```
User enters query: "Tell me about happy moments"
    │
    ▼
SearchPanel sends POST /api/query
    │
    ▼
EmbeddingService.embed_text(query)
    └─► 384-dim query vector
    │
    ▼
DiaryDatabase.semantic_search()
    ├─► Neo4j cosine similarity
    ├─► Filter by threshold >0.5
    ├─► Rank by similarity DESC
    ├─► Retrieve top 20 entries
    │
    ▼
EmbeddingService.generate_summary()
    ├─► Process top 5 results
    ├─► Format context
    └─► Generate summary text
    │
    ▼
Return results to frontend:
    - summary (string)
    - relevant_entries (array)
    - media (images/audio)
    - count (number)
    │
    ▼
SearchPanel displays:
    ├─► Summary card
    ├─► List of entries with similarity scores
    └─► Media previews
```

## File Storage

```
uploads/
├── audio_20241215_143022.mp3
├── audio_20241215_144530.wav
├── image_20241215_150045.png
├── image_20241215_151230.jpg
└── ...
```

**Naming Convention**: `{type}_{YYYYMMDD}_{HHMMSS}{ext}`

## Configuration

### Environment Variables (.env)

```env
# Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
NEO4J_DATABASE=neo4j

# Server
HOST=0.0.0.0
PORT=8000

# Storage
UPLOAD_DIR=./uploads
MAX_FILE_SIZE_MB=50

# Optional
TESSERACT_CMD=C:\\Program Files\\Tesseract-OCR\\tesseract.exe
```

## Security Considerations

1. **File Uploads**: Type validation, size limits
2. **Database**: Credential management via .env
3. **CORS**: Configured for localhost development
4. **Input Sanitization**: Pydantic validation
5. **Error Handling**: Try-catch blocks with logging

## Performance Optimizations

1. **Async Operations**: Non-blocking I/O
2. **Vector Index**: Neo4j native indexing
3. **Lazy Loading**: Frontend pagination
4. **Batch Processing**: Multiple embeddings at once
5. **Caching**: Model loading (singleton)
6. **Database Indexes**: Full-text and vector

## Error Handling

```python
try:
    result = await db.semantic_search(query)
except ConnectionError:
    return {"error": "Database connection failed"}
except Exception as e:
    log.error(f"Search failed: {e}")
    return {"error": str(e)}
```

## Testing Strategy

### Unit Tests
- Embedding generation
- Text processing
- Query formatting

### Integration Tests
- API endpoints
- Database operations
- File upload/download

### E2E Tests
- User workflows
- Search functionality
- Media handling

## Deployment Considerations

### Development
- Local Neo4j Desktop
- File-based storage
- Single user

### Production
- Neo4j Aura or cluster
- S3/Object storage for media
- Load balancing
- CDN for static assets
- Redis caching
- Background jobs

---

**Architecture designed for scalability, maintainability, and performance.**




