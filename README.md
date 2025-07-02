# EmPuAssistant 
**Virtual Assistant for EmPULIA Documentation**  
Martina Capone – University of Bari Aldo Moro, Italy


## Overview

**EmPuAssistant** is a virtual assistant powered by LLMs that answers questions based on institutional documentation from the **EmPULIA** platform, through a two-phase semantic pipeline:

- **Phase 1 – KG Construction**: scraping official PDFs, text reformulation with ANITA, RDF triple extraction, and knowledge graph generation.
- **Phase 2 – RAG QA**: user query → relevant triples retrieval → grounded answer generated via ANITA or Mistral.

> Includes an interactive Gradio interface. Evaluation conducted on 52 domain-specific procedural queries.



## Project Structure

```
data/                 # PDF, TEXT, REPHRASE\_TEXT, TRIPLES
knowledge\_graph/      # kg.graphml
models/               # ANITA/, mistral/
pipelines/            # preprocessing.py
src/                  # scraping/, processing/, utils/, ui/
EmPuAssinstant\_\*.py   # LLM-based assistant launchers
requirements.txt
```


## Quickstart

```
pip install -r requirements.txt
python src/utils/download_model.py --model anita
python pipelines/preprocessing.py
python EmPuAssinstant_ANITA.py      # or EmPuAssinstant_mistral.py
```

Then open your browser to access the Gradio interface.


## Key Libraries

* `llama-cpp-python`, `transformers`, `torch`, `sentence-transformers`
* `spacy`, `nltk`, `PyMuPDF`, `networkx`, `gradio`
* `requests`, `beautifulsoup4`, `tiktoken`, `huggingface_hub`

---

## RAG QA Results

| Model            | Accuracy | Completeness | Hallucinations | Language   |
| ---------------- | -------- | ------------ | -------------- | ---------- |
| LLaMAntino-ANITA | High     | High         | None           | Italian ✔️ |
| Mistral-7B       | Medium   | Partial      | Some           | Mixed ❌    |

* ANITA outperformed ReBEL and spaCy for RDF triple generation due to its Italian-language specialization.


## Notes

* Includes a DevContainer for out-of-the-box setup.
* The assistant is optimized for Italian legal and procedural content.


## Future Work

* Integration of semantic vector retrievers (e.g., FAISS)
* Automatic Knowledge Graph updating
* Multi-turn memory and dialogue support


