# 🚀 START HERE

Welcome to **Personal Semantic Diary** - Your AI-powered memory companion!

## What is This?

This is a complete, production-ready personal diary application that uses:
- **AI & Machine Learning** for understanding your memories
- **Graph Databases** for smart relationships
- **Natural Language Processing** for intelligent search
- **Multi-modal Input** for text, voice, and images

Unlike traditional diaries, this one **understands context** and can answer questions like "Tell me about the happiest moments in my life."

## Quick Start

### Prerequisites
- ✅ Python 3.9+
- ✅ Node.js 18+
- ✅ Neo4j (Desktop or Aura)
- ✅ FFmpeg

### Installation (5 Minutes)

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Neo4j:**
   - Install Neo4j Desktop
   - Create a database
   - Note your connection details

3. **Configure environment:**
   ```bash
   # Copy the example
   copy .env.example .env
   # Edit .env with your Neo4j credentials
   ```

4. **Install frontend:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

5. **Run the app:**
   ```bash
   # Windows:
   run.bat
   
   # Mac/Linux:
   ./run.sh
   ```

6. **Open browser:**
   ```
   http://localhost:5173
   ```

## Your First Entry

1. Click **"New Entry"**
2. Write some text or record audio
3. Add tags like "happy", "work"
4. Click **"Save Entry"**

## Try the Magic ✨

Click **"Search"** and ask:
- "Tell me about happy moments"
- "What did I learn today?"
- "Show me work memories"

Watch as the AI searches across ALL your entries semantically!

## Project Structure

```
📁 project_final_year/
├── 📁 diary/              # Backend modules
│   ├── database.py        # Neo4j integration
│   ├── embeddings.py      # AI embeddings
│   ├── speech.py          # Audio transcription
│   └── image.py           # Image OCR
├── 📁 frontend/           # React UI
│   ├── src/
│   │   ├── components/
│   │   └── App.jsx
├── main.py               # FastAPI backend
├── requirements.txt      # Python deps
└── 📄 Documentation
    ├── README.md         # Main readme
    ├── QUICKSTART.md     # Quick guide
    ├── SETUP.md          # Detailed setup
    ├── ARCHITECTURE.md   # System design
    ├── FEATURES.md       # Feature list
    └── PROJECT_OVERVIEW.md # Full overview
```

## Key Features

### 🎨 Multi-Modal Input
- Type your thoughts
- Record voice notes
- Upload photos

### 🧠 Semantic Search
- Ask in natural language
- Get contextual answers
- See similarity scores

### 📊 Graph Storage
- Neo4j relationships
- Similarity connections
- Tag organization

### 🖼️ Media Retrieval
- View original images
- Play audio recordings
- Timestamped entries

## Technology Highlights

- **FastAPI**: Modern Python backend
- **Neo4j**: Graph database
- **React**: Beautiful UI
- **Whisper**: Speech-to-text
- **Transformers**: AI embeddings
- **Tesseract**: Image OCR

## Common Questions

**Q: Do I need to be online?**  
A: Only for initial setup. After that, everything runs locally!

**Q: Is my data private?**  
A: 100%! Everything stays on your machine.

**Q: How big can my diary be?**  
A: Limited only by your disk space. Handles thousands of entries.

**Q: Can I export my data?**  
A: Yes! Your Neo4j database and uploads folder contain everything.

## Troubleshooting

**Neo4j won't connect?**
- Check .env credentials
- Ensure Neo4j is running
- Verify firewall settings

**Audio not working?**
- Install FFmpeg
- Check browser permissions
- Verify audio format

**Module errors?**
- Run: `pip install -r requirements.txt`
- Check Python version: 3.9+

## Next Steps

1. ✅ Get it running (follow Quick Start)
2. ✅ Add some entries
3. ✅ Try searches
4. 📖 Read ARCHITECTURE.md to understand design
5. 🎨 Customize the UI in frontend/
6. 🤖 Enhance AI in diary/embeddings.py

## Learn More

📖 **[QUICKSTART.md](QUICKSTART.md)** - Installation guide  
🏗️ **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design  
🎯 **[FEATURES.md](FEATURES.md)** - Complete features  
📊 **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Full overview  

## Support

Check the documentation files for detailed information:
- Setup issues → SETUP.md
- Architecture questions → ARCHITECTURE.md
- Feature requests → FEATURES.md

## What Makes This Special?

This isn't just a diary app. It's a demonstration of:

✅ **Full-Stack Development** (Frontend + Backend)  
✅ **AI/ML Integration** (Embeddings, NLP, Speech)  
✅ **Graph Database Design** (Neo4j relationships)  
✅ **Modern Architecture** (FastAPI, React, Async)  
✅ **Production Quality** (Error handling, validation)  

Perfect for final year projects or portfolio pieces!

---

**Ready to start? Follow the Quick Start guide above! 🚀**

Enjoy your Personal Semantic Diary! 📔✨




