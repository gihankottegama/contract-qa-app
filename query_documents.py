import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

# 🔐 Load OpenAI API Key
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# 🧠 Set up embedding + vector store
embedding_model = OpenAIEmbeddings(openai_api_key=openai_key)
CHROMA_DIR = "C:/Users/gihan/OneDrive/data/vector_store/chroma"

vectorstore = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embedding_model
)

# 🔍 Ask your question
while True:
    query = input("\n💬 Ask a question (or type 'exit' to quit): ").strip()
    if query.lower() in ("exit", "quit"):
        print("👋 Exiting...")
        break

    results = vectorstore.similarity_search(query, k=3)

    print("\n📌 Top Matches:\n")
    for i, doc in enumerate(results, 1):
        meta = doc.metadata
        print(f"--- Result {i} ---")
        print(f"Filename: {meta.get('filename', 'N/A')}")
        print(f"Chunk ID: {meta.get('chunk_id', 'N/A')}")
        print(f"Excerpt:\n{doc.page_content[:500]}")  # Truncate if long
        print("-" * 40)