import os
import csv
import re
import logging
from llama_cpp import Llama
from tqdm import tqdm
import tiktoken
from src.utils.config import Config
from src.utils.logging_config import setup_logging


def count_tokens(text: str) -> int:
    return len(tiktoken.get_encoding("cl100k_base").encode(text))


def clean_text(text: str) -> str:
    """Remove headers like 'Riformulato testo:' or similar."""
    return re.sub(r"(Riformulazione del testo:|Riformulato testo:)", "", text, flags=re.IGNORECASE).strip()


def split_into_blocks(sentences, max_tokens=Config.MAX_TOKENS):
    blocks = []
    buffer = []
    token_count = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        tokens = count_tokens(sentence)
        if token_count + tokens <= max_tokens:
            buffer.append(sentence)
            token_count += tokens
        else:
            blocks.append(" ".join(buffer))
            buffer = [sentence]
            token_count = tokens

    if buffer:
        blocks.append(" ".join(buffer))

    return blocks


def extract_triples_block(llm, text_block: str) -> str:
    prompt = f"""### Istruzione:
Estrai tutte le triple RDF dal seguente testo. Ogni tripla deve essere nel formato (soggetto, relazione, oggetto).
Ignora completamente qualsiasi frase o riferimento a figure, incluse espressioni come "figura", "vedi figura", "come mostrato nella figura", "figura X".
Non includere triple che derivano da descrizioni, titoli o riferimenti visivi non testuali.

Testo:
{text_block}

### Risposta:"""

    response = llm(prompt, max_tokens=2000, stop=["###"])
    return response["choices"][0]["text"].strip()



def parse_triples(raw_output: str):
    pattern = r"\(([^,]+),\s*([^,]+),\s*([^)]+)\)"
    matches = re.findall(pattern, raw_output)
    triples = []
    for subj, rel, obj in matches:
        triples.append((subj.strip(), rel.strip(), obj.strip()))
    return triples

def extract_all_triples():
    setup_logging()
    logger = logging.getLogger("TripleExtractor")

    logger.info("Initializing LLaMAntino model...")
    llm = Llama(
        model_path=Config.MODEL_PATH,
        chat_format="chatml",
        n_threads=Config.N_THREADS,
        n_ctx=Config.N_CTX,
        n_gpu_layers=Config.N_GPU_LAYERS,
    )

    os.makedirs(Config.TRIPLE_DIR, exist_ok=True)

    logger.info("Scanning input folder for text files...")
    for filename in os.listdir(Config.REPHRASE_DIR):
        if not filename.endswith(".txt"):
            continue

        input_path = os.path.join(Config.REPHRASE_DIR, filename)
        output_path = os.path.join(Config.TRIPLE_DIR, filename.replace(".txt", ".csv"))

        if os.path.exists(output_path):
            logger.info(f"Triples file already exists: {output_path}, skipping.")
            continue
        
        with open(input_path, "r", encoding=Config.ENCODING) as f:
            raw_text = clean_text(f.read())
            sentences = re.split(r'(?<=[.!?])\s+', raw_text)
            blocks = split_into_blocks(sentences)

        all_triples = []

        for block in tqdm(blocks, desc=f" {filename}", leave=False):
            raw_response = extract_triples_block(llm, block)
            triples = parse_triples(raw_response)
            all_triples.extend(triples)

        logger.info(f"Writing {len(all_triples)} triples to {output_path}")
        with open(output_path, "w", newline="", encoding=Config.ENCODING) as f_out:
            writer = csv.writer(f_out)
            writer.writerow(["soggetto", "relazione", "oggetto"])
            writer.writerows(all_triples)

    logger.info("Triple extraction completed.")


if __name__ == "__main__":
    extract_all_triples()