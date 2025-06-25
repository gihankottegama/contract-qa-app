import os
from pathlib import Path
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    TextLoader
)
from extract_metadata import extract_metadata_from_path  # Make sure this file is in the same folder or adjust the import

def load_documents_from_directory(directory_path):
    documents = []
    for file_path in Path(directory_path).rglob("*"):
        if file_path.is_file():
            if file_path.suffix.lower() == ".pdf":
                loader = PyPDFLoader(str(file_path))
            elif file_path.suffix.lower() == ".docx":
                loader = UnstructuredWordDocumentLoader(str(file_path))
            elif file_path.suffix.lower() == ".txt":
                loader = TextLoader(str(file_path))
            else:
                print(f"Skipping unsupported file: {file_path}")
                continue

            try:
                docs = loader.load()
                for doc in docs:
                    doc.metadata["source_path"] = str(file_path)
                    doc.metadata.update(extract_metadata_from_path(file_path))
                    documents.append(doc)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
    return documents

if __name__ == "__main__":

print("Running load_documents.py...")
    input_dir = "data/raw"
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)

    docs = load_documents_from_directory(input_dir)
    print(f"Loaded {len(docs)} documents.")

    # Optional: Save each document's content and metadata
    for i, doc in enumerate(docs):
        filename = f"{output_dir}/doc_{i+1}_{doc.metadata.get('doc_type', 'unknown')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("--- Metadata ---\n")
            for key, value in doc.metadata.items():
                f.write(f"{key}: {value}\n")
            f.write("\n--- Content ---\n")
            f.write(doc.page_content)