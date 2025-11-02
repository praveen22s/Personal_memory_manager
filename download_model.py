"""
Manually download the embedding model to fix cache issues
"""
from sentence_transformers import SentenceTransformer
import shutil
from pathlib import Path

print("=" * 60)
print("Manual Model Download Tool")
print("=" * 60)
print("")

print("This will:")
print("1. Clear any corrupted cache")
print("2. Download the model fresh")
print("3. Verify it works")
print("")

cache_base = Path.home() / ".cache" / "huggingface"
cache_dir = cache_base / "hub"

# Clear cache
model_pattern = "models--sentence-transformers--all-MiniLM-L6-v2"
if cache_dir.exists():
    for item in cache_dir.glob(f"{model_pattern}*"):
        if item.is_dir():
            print(f"Clearing: {item}")
            try:
                shutil.rmtree(item, ignore_errors=True)
            except:
                pass

print("")
print("Downloading model: all-MiniLM-L6-v2")
print("This may take a few minutes (~420MB)...")
print("")

try:
    # Download the model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Test it works
    test_text = "Hello world"
    embedding = model.encode(test_text)
    
    print("")
    print("=" * 60)
    print("[OK] Model downloaded and tested successfully!")
    print(f"Test embedding shape: {embedding.shape}")
    print("=" * 60)
    print("")
    print("You can now run: python main.py")
    print("The model should load correctly.")
    
except Exception as e:
    print("")
    print("=" * 60)
    print(f"[ERROR] Failed to download model: {e}")
    print("=" * 60)
    print("")
    print("Troubleshooting:")
    print("1. Check internet connection")
    print("2. Try: pip install --upgrade sentence-transformers")
    print("3. Try: pip install --upgrade huggingface_hub")
    exit(1)
