import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_contract(text):
    # Split by "Clause X.X" pattern
    clauses = re.split(r"(Clause\s+\d+(\.\d+)*\s*[-:]?)", text)
    chunks = []
    for i in range(1, len(clauses), 2):
        header = clauses[i].strip()
        body = clauses[i+1].strip() if i+1 < len(clauses) else ""
        chunks.append(f"{header}\n{body}")
    return chunks

def chunk_report(text):
    # Split by common report section headers
    sections = re.split(r"(Work Done|Weather|Resources|Site Instructions|Delays)", text, flags=re.IGNORECASE)
    return [s.strip() for s in sections if s.strip()]

def chunk_letter(text):
    # Paragraph-based splitting
    return [p.strip() for p in text.split("\n\n") if p.strip()]

def chunk_default(text):
    # Fallback: recursive splitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return splitter.split_text(text)

def smart_chunk(text, doc_type):
    if "contract" in doc_type:
        return chunk_contract(text)
    elif "report" in doc_type:
        return chunk_report(text)
    elif "letter" in doc_type:
        return chunk_letter(text)
    else:
        return chunk_default(text)