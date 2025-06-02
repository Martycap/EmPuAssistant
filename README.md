# 📚 EmpuAssistant – Virtual Assistant for Empulia Documentation
EmpuAssistant is an NLP-based virtual assistant designed to help users navigate and understand the practical guides and manuals published on the Empulia portal. The project leverages open-source language models and semantic search to enable natural language question answering over official documentation.

## 🔍 Main Features
- Web scraping & preprocessing of official PDFs from the Empulia site

- Text extraction with PyMuPDF and chunking strategy

- Embedding generation using SentenceTransformers (all-MiniLM-L6-v2)

- Semantic retrieval via FAISS for document similarity

- Local inference using llama-cpp-python and a quantized .gguf model (e.g., TinyLlama)

- RAG pipeline (Retrieval-Augmented Generation) that answers questions based on real content

## ⚙️ Technologies

- Python

- FAISS

- SentenceTransformers

- llama-cpp-python

- LangChain (optional extension)

## 🎓 Academic Context
This project was developed as part of an NLP course assignment, with the goal of exploring practical applications of local language models and document intelligence in public administration.

##🗂 Structure

├── docs/         # Preprocessed .txt documents extracted from Empulia PDFs
├── model/        # Quantized LLM model (.gguf)
├── db/           # FAISS index for retrieval
├── app.py        # Main pipeline: retrieval + LLM response
└── README.md     # Project description and setup
