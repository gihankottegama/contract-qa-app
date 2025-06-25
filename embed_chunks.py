import os
import json
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from pathlib import Path
from dotenv import load_dotenv

# 🗝️ Load your OpenAI API key from .env file (recommended)
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# 📂 Paths
CHUNKS_FILE = "C:/Users/gihan/OneDrive/data/processed/chunked_documents_cleaned.json"
CHROMA_DIR = "C:/Users/gihan/OneDrive/data/vector_store/chroma"

# ✅ Load chunks
with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    raw_chunks = json.load(f)

documents = [
    Document(page_content=chunk["content"], metadata=chunk["metadata"])
    for chunk in raw_chunks
]

print(f"Loaded {len(documents)} chunks for embedding...")

# 🤖 Set up OpenAI embeddings
embedding_model = OpenAIEmbeddings(openai_api_key=openai_key)

# 🧠 Create vector store
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embedding_model,
    persist_directory=CHROMA_DIR
)

vectorstore.persist()
print(f"\n✅ All chunks embedded and stored in ChromaDB at: {CHROMA_DIR}")