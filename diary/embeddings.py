"""
Embedding service for semantic search and summarization
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
import torch


class EmbeddingService:
    """Service for generating and managing embeddings"""
    
    def __init__(self):
        self.model = None
        self.model_name = "all-MiniLM-L6-v2"  # 384 dimensions, fast and efficient
    
    async def load_model(self):
        """Load the sentence transformer model"""
        print("Loading embedding model...")
        try:
            # Try loading directly first
            self.model = SentenceTransformer(self.model_name)
            print("[OK] Embedding model loaded")
        except (FileNotFoundError, OSError, Exception) as e:
            print(f"[WARN] Model cache issue detected: {e}")
            print("Attempting to fix by clearing ALL cache and re-downloading...")
            try:
                import shutil
                import os
                from pathlib import Path
                
                # Find and clear ALL related cache
                cache_base = Path.home() / ".cache" / "huggingface"
                cache_dir = cache_base / "hub"
                
                # Clear the entire model cache directory
                model_cache_pattern = "models--sentence-transformers--all-MiniLM-L6-v2"
                
                print("Clearing all related cache...")
                
                # Remove the main model cache
                if cache_dir.exists():
                    for item in cache_dir.glob(f"{model_cache_pattern}*"):
                        if item.is_dir():
                            print(f"Removing: {item}")
                            try:
                                shutil.rmtree(item, ignore_errors=True)
                            except Exception:
                                pass
                    
                    # Also check snapshots directory
                    for item in cache_dir.rglob("*sentence-transformers*all-MiniLM-L6-v2*"):
                        if item.is_dir():
                            print(f"Removing snapshot: {item}")
                            try:
                                shutil.rmtree(item, ignore_errors=True)
                            except Exception:
                                pass
                
                # Force fresh download - use default cache but ensure clean download
                import tempfile
                
                print("Re-downloading model with fresh cache (this may take a few minutes, ~420MB)...")
                print("Please be patient, downloading from HuggingFace...")
                
                # Try downloading to a temporary location first, then move
                # This avoids cache corruption issues
                try:
                    # Use default cache but force re-download
                    from huggingface_hub import snapshot_download
                    import os
                    
                    # Clear any environment variables that might interfere
                    if 'TRANSFORMERS_CACHE' in os.environ:
                        del os.environ['TRANSFORMERS_CACHE']
                    if 'HF_HOME' in os.environ:
                        del os.environ['HF_HOME']
                    
                    # Direct download approach - let sentence-transformers handle it
                    print("Downloading model files...")
                    self.model = SentenceTransformer(self.model_name)
                    
                except Exception as download_error:
                    print(f"[WARN] Direct download failed: {download_error}")
                    print("[INFO] Trying alternative download method...")
                    
                    # Last resort: use a simpler model or skip
                    print("[WARN] Using fallback - model will be None")
                    print("[INFO] You can manually install with: pip install --upgrade sentence-transformers")
                    raise download_error
                print("[OK] Embedding model loaded successfully")
            except Exception as e2:
                print(f"[ERROR] Failed to load embedding model after retry: {e2}")
                print("[WARN] App will start but semantic search will be limited")
                print("[INFO] You can try running 'python fix_model_cache.py' manually")
                self.model = None
    
    async def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for a text string"""
        if not text or not text.strip():
            return np.zeros(384)
        
        if self.model is None:
            await self.load_model()
        
        if self.model is None:
            # Return zero vector if model failed to load
            return np.zeros(384)
        
        # Generate embedding
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    async def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for multiple texts"""
        if self.model is None:
            await self.load_model()
        
        if self.model is None:
            # Return zero vectors if model failed to load
            return np.zeros((len(texts), 384))
        
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings
    
    async def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between two embeddings"""
        similarity = np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )
        return float(similarity)
    
    async def generate_summary(self, query: str, results: List[Dict]) -> str:
        """
        Generate a contextual summary from search results
        This is a simple implementation - you could enhance with LLMs
        """
        if not results:
            return "No relevant memories found."
        
        # Simple summarization based on top results
        relevant_texts = []
        for result in results[:5]:  # Top 5 results
            if result.get("text"):
                relevant_texts.append(f"- {result.get('text', '')[:200]}")
        
        if not relevant_texts:
            return "Found relevant entries but no detailed content."
        
        # Generate a basic summary
        summary = f"Based on your query '{query}', here are your relevant memories:\n\n"
        summary += "\n".join(relevant_texts)
        
        # Add timestamp context if available
        if results[0].get("timestamp"):
            summary += f"\n\nMost relevant memory from: {results[0]['timestamp']}"
        
        return summary
    
    async def cluster_similar(self, embeddings: np.ndarray, threshold: float = 0.75) -> List[List[int]]:
        """Cluster similar embeddings together"""
        if len(embeddings) < 2:
            return [[0]] if len(embeddings) == 1 else []
        
        clusters = []
        used = set()
        
        for i, emb1 in enumerate(embeddings):
            if i in used:
                continue
            
            cluster = [i]
            used.add(i)
            
            for j, emb2 in enumerate(embeddings[i+1:], start=i+1):
                if j in used:
                    continue
                
                similarity = await self.similarity(emb1, emb2)
                if similarity >= threshold:
                    cluster.append(j)
                    used.add(j)
            
            clusters.append(cluster)
        
        return clusters



