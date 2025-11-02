"""
Fix model download by using huggingface_hub directly
"""
from huggingface_hub import snapshot_download
from pathlib import Path
import shutil
import os

print("=" * 60)
print("Fixing Model Download - Alternative Method")
print("=" * 60)
print("")

# Clear cache completely
cache_base = Path.home() / ".cache" / "huggingface"
cache_dir = cache_base / "hub"
model_pattern = "models--sentence-transformers--all-MiniLM-L6-v2"

print("Clearing all cache...")
if cache_dir.exists():
    for item in cache_dir.glob(f"{model_pattern}*"):
        if item.is_dir():
            print(f"Removing: {item}")
            try:
                shutil.rmtree(item, ignore_errors=True)
            except:
                pass

print("")
print("Downloading using huggingface_hub directly...")
print("Model: sentence-transformers/all-MiniLM-L6-v2")
print("This may take a few minutes...")
print("")

try:
    # Download to a temporary location first
    temp_dir = Path.home() / ".cache" / "temp_model_download"
    if temp_dir.exists():
        shutil.rmtree(temp_dir, ignore_errors=True)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Download using huggingface_hub
    model_path = snapshot_download(
        repo_id="sentence-transformers/all-MiniLM-L6-v2",
        cache_dir=str(cache_base),
        local_files_only=False
    )
    
    print(f"[OK] Model downloaded to: {model_path}")
    print("")
    print("Testing with sentence-transformers...")
    
    # Now try loading with sentence-transformers
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Test
    test_emb = model.encode("test")
    print(f"[OK] Model loaded and tested! Embedding shape: {test_emb.shape}")
    print("")
    print("=" * 60)
    print("[SUCCESS] Model is ready!")
    print("You can now run: python main.py")
    print("=" * 60)
    
except Exception as e:
    print("")
    print("=" * 60)
    print(f"[ERROR] Failed: {e}")
    print("=" * 60)
    print("")
    print("Alternative: The app will work without embeddings.")
    print("You can still:")
    print("- Create diary entries")
    print("- Store text, images, audio")
    print("- Search by keywords (basic search)")
    print("")
    print("For full semantic search, the model needs to download correctly.")
    exit(1)
