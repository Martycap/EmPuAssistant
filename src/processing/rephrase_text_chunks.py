import os
import logging
from tqdm import tqdm
import tiktoken
from llama_cpp import Llama
from src.utils.config import Config
from src.utils.logging_config import setup_logging

def count_tokens(text: str) -> int:
    """Count tokens using ChatML-compatible tokenizer."""
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def split_text(text: str, max_tokens: int) -> list:
    """Split text into chunks that fit within the token limit."""
    words = text.split()
    chunks, current = [], []
    current_token_len = 0

    for word in words:
        word_token_len = count_tokens(word + " ")
        if current_token_len + word_token_len > max_tokens:
            chunks.append(" ".join(current))
            current = [word]
            current_token_len = word_token_len
        else:
            current.append(word)
            current_token_len += word_token_len

    if current:
        chunks.append(" ".join(current))
    return chunks

def rephrase_chunk(chunk: str, llm) -> str:
    """Send a prompt to LLaMantino to rephrase a chunk."""
    prompt = f"""### Istruzione:
Riformula il seguente testo rendendolo più chiaro, leggibile e coeso. Evita ripetizioni.

Testo:
\"\"\"{chunk}\"\"\"

### Risposta:"""

    response = llm.create_chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.3,
        stop=["###"],
    )
    return response["choices"][0]["message"]["content"].strip()

def rephrase_all_texts():
    setup_logging()
    logger = logging.getLogger("TextRephraser")

    os.makedirs(Config.REPHRASE_DIR, exist_ok=True)
    logger.info(f"Scanning directory: {Config.TEXT_DIR}")

    logger.info("Initializing LLaMantino model...")
    llm = Llama(
        model_path=str(Config.MODEL_PATH),
        chat_format="chatml",
        n_ctx=Config.N_CTX,
        n_threads=Config.N_THREADS,
        n_gpu_layers=Config.N_GPU_LAYERS,
    )

    for filename in os.listdir(Config.TEXT_DIR):
        if filename.endswith(".txt"):
            logger.info(f"Processing file: {filename}")
            input_path = os.path.join(Config.TEXT_DIR, filename)
            output_path = os.path.join(Config.REPHRASE_DIR, filename)

            if os.path.exists(output_path):
                logger.info(f"Rephrased file already exists: {output_path}, skipping.")
                continue 
            
            with open(input_path, "r", encoding="utf-8") as f:
                text = f.read()

            chunks = split_text(text, Config.MAX_TOKENS)
            rephrased = []
            for chunk in tqdm(chunks, desc=f"Rephrasing {filename}"):
                rephrased_text = rephrase_chunk(chunk, llm)
                rephrased.append(rephrased_text)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n\n".join(rephrased))
            logger.info(f"Saved rephrased text to: {output_path}")

if __name__ == "__main__":
    rephrase_all_texts()