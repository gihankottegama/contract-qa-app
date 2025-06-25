import os
from pathlib import Path

PROCESSED_DIR = "C:/Users/gihan/OneDrive/data/processed"

deleted_count = 0

for file in Path(PROCESSED_DIR).glob("*.txt"):
    try:
        file.unlink()
        print(f"Deleted: {file.name}")
        deleted_count += 1
    except Exception as e:
        print(f"Error deleting {file.name}: {e}")

print(f"\n✅ Cleanup complete: {deleted_count} .txt files deleted from {PROCESSED_DIR}")