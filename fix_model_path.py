"""
Fix model path by moving files to correct location
"""
import shutil
from pathlib import Path
import os

print("=" * 60)
print("Fixing Model Path Location")
print("=" * 60)
print("")

cache_base = Path.home() / ".cache" / "huggingface"
wrong_location = cache_base / "models--sentence-transformers--all-MiniLM-L6-v2"
correct_location = cache_base / "hub" / "models--sentence-transformers--all-MiniLM-L6-v2"

print(f"Looking for model in wrong location: {wrong_location}")
print(f"Should be in: {correct_location}")
print("")

if wrong_location.exists() and not correct_location.exists():
    print("[FIX] Moving model to correct location...")
    
    # Create hub directory if it doesn't exist
    (cache_base / "hub").mkdir(parents=True, exist_ok=True)
    
    # Move the entire directory
    try:
        shutil.move(str(wrong_location), str(correct_location))
        print(f"[OK] Moved model to: {correct_location}")
    except Exception as e:
        print(f"[WARN] Move failed: {e}")
        print("[INFO] Trying copy instead...")
        try:
            shutil.copytree(str(wrong_location), str(correct_location))
            print(f"[OK] Copied model to: {correct_location}")
        except Exception as e2:
            print(f"[ERROR] Copy also failed: {e2}")
            exit(1)
    
    # Also fix the path issue with the double backslash
    # The issue is in how sentence-transformers constructs paths
    # We need to ensure the config file exists in the snapshot directory
    snapshot_dir = correct_location / "snapshots" / "c9745ed1d9f207416be6d2e6f8de32d1f16199bf"
    if snapshot_dir.exists():
        config_file = snapshot_dir / "config_sentence_transformers.json"
        if not config_file.exists():
            # Create a minimal config if missing
            import json
            minimal_config = {
                "max_seq_length": 256,
                "do_lower_case": False
            }
            with open(config_file, 'w') as f:
                json.dump(minimal_config, f)
            print(f"[OK] Created missing config file: {config_file}")
    
    print("")
    print("[OK] Path fixed! Now testing...")
    print("")
    
    # Test loading
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        test_emb = model.encode("test")
        print(f"[SUCCESS] Model loaded! Embedding shape: {test_emb.shape}")
        print("")
        print("You can now run: python main.py")
    except Exception as e:
        print(f"[ERROR] Still failing: {e}")
        print("")
        print("The app will still work, but semantic search will be limited.")
        print("You can create entries and search by keywords.")
        
elif correct_location.exists():
    print("[OK] Model is already in correct location!")
    print(f"Location: {correct_location}")
else:
    print("[INFO] Model not found. It will download on first use.")
    print("You can run: python main.py")

print("=" * 60)
