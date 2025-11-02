"""
Fix corrupted model cache by completely clearing and re-downloading
"""
import shutil
from pathlib import Path
import os

print("=" * 50)
print("Fixing Corrupted Model Cache")
print("=" * 50)
print("")

cache_base = Path.home() / ".cache" / "huggingface"
cache_dir = cache_base / "hub"
model_pattern = "sentence-transformers--all-MiniLM-L6-v2"

print(f"Cache base: {cache_base}")
print(f"Hub cache: {cache_dir}")
print(f"Looking for: *{model_pattern}*")
print("")

if not cache_dir.exists():
    print(f"[INFO] Cache directory doesn't exist: {cache_dir}")
    print("[OK] Ready for fresh download")
    exit(0)

# Find and remove ALL related cache
removed_count = 0

# Method 1: Remove by exact pattern
exact_pattern = f"models--{model_pattern}"
for item in cache_dir.glob(f"{exact_pattern}*"):
    if item.is_dir():
        print(f"[1] Found: {item}")
        try:
            shutil.rmtree(item, ignore_errors=True)
            removed_count += 1
            print(f"     [OK] Removed")
        except Exception as e:
            print(f"     [WARN] Error: {e}")

# Method 2: Remove any directories containing the model name
print("")
print("Searching for related cache directories...")
for item in cache_dir.rglob("*"):
    if item.is_dir() and model_pattern in str(item):
        print(f"[2] Found: {item}")
        try:
            shutil.rmtree(item, ignore_errors=True)
            removed_count += 1
            print(f"     [OK] Removed")
        except Exception as e:
            print(f"     [WARN] Error: {e}")

# Method 3: Clear snapshots that might be corrupted
snapshots_dir = cache_dir
for item in snapshots_dir.rglob("*all-MiniLM-L6-v2*"):
    if item.is_dir() and "snapshot" in str(item):
        print(f"[3] Found snapshot: {item}")
        try:
            shutil.rmtree(item, ignore_errors=True)
            removed_count += 1
            print(f"     [OK] Removed")
        except Exception as e:
            print(f"     [WARN] Error: {e}")

print("")
print("=" * 50)
if removed_count > 0:
    print(f"[OK] Cleared {removed_count} cache directory/directories")
    print("[OK] Corrupted cache removed!")
    print("")
    print("Next steps:")
    print("1. Run: python main.py")
    print("2. The model will download fresh (~420MB)")
    print("3. This may take a few minutes on first startup")
else:
    print("[INFO] No cache directories found to remove")
    print("[INFO] Cache may already be cleared or never downloaded")
    print("")
    print("Next steps:")
    print("1. Run: python main.py")
    print("2. The model will download automatically")

print("=" * 50)