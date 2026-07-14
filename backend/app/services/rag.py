"""
RAG (Retrieval-Augmented Generation) service.

Flow:
  1. Documents are chunked and embedded with a local sentence-transformer model
  2. Chunks stored in ChromaDB (local, persistent vector store)
  3. On a query: embed question -> similarity search -> top-k chunks
  4. Chunks + question sent to a local LLM (via Ollama) with a strict
     "answer only from context" prompt
  5. Retrieval similarity score is returned as a confidence value —
     low confidence = likely a knowledge-base gap (a great dashboard metric)
"""
import chromadb
from sentence_transformers import SentenceTransformer
import ollama
import os
from pypdf import PdfReader

CHROMA_PATH = "./chroma_store"
COLLECTION_NAME = "company_kb"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

_embedder = SentenceTransformer("all-MiniLM-L6-v2")  # small, fast, CPU-friendly
_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _client.get_or_create_collection(name=COLLECTION_NAME)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 80) -> list[str]:
    """Simple sliding-window chunking by characters. Good enough for policy docs/FAQs."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return [c.strip() for c in chunks if c.strip()]


def extract_text(filepath: str) -> str:
    if filepath.lower().endswith(".pdf"):
        reader = PdfReader(filepath)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def ingest_document(filepath: str, filename: str) -> int:
    """Chunk, embed, and store a document. Returns number of chunks stored."""
    text = extract_text(filepath)
    chunks = chunk_text(text)
    if not chunks:
        return 0

    embeddings = _embedder.encode(chunks).tolist()
    ids = [f"{filename}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]

    _collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )
    return len(chunks)


def retrieve(query: str, top_k: int = 4):
    """Return top-k relevant chunks + a confidence score (0-1, higher = more relevant)."""
    query_embedding = _embedder.encode([query]).tolist()
    results = _collection.query(query_embeddings=query_embedding, n_results=top_k)

    if not results["documents"] or not results["documents"][0]:
        return [], [], 0.0

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]  # lower = more similar (cosine distance)

    # Convert distance -> a rough 0-1 confidence score
    confidence = max(0.0, 1 - (sum(distances) / len(distances)))
    sources = list({m["source"] for m in metas})

    return docs, sources, round(confidence, 3)


def generate_answer(question: str, context_chunks: list[str]) -> str:
    """Call local Ollama model, grounded strictly in retrieved context."""
    context = "\n\n---\n\n".join(context_chunks)

    prompt = f"""You are a helpful customer support assistant. Answer the customer's
question using ONLY the information in the context below. If the context does not
contain the answer, say clearly that you don't have that information and that the
ticket will be escalated to a human agent. Do not make anything up.

Context:
{context}

Customer question: {question}

Answer concisely and professionally:"""

    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]
    except Exception as e:
        return (
            "I'm unable to reach the local model right now "
            f"(is Ollama running? `ollama serve`). Error: {e}"
        )


def answer_query(question: str, top_k: int = 4):
    chunks, sources, confidence = retrieve(question, top_k=top_k)
    if not chunks:
        return {
            "answer": "I couldn't find anything relevant in the knowledge base. This will be escalated to a human agent.",
            "sources": [],
            "confidence": 0.0,
        }
    answer = generate_answer(question, chunks)
    return {"answer": answer, "sources": sources, "confidence": confidence}
