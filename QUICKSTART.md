# Quick Start Guide

Get your Personal Semantic Diary running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed  
- [ ] Neo4j running (Desktop or Aura)
- [ ] FFmpeg installed (for audio processing)

## Installation Steps

### 1. Install Python Dependencies

```bash
# Windows
python -m pip install -r requirements.txt

# Mac/Linux
pip3 install -r requirements.txt
```

**Note:** This will download ML models (~500MB), be patient!

### 2. Configure Neo4j

Create `.env` file in the project root:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here
NEO4J_DATABASE=neo4j
```

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 4. Run the Application

**Option A: Use the run script**

Windows:
```bash
run.bat
```

Mac/Linux:
```bash
chmod +x run.sh
./run.sh
```

**Option B: Manual start**

Terminal 1 (Backend):
```bash
python main.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

### 5. Open Your Browser

Navigate to: **http://localhost:5173**

## First Steps

### Create Your First Entry

1. Click **"New Entry"** button
2. Add a title: "My First Memory"
3. Write some text: "Today I learned how to build an AI diary!"
4. Add tags: "happy, learning, project"
5. Click **"Save Entry"**

### Search Your Memories

1. Click **"Search"** button
2. Try queries like:
   - "Tell me about happy moments"
   - "What did I learn today?"
   - "Show me memories about project"

### Try Multi-Modal Input

**Text:**
- Just type your thoughts

**Audio:**
- Click "Record Audio"
- Allow microphone access
- Speak your entry
- Stop recording
- Audio is automatically transcribed!

**Images:**
- Click "Upload Image"
- Select a photo
- Text in the image will be extracted (with OCR)

## Common Issues

### Neo4j Connection Failed

```bash
# Check if Neo4j is running
# Verify credentials in .env
# Check firewall settings
```

### Audio Not Transcribing

```bash
# Ensure FFmpeg is installed
ffmpeg -version

# Check audio format supported: mp3, wav, m4a, ogg
```

### Port Already in Use

```bash
# Change port in main.py or frontend/vite.config.js
```

### Missing Dependencies

```bash
# Reinstall everything
pip install --upgrade -r requirements.txt
cd frontend && npm install && cd ..
```

## Next Steps

- Add more entries to build your memory graph
- Explore Neo4j Browser to see relationships
- Try different search queries
- Add tags to organize memories
- Upload photos with text to test OCR

## Architecture Overview

```
┌─────────────┐         ┌──────────────┐         ┌──────────┐
│   Frontend  │ ◄────► │   Backend    │ ◄────► │  Neo4j   │
│   (React)   │         │  (FastAPI)   │         │ Database │
└─────────────┘         └──────────────┘         └──────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
              ┌─────▼─────┐      ┌─────▼─────┐
              │  Whisper  │      │ Embeddings│
              │  (Audio)  │      │ (Semantic)│
              └───────────┘      └───────────┘
```

## Features at a Glance

✅ **Multi-modal Input** - Text, speech, images
✅ **Semantic Search** - Understand context, not just keywords
✅ **Graph Storage** - Find relationships between memories
✅ **Smart Summarization** - Get answers from your past
✅ **Media Retrieval** - View original images and audio
✅ **Tags & Organization** - Structure your diary
✅ **Timestamps** - Chronological timeline

## Tips for Best Results

1. **Use descriptive text** - More context = better search
2. **Add relevant tags** - Organize your memories
3. **Upload photos** - Visual context matters
4. **Speak clearly** - Better transcription quality
5. **Be consistent** - Regular entries build better graphs
6. **Mix modalities** - Combine text, images, and audio

Happy journaling! 📔✨




