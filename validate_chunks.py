import json
from pathlib import Path

INPUT_FILE = "C:/Users/gihan/OneDrive/data/processed/chunked_documents.json"
OUTPUT_FILE = "C:/Users/gihan/OneDrive/data/processed/chunked_documents_cleaned.json"

required_fields = ["content", "metadata"]
required_metadata = ["chunk_id", "filename", "source"]

valid_chunks = []
invalid_count = 0

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

for chunk in chunks:
    if not isinstance(chunk, dict):
        invalid_count += 1
        continue

    if not all(field in chunk for field in required_fields):
        invalid_count += 1
        continue

    meta = chunk["metadata"]
    if not isinstance(meta, dict) or not all(key in meta for key in required_metadata):
        invalid_count += 1
        continue

    valid_chunks.append(chunk)

# Save the cleaned file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(valid_chunks, f, indent=2)

print(f"✅ Validation complete. {len(valid_chunks)} valid chunks saved.")
print(f"⚠️  {invalid_count} invalid chunks were removed.")