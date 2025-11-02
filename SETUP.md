# Setup Instructions

## Prerequisites

1. **Python 3.9+** installed
2. **Node.js 18+** and npm installed
3. **Neo4j Database** - Download from https://neo4j.com/download/
4. **FFmpeg** - For audio processing

## Installation Steps

### 1. Clone and Navigate

```bash
cd D:\project_final_year
```

### 2. Set Up Python Environment

```bash
# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Neo4j

#### Option A: Neo4j Desktop (Recommended for Development)

1. Download and install Neo4j Desktop
2. Create a new database
3. Start the database
4. Note the connection URI (usually `bolt://localhost:7687`)
5. Set the password

#### Option B: Neo4j Aura (Cloud)

1. Create account at https://neo4j.com/cloud/aura/
2. Create free tier database
3. Copy connection URI and credentials

### 4. Configure Environment

```bash
# Create .env file
cp .env.example .env

# Edit .env with your Neo4j credentials
# NEO4J_URI=bolt://localhost:7687
# NEO4J_USER=neo4j
# NEO4J_PASSWORD=your_password
```

### 5. Install FFmpeg (for audio processing)

#### Windows:
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add to PATH: `C:\ffmpeg\bin`

#### Verify installation:
```bash
ffmpeg -version
```

### 6. Set Up Frontend

```bash
cd frontend
npm install
cd ..
```

### 7. Run the Application

#### Terminal 1 - Backend:
```bash
python main.py
```

The backend will run on `http://localhost:8000`

#### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

The frontend will run on `http://localhost:5173`

## Troubleshooting

### Neo4j Connection Issues

- Verify Neo4j is running
- Check firewall settings
- Verify credentials in `.env`

### Audio Processing Issues

- Ensure FFmpeg is installed and in PATH
- Check audio file formats (supports: mp3, wav, m4a, ogg)

### Module Import Errors

```bash
pip install --upgrade -r requirements.txt
```

### Frontend Build Errors

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## First Run

1. Open browser to `http://localhost:5173`
2. Click "New Entry"
3. Try:
   - Adding text entry
   - Uploading an image
   - Recording audio
   - Adding tags
4. Click "Search" and try queries like:
   - "Tell me about happy moments"
   - "What did I write about work?"

## Next Steps

- Explore the graph visualization in Neo4j Browser
- Add more diary entries to build your semantic graph
- Try different search queries to test semantic understanding

## Architecture

```
Frontend (React) → Backend (FastAPI) → Neo4j Database
                              ↓
                    Whisper (Audio)
                    Tesseract (Images)
                    Sentence Transformers (Embeddings)
```

Enjoy your Personal Semantic Diary! 🎉




