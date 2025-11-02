# Personal Semantic Diary - Project Overview

## 🎯 Project Description

A cutting-edge personal diary application that leverages **Artificial Intelligence** and **Semantic Graph Databases** to create an intelligent memory management system. Unlike traditional diaries, this application understands context and relationships between your memories, allowing you to query your past in natural language.

## 🌟 Key Features

### 1. **Multi-Modal Input**
- **Text**: Write your thoughts directly
- **Speech**: Record audio that's automatically transcribed using OpenAI Whisper
- **Images**: Upload photos with OCR text extraction

### 2. **Semantic Storage**
- **Neo4j Graph Database**: Stores memories as nodes with relationships
- **Vector Embeddings**: 384-dimensional embeddings using sentence-transformers
- **Similarity Relationships**: Automatically links similar memories
- **Tag-Based Organization**: Categorize and connect entries

### 3. **Intelligent Search**
- **Natural Language Queries**: Ask questions like "Tell me about the happiest moments"
- **Semantic Understanding**: Matches intent, not just keywords
- **Contextual Summarization**: Generates summaries from relevant memories
- **Similarity Scoring**: Shows relevance of each result

### 4. **Media Retrieval**
- **Image Display**: View original photos in search results
- **Audio Playback**: Listen to original recordings
- **Timestamped**: All entries include creation time
- **Chronological Timeline**: Browse entries in time order

## 🏗️ Architecture

### Backend (Python/FastAPI)
```
main.py                 # API endpoints and file handling
diary/
├── database.py         # Neo4j integration
├── embeddings.py       # Semantic embeddings & search
├── speech.py           # Whisper transcription
├── image.py            # Image OCR processing
└── models.py           # Pydantic data models
```

### Frontend (React/Vite)
```
src/
├── App.jsx             # Main application
├── components/
│   ├── EntryForm.jsx   # Create/edit entries
│   ├── EntryList.jsx   # Display all entries
│   ├── EntryCard.jsx   # Individual entry display
│   └── SearchPanel.jsx # Semantic search interface
├── App.css             # Application styles
└── index.css           # Global styles
```

### Database (Neo4j)
```
Entry Nodes:
- id: UUID
- title: String
- text: String
- timestamp: DateTime
- audio_path: String (optional)
- image_path: String (optional)
- embedding: Vector[384]

Relationships:
- Entry -[:HAS_TAG]-> Tag
- Entry -[:SIMILAR_TO]-> Entry (with similarity score)
```

## 🔧 Technology Stack

### Core Technologies
- **Backend**: FastAPI, Python 3.9+
- **Database**: Neo4j 5.x
- **Frontend**: React 18, Vite
- **ML**: sentence-transformers, OpenAI Whisper

### Key Libraries
- `neo4j`: Graph database driver
- `sentence-transformers`: Embedding generation
- `openai-whisper`: Speech-to-text
- `pytesseract`: OCR text extraction
- `numpy`: Vector operations
- `Pillow`: Image processing

## 📊 Data Flow

### Creating an Entry
```
User Input (text/audio/image)
    ↓
FastAPI Receives Request
    ↓
┌─────────────────────────────────────┐
│ Text → Direct                       │
│ Audio → Whisper → Transcription     │
│ Image → OCR → Text Extraction       │
└─────────────────────────────────────┘
    ↓
Generate Embedding (384-dim vector)
    ↓
Store in Neo4j:
  - Create Entry Node
  - Create Tag Nodes & Relationships
  - Create Similarity Relationships
    ↓
Return Stored Entry
```

### Semantic Search
```
User Query: "Tell me about happy moments"
    ↓
Generate Query Embedding
    ↓
Search Neo4j:
  - Cosine similarity with all entries
  - Filter by threshold (>0.5)
  - Rank by similarity
    ↓
Retrieve Top Results with Media
    ↓
Generate Summary from Results
    ↓
Return: Summary + Entries + Media
```

## 🎨 User Interface

### Design Philosophy
- **Dark Theme**: Modern, easy on the eyes
- **Responsive**: Works on desktop and mobile
- **Intuitive**: Minimal learning curve
- **Visual Feedback**: Loading states, animations
- **Accessible**: Semantic HTML, keyboard navigation

### Key Screens
1. **Entry List**: Chronological timeline with filters
2. **Entry Form**: Multi-modal input with preview
3. **Search Panel**: Natural language interface
4. **Results**: Summary + ranked entries with media

## 🔍 Semantic Graph Concepts

### Nodes
- **Entry**: Individual diary entry
- **Tag**: Category label (e.g., "happy", "work")

### Relationships
- **HAS_TAG**: Links entries to categories
- **SIMILAR_TO**: Connects related memories by content

### Vector Search
- Uses `cosineSimilarity()` function in Neo4j
- Compares 384-dimensional embeddings
- Threshold-based filtering for relevance
- Scoring and ranking by similarity

## 🚀 Performance Considerations

### Embeddings
- Model: `all-MiniLM-L6-v2` (384 dimensions)
- Fast inference with sentence-transformers
- Batched processing for multiple texts

### Database
- Vector indexes on embeddings
- Full-text indexes on text content
- Cypher query optimization

### Frontend
- React component optimization
- Lazy loading for media
- Debounced search queries

## 🔐 Security & Privacy

### Data Protection
- Local storage: Files stored on your machine
- Database: Neo4j runs locally or on your server
- No cloud dependencies: Everything stays private

### Input Validation
- File type checking
- Size limits (configurable)
- Sanitized text inputs

## 📈 Future Enhancements

### Potential Features
- [ ] Mood tracking and sentiment analysis
- [ ] Automatic timeline generation
- [ ] Location-based tagging
- [ ] People recognition from photos
- [ ] Weather/context integration
- [ ] Export to PDF/Word
- [ ] Mobile app (React Native)
- [ ] Voice commands
- [ ] Graph visualization
- [ ] Memory reminders
- [ ] Statistical insights
- [ ] Integration with calendar

### Technical Improvements
- [ ] Caching layer (Redis)
- [ ] Background job processing
- [ ] Batch operations
- [ ] Incremental embeddings
- [ ] Multi-language support
- [ ] Better OCR with ML models
- [ ] Video support
- [ ] Real-time collaboration

## 🧪 Testing

### Test Scenarios
1. Create entries with all input types
2. Semantic search with various queries
3. Media upload and retrieval
4. Tag filtering
5. Similarity relationships
6. Error handling

### Example Queries
- "Show me work-related entries"
- "What did I do last weekend?"
- "Tell me about traveling"
- "Memories with Sarah"
- "Happy moments in 2024"

## 📝 Use Cases

1. **Personal Journal**: Daily reflections and thoughts
2. **Project Log**: Track progress and decisions
3. **Learning Diary**: Record insights and discoveries
4. **Travel Journal**: Document trips with photos
5. **Mood Tracker**: Emotional wellbeing monitoring
6. **Idea Bank**: Store and link creative thoughts
7. **Research Log**: Academic or professional notes

## 🤝 Contributing

This is a final-year project demonstrating:
- Full-stack development
- AI/ML integration
- Graph database design
- Modern UI/UX
- Semantic search implementation

## 📄 License

Educational project for academic purposes.

---

**Built with ❤️ using AI and Graph Technology**




