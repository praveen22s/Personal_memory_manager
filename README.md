# 📔 Personal Semantic Diary

<div align="center">

**An intelligent personal diary application with semantic understanding and graph-based memory storage**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.x-orange.svg)](https://neo4j.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 🌟 Overview

Personal Semantic Diary is an AI-powered diary application that stores text, speech, and images with semantic understanding. It uses Neo4j graph database to create intelligent relationships between memories and enables natural language queries to retrieve contextual information.

### Key Features

- **📝 Multi-Modal Input**: Text, speech (audio), and images
- **🧠 Semantic Graph Storage**: Neo4j graph database with automatic relationship creation
- **🔍 Intelligent Search**: Natural language queries with semantic understanding
- **🎯 Auto-Linking**: Entries automatically connect based on shared concepts, keywords, and entities
- **📊 Graph Visualization**: Visualize relationships between your memories
- **🎨 Modern UI**: Beautiful, responsive React interface
- **🔐 Privacy-First**: All data stored locally

## 🎬 Demo

Create entries with text, images, or audio. The system automatically:
- Extracts concepts, keywords, and entities
- Creates graph relationships
- Links related entries
- Enables semantic search

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────┐         ┌──────────┐
│   React UI      │ ◄────► │   FastAPI    │ ◄────► │  Neo4j   │
│   (Frontend)    │         │   Backend    │         │  Graph   │
└─────────────────┘         └──────────────┘         └──────────┘
                                    │
                          ┌─────────┴─────────┐
                          │                   │
                    ┌─────▼─────┐      ┌─────▼─────┐
                    │  Whisper  │      │Embeddings │
                    │  (Audio)  │      │  (ML)     │
                    └───────────┘      └───────────┘
```

## 📋 Prerequisites

- **Python 3.9+**
- **Node.js 18+**
- **Neo4j Desktop** or **Neo4j Aura** (free tier available)
- **FFmpeg** (for audio processing)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/personal-semantic-diary.git
cd personal-semantic-diary
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note**: First installation may take a few minutes as it downloads ML models (~500MB).

### 3. Set Up Neo4j

1. Download and install [Neo4j Desktop](https://neo4j.com/download/)
2. Create a new database
3. Start the database and note your password

### 4. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Neo4j credentials
# NEO4J_URI=bolt://localhost:7687
# NEO4J_USER=neo4j
# NEO4J_PASSWORD=your_password
```

### 5. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 6. Run the Application

**Backend**:
```bash
python main.py
```

**Frontend** (in a new terminal):
```bash
cd frontend
npm run dev
```

**Or use the convenience scripts**:
- Windows: `run.bat`
- Mac/Linux: `./run.sh`

### 7. Open in Browser

Navigate to **http://localhost:5173**

## 📖 Usage

### Creating Entries

1. Click **"New Entry"**
2. Add text, upload images, or record audio
3. Add tags (optional)
4. Click **"Save Entry"**

The system automatically:
- Extracts keywords, concepts, and entities
- Creates graph nodes and relationships
- Links to related entries

### Searching Memories

Use natural language queries:
- "Tell me about happy moments"
- "What did I do last week?"
- "Show me memories about work"
- "Find entries about Paris"

### Viewing the Graph

Open Neo4j Browser (`http://localhost:7474`) to visualize your memory graph:

```cypher
// See all entries and connections
MATCH (e:Entry)-[r]->(n)
RETURN e, r, n
LIMIT 100
```

## 🧩 Graph Structure

The application creates a rich graph structure:

- **Entry** nodes - Your diary entries
- **Concept** nodes - Semantic concepts (emotions, activities, topics)
- **Entity** nodes - Named entities (people, places)
- **Keyword** nodes - Important keywords
- **Tag** nodes - User-defined tags

**Relationships**:
- `MENTIONS_CONCEPT` - Entry → Concept
- `MENTIONS_ENTITY` - Entry → Entity
- `HAS_KEYWORD` - Entry → Keyword
- `SHARES_CONCEPT` - Entry → Entry (when entries share concepts)
- `SHARES_KEYWORD` - Entry → Entry (when entries share keywords)
- `SIMILAR_TO` - Entry → Entry (semantic similarity)

## 📁 Project Structure

```
personal-semantic-diary/
├── diary/                  # Backend package
│   ├── database.py        # Neo4j integration
│   ├── embeddings.py      # AI embeddings
│   ├── graph_processor.py # Graph extraction
│   ├── speech.py          # Audio transcription
│   └── image.py           # Image OCR
├── frontend/              # React application
│   ├── src/
│   │   ├── components/    # UI components
│   │   └── App.jsx        # Main app
│   └── package.json
├── main.py               # Backend entry point
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Media Storage
UPLOAD_DIR=./uploads
MAX_FILE_SIZE_MB=50
```

## 🛠️ API Endpoints

- `POST /api/entries` - Create new entry (text, audio, image)
- `GET /api/entries` - List all entries
- `GET /api/entries/{id}` - Get specific entry
- `POST /api/query` - Semantic search with summarization
- `POST /api/search` - Basic semantic search
- `GET /api/media/{id}` - Retrieve media files
- `DELETE /api/entries/{id}` - Delete entry

## 📚 Documentation

- **[START_HERE.md](START_HERE.md)** - Getting started guide
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[GRAPH_STRUCTURE.md](GRAPH_STRUCTURE.md)** - Graph database structure
- **[FEATURES.md](FEATURES.md)** - Complete feature list

## 🐛 Troubleshooting

### Common Issues

**Neo4j Connection Failed**
- Ensure Neo4j Desktop is running
- Check credentials in `.env`
- Verify firewall settings

**Model Loading Issues**
- First run downloads models (~420MB)
- Check internet connection
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

**PowerShell Execution Policy**
- Use Command Prompt or run: `Set-ExecutionPolicy RemoteSigned`

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** - Modern Python web framework
- **Neo4j** - Graph database platform
- **React** - UI library
- **sentence-transformers** - Semantic embeddings
- **OpenAI Whisper** - Speech recognition

## 📞 Support

For issues and questions:
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for system details
- Open an issue on GitHub

## 🌟 Features in Detail

### Semantic Graph
- Automatic concept extraction
- Entity recognition
- Keyword identification
- Relationship inference

### Multi-Modal Support
- Text entries
- Audio transcription (Whisper)
- Image OCR (Tesseract)

### Intelligent Search
- Natural language queries
- Semantic similarity matching
- Context-aware results
- Summarization

---

<div align="center">

**Built with ❤️ using AI and Graph Technology**

⭐ Star this repo if you find it useful!

</div>#   P e r s o n a l _ m e m o r y _ m a n a g e r  
 