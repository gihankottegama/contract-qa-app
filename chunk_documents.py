import os
import json
from pathlib import Path
from load_documents import load_documents_from_directory
from smart_chunker import smart_chunk

# Paths
INPUT_DIR = "C:/Users/gihan/OneDrive/data/raw"
OUTPUT_FILE = "C:/Users/gihan/OneDrive/data/processed/chunked_documents.json"

# Load all documents
docs = load_documents_from_directory(INPUT_DIR)
print(f"Loaded {len(docs)} documents for chunking.")

# Initialize list to hold chunks
chunked_docs = []

# Chunk and tag
for doc in docs:
    try:
        chunks = smart_chunk(doc.page_content, doc.metadata.get("doc_type", "generic"))
        for i, chunk in enumerate(chunks):
            chunked_docs.append({
                "content": chunk,
                "metadata": {
                    **doc.metadata,
                    "chunk_id": f"{Path(doc.metadata['source_path']).stem}_chunk{i+1}"
                }
            })
    except Exception as e:
        print(f"Skipping document due to error: {doc.metadata.get('filename', 'Unknown')} — {e}")

# Save chunks to JSON
os.makedirs(Path(OUTPUT_FILE).parent, exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(chunked_docs, f, indent=2)

print(f"\n✅ Chunking complete: {len(chunked_docs)} chunks saved to {OUTPUT_FILE}")