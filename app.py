import os
import json
import streamlit as st
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_core.documents import Document

# Load API key
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# Initialize embedding model
embedding = OpenAIEmbeddings(openai_api_key=openai_key)

# Load documents from JSONL
documents = []
with open(r"C:\Users\gihan\OneDrive\data\processedchunked_documents_min.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        documents.append(Document(page_content=item["content"], metadata=item["metadata"]))

# Build FAISS vector store in memory
vectorstore = FAISS.from_documents(documents, embedding)

# Setup LLM and RetrievalQA chain
llm = ChatOpenAI(openai_api_key=openai_key, temperature=0.2, model="gpt-3.5-turbo")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
    return_source_documents=True
)

# --- Streamlit UI ---
st.set_page_config(page_title="Ask Your Docs", layout="centered")
st.title("📄 Contract Q&A Assistant")

query = st.text_input("Ask a contract-related question:")
if query:
    with st.spinner("Thinking..."):
        result = qa_chain(query)
        st.markdown("### 🧠 Answer")
        st.write(result["result"])

        st.markdown("### 📎 Sources")
        for i, doc in enumerate(result["source_documents"], 1):
            meta = doc.metadata
            st.write(f"**{i}.** {meta.get('filename', 'Unknown')} — `{meta.get('chunk_id')}`")