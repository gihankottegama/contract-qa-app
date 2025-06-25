import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# 🔐 Load API key
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# 📚 Load ChromaDB vector store
CHROMA_DIR = "C:/Users/gihan/OneDrive/data/vector_store/chroma"
embedding = OpenAIEmbeddings(openai_api_key=openai_key)
vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embedding)

# 🤖 Set up GPT-powered Q&A chain
llm = ChatOpenAI(openai_api_key=openai_key, temperature=0.2, model="gpt-3.5-turbo")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
    return_source_documents=True
)

# 💬 Ask questions interactively
while True:
    query = input("\n💬 Ask your contract question (or type 'exit'): ").strip()
    if query.lower() in ("exit", "quit"):
        print("👋 Goodbye!")
        break

    result = qa_chain(query)
    print("\n🧠 GPT Answer:\n", result["result"])

    print("\n📎 Sources:")
    for i, doc in enumerate(result["source_documents"], 1):
        print(f"{i}. {doc.metadata.get('filename')} — {doc.metadata.get('chunk_id')}")