"""
Create the missing config_sentence_transformers.json file
"""
from pathlib import Path
import json

print("Creating missing config file...")

cache_base = Path.home() / ".cache" / "huggingface"
model_dir = cache_base / "hub" / "models--sentence-transformers--all-MiniLM-L6-v2" / "snapshots" / "c9745ed1d9f207416be6d2e6f8de32d1f16199bf"

config_file = model_dir / "config_sentence_transformers.json"

print(f"Checking: {config_file}")

if config_file.exists():
    print("[OK] Config file already exists!")
    with open(config_file) as f:
        config = json.load(f)
    print(f"Config: {config}")
else:
    print("[FIX] Creating config file...")
    
    # Create directory if needed
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # Create minimal config
    config = {
        "max_seq_length": 256,
        "do_lower_case": False
    }
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"[OK] Created: {config_file}")

# Also check for the path with double backslash issue
# Try to access it the way sentence-transformers might
import os
alt_path = str(model_dir) + '\\.\\config_sentence_transformers.json'
print(f"\nChecking alternative path: {alt_path}")

if os.path.exists(alt_path.replace('\\.\\', '\\')):
    print("[OK] File exists (without double backslash)")
    # Try creating a symlink or copy
    normalized_path = Path(alt_path.replace('\\.\\', '\\'))
    if normalized_path.exists() and not Path(alt_path).exists():
        print("[INFO] The path issue is in how sentence-transformers accesses the file")
        print("[INFO] This is a known issue with sentence-transformers on Windows")

print("\nTesting model load...")
try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    test = model.encode("test")
    print(f"[SUCCESS] Model works! Shape: {test.shape}")
except Exception as e:
    print(f"[ERROR] Still failing: {e}")
    print("\n[INFO] The app will work without embeddings for now.")
