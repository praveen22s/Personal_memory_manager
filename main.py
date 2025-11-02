"""
Personal Semantic Diary - Main Application
FastAPI backend for multi-modal diary entries with semantic search
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from datetime import datetime
from typing import List, Optional
import os
import aiofiles
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from diary.database import DiaryDatabase
from diary.models import EntryCreate, EntryResponse, SearchQuery
from diary.embeddings import EmbeddingService
from diary.speech import SpeechProcessor
from diary.image import ImageProcessor
from diary.graph_processor import GraphProcessor

# Initialize FastAPI app
app = FastAPI(
    title="Personal Semantic Diary",
    description="Intelligent diary with semantic search and multi-modal input",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
db = DiaryDatabase()
embeddings = EmbeddingService()
speech_processor = SpeechProcessor()
image_processor = ImageProcessor()

# Mount uploads directory
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.on_event("startup")
async def startup_event():
    """Initialize database connection and embeddings"""
    await db.connect()
    try:
        await embeddings.load_model()
    except Exception as e:
        print(f"[WARN] Could not load embedding model: {e}")
        print("[INFO] App will start but semantic search will use basic keyword matching")
    print("[OK] Backend services initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    await db.close()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Personal Semantic Diary",
        "version": "1.0.0"
    }


@app.post("/api/entries", response_model=EntryResponse)
async def create_entry(
    title: str = Form(None),
    text: str = Form(None),
    audio: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
    tags: Optional[str] = Form(None)
):
    """
    Create a new diary entry with text, audio, or image
    """
    try:
        entry_data = {
            "title": title or "Untitled",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Process text input
        if text:
            entry_data["text"] = text
        
        # Process audio input
        if audio:
            audio_filename = await save_file(audio, "audio")
            transcription = await speech_processor.transcribe(audio_filename)
            entry_data["audio_path"] = audio_filename
            entry_data["text"] = (entry_data.get("text", "") + " " + transcription).strip()
        
        # Process image input
        if image:
            image_filename = await save_file(image, "image")
            # Extract text from image (OCR if needed)
            image_text = await image_processor.process_image(image_filename)
            entry_data["image_path"] = image_filename
            entry_data["text"] = (entry_data.get("text", "") + " " + image_text).strip()
        
        # Create embeddings
        if entry_data.get("text"):
            try:
                entry_data["embedding"] = await embeddings.embed_text(entry_data["text"])
            except Exception as emb_error:
                print(f"[WARN] Could not generate embedding: {emb_error}")
                # Continue without embedding - entry will still be saved
                entry_data["embedding"] = None
        
        # Parse tags
        entry_data["tags"] = tags.split(",") if tags else []
        
        # Save to database
        entry = await db.create_entry(entry_data)
        
        return EntryResponse(**entry)
    
    except Exception as e:
        print(f"[ERROR] Failed to create entry: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create entry: {str(e)}")


@app.get("/api/entries", response_model=List[EntryResponse])
async def list_entries(skip: int = 0, limit: int = 100):
    """Get all diary entries"""
    try:
        entries = await db.get_all_entries(skip, limit)
        return [EntryResponse(**entry) for entry in entries]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/entries/{entry_id}", response_model=EntryResponse)
async def get_entry(entry_id: str):
    """Get a specific diary entry"""
    try:
        entry = await db.get_entry_by_id(entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        return EntryResponse(**entry)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search")
async def semantic_search(query: SearchQuery):
    """
    Perform semantic search on diary entries
    Returns relevant entries with similarity scores
    """
    try:
        # Generate query embedding
        query_embedding = await embeddings.embed_text(query.text)
        
        # Search in database
        results = await db.semantic_search(query_embedding, query.limit or 10)
        
        # Format results
        response = {
            "query": query.text,
            "results": results,
            "total": len(results)
        }
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/query")
async def answer_question(query: SearchQuery):
    """
    Answer natural language questions by searching and summarizing
    Example: "Tell me about the happiest moments in my life"
    """
    try:
        # Try semantic search first
        try:
            query_embedding = await embeddings.embed_text(query.text)
            if embeddings.model is not None and query_embedding is not None and query_embedding.sum() != 0:
                # Search relevant entries using embeddings
                results = await db.semantic_search(query_embedding, query.limit or 20)
            else:
                # Fallback to text search if embeddings unavailable
                results = await db.text_search(query.text, query.limit or 20)
        except Exception as emb_error:
            print(f"[WARN] Embedding search failed, using text search: {emb_error}")
            # Fallback to text-based search
            results = await db.text_search(query.text, query.limit or 20)
        
        # Generate summary
        summary = await embeddings.generate_summary(query.text, results) if results else "No results found."
        
        # Get media files
        media = []
        for result in results[:5]:  # Top 5 results
            if result.get("image_path"):
                media.append({"type": "image", "path": result["image_path"], "entry_id": result["id"]})
            if result.get("audio_path"):
                media.append({"type": "audio", "path": result["audio_path"], "entry_id": result["id"]})
        
        return {
            "query": query.text,
            "summary": summary,
            "relevant_entries": results[:10] if results else [],
            "media": media,
            "count": len(results) if results else 0
        }
    
    except Exception as e:
        print(f"[ERROR] Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/media/{entry_id}")
async def get_media(entry_id: str):
    """Serve media files for an entry"""
    try:
        entry = await db.get_entry_by_id(entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        
        if entry.get("image_path") and os.path.exists(entry["image_path"]):
            return FileResponse(entry["image_path"])
        elif entry.get("audio_path") and os.path.exists(entry["audio_path"]):
            return FileResponse(entry["audio_path"], media_type="audio/mpeg")
        else:
            raise HTTPException(status_code=404, detail="No media found")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/entries/{entry_id}")
async def delete_entry(entry_id: str):
    """Delete a diary entry"""
    try:
        success = await db.delete_entry(entry_id)
        if not success:
            raise HTTPException(status_code=404, detail="Entry not found")
        return {"status": "deleted", "id": entry_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def save_file(file: UploadFile, file_type: str) -> str:
    """Save uploaded file and return path"""
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    
    # Determine file extension
    ext = os.path.splitext(file.filename)[1] if file.filename else ".tmp"
    
    # Create filename
    if file_type == "audio":
        ext = ext if ext in [".mp3", ".wav", ".m4a", ".ogg"] else ".mp3"
    elif file_type == "image":
        ext = ext if ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"] else ".png"
    
    filename = f"{file_type}_{timestamp}{ext}"
    filepath = os.path.join("uploads", filename)
    
    # Save file
    async with aiofiles.open(filepath, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return filepath


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
