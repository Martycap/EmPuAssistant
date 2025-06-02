import os
from pathlib import Path
from llama_cpp import Llama
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

### --- CONFIG ---
DOCS_FOLDER = "./data/TEXT"
MODEL_PATH = "./src/model/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
N_THREADS = 8
CTX_WINDOW = 2048
TOP_K = 3
### -------------

# 1. Carica documento da cartella
def load_documents(folder):
    docs = []
    sources = []
    for file in Path(folder).rglob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()
            docs.append(text)
            sources.append(str(file.name))
    return docs, sources

# 2. Spezzetta e embeddizza
def embed_documents(docs, embedder):
    chunks, metadata = [], []
    for idx, doc in enumerate(docs):
        for i in range(0, len(doc), 500):
            chunk = doc[i:i+500]
            chunks.append(chunk)
            metadata.append((idx, i))
    vectors = embedder.encode(chunks, convert_to_numpy=True)
    return chunks, metadata, vectors

# 3. Inizializza FAISS
def build_faiss_index(vectors):
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    return index

# 4. Recupera i top-k più simili
def retrieve(query, embedder, index, chunks, metadata, sources):
    q_vec = embedder.encode([query])
    D, I = index.search(q_vec, TOP_K)
    results = []
    for i in I[0]:
        idx, offset = metadata[i]
        results.append((chunks[i], sources[idx]))
    return results

# 5. Inizializza il modello LLaMA
def load_llm():
    return Llama(
        model_path=MODEL_PATH,
        chat_format="chatml",
        n_threads=N_THREADS,
        n_ctx=CTX_WINDOW,
        n_gpu_layers=0  # CPU only
    )

# 6. Costruisci prompt con contesto
def build_prompt(context_chunks, query):
    context_text = "\n\n".join([f"- {text}" for text, _ in context_chunks])
    prompt = (
        f"<|system|>\nSei un assistente utile che risponde basandosi solo sui manuali forniti.\n</s>\n"
        f"<|user|>\nContesto:\n{context_text}\n\nDomanda: {query}\n</s>\n"
        f"<|assistant|>"
    )
    return prompt

### MAIN FLOW
if __name__ == "__main__":
    print("Carico i documenti...")
    raw_docs, sources = load_documents(DOCS_FOLDER)

    print("Creo gli embeddings...")
    embedder = SentenceTransformer(EMBED_MODEL_NAME)
    chunks, metadata, vectors = embed_documents(raw_docs, embedder)
    index = build_faiss_index(vectors)

    print("Inizializzo LLaMA...")
    llm = load_llm()

    print("Assistant pronto. Scrivi una domanda, o 'exit' per uscire.")
    while True:
        query = input("\n Domanda: ")
        if query.strip().lower() in ("exit", "quit"):
            break

        context = retrieve(query, embedder, index, chunks, metadata, sources)
        prompt = build_prompt(context, query)

        output = llm(prompt, max_tokens=512, stop=["</s>"])
        answer = output["choices"][0]["text"]

        print("\n Risposta:", answer.strip())
        print("\n Fonti:", [src for _, src in context])
