from pathlib import Path

def extract_metadata_from_path(file_path: Path) -> dict:
    """
    Extracts smart metadata from a document file path.
    Assumes structure like:
    data/raw/<category>/<doc_type>/<sub_type>/filename.pdf
    """
    parts = file_path.parts
    metadata = {}

    # Try to locate 'raw' in path to index relative segments
    if "raw" in parts:
        try:
            raw_index = parts.index("raw")
            metadata["category"] = parts[raw_index + 1]           # static or dynamic
            metadata["doc_type"] = parts[raw_index + 2]           # letters, reports, etc.
            if len(parts) > raw_index + 3:
                metadata["sub_type"] = parts[raw_index + 3]       # client, weekly, etc.
        except IndexError:
            pass  # In case the path is incomplete

    # Optional: infer semantic metadata from folder names
    folder_keywords = [p.lower() for p in parts]

    if any(k in folder_keywords for k in {"client", "incoming"}):
        metadata["direction"] = "incoming"
    elif "outgoing" in folder_keywords:
        metadata["direction"] = "outgoing"

    if any(k in folder_keywords for k in {"daily", "weekly", "monthly"}):
        metadata["frequency"] = next((k for k in folder_keywords if k in {"daily", "weekly", "monthly"}), None)

    # Assign base filename for traceability
    metadata["filename"] = file_path.name

    return metadata