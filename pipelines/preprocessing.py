import os
import logging
from pathlib import Path
import networkx as nx
from src.graph.build_graph import load_all_triples
from src.processing.extract_text import extract_text_from_pdf
from src.processing.extract_triples_from_text import extract_all_triples
from src.processing.rephrase_text_chunks import rephrase_all_texts
from src.scraper.download_empulia import download_pdf_from_page
from src.utils.config import Config
from src.utils.logging_config import setup_logging
from src.utils.download_model import download_model

def model_exists() -> bool:
    """
    Checks if a GGUF model already exists in the model directory.
    """
    if not os.path.exists(Config.LOCAL_MODEL_ANITA):
        return False
    return any(fname.endswith(".gguf") for fname in os.listdir(Config.LOCAL_MODEL_ANITA))

def is_file_processed(pdf_filename: str, stage: str) -> bool:
    """
    Check if a file from PDF_DIR has already been processed in the given stage.
    
    stage: one of ['text', 'rephrase', 'triple']
    """
    name = Path(pdf_filename).stem
    if stage == "text":
        return (Config.TEXT_DIR / f"{name}.txt").exists()
    elif stage == "rephrase":
        return (Config.REPHRASE_DIR / f"{name}.txt").exists()
    elif stage == "triple":
        return (Config.TRIPLE_DIR / f"{name}.csv").exists()
    else:
        raise ValueError(f"Unknown stage: {stage}")

def main():
    setup_logging()
    logger = logging.getLogger("MainPipeline")

    logger.info("Pipeline started.")
    
    # Step 1: Download model (only if not already present)
    if model_exists():
        logger.info(f"Model already exists in '{Config.LOCAL_MODEL_ANITA}', skipping download.")
    else:
        logger.warning(f"No model found in '{Config.LOCAL_MODEL_ANITA}', initiating download...")
        download_model()
        
    # Step 2: Download PDFs
    download_pdf_from_page()

    # Step 3: Extract text (only for new PDFs)
    to_process = [
        pdf for pdf in os.listdir(Config.PDF_DIR)
        if pdf.endswith(".pdf") and not is_file_processed(pdf, "text")
    ]
    if to_process:
        logger.info(f"Extracting text from {len(to_process)} new PDF(s)...")
        extract_text_from_pdf()
    else:
        logger.info("All PDFs already have corresponding text files. Skipping text extraction.")

    # Step 4: Rephrase text (only if not already rephrased)
    to_process = [
        txt for txt in os.listdir(Config.TEXT_DIR)
        if txt.endswith(".txt") and not is_file_processed(txt, "rephrase")
    ]
    if to_process:
        logger.info(f"Rephrasing {len(to_process)} new text file(s)...")
        rephrase_all_texts()
    else:
        logger.info("All text files already rephrased. Skipping rephrasing.")

    # Step 5: Extract triples (only if not already extracted)
    to_process = [
        txt for txt in os.listdir(Config.REPHRASE_DIR)
        if txt.endswith(".rephrased.txt") and not is_file_processed(txt, "triple")
    ]
    if to_process:
        logger.info(f"Extracting triples from {len(to_process)} new file(s)...")
        extract_all_triples()
    else:
        logger.info("All rephrased texts already processed into triples. Skipping extraction.")

    # Step 6: Build Knowledge Graph
    logger.info("Starting Knowledge Graph generation...")

    triple_dir = Path(Config.TRIPLE_DIR)
    output_path = Path(Config.KNOWLEDGE_GRAPH_PATH)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    graph = load_all_triples(triple_dir)

    if graph.number_of_nodes() == 0:
        logger.warning("No nodes in the graph. Process aborted.")
        return

    for idx, (u, v, k) in enumerate(graph.edges(keys=True)):
        graph.edges[u, v, k]["id"] = str(idx)

    nx.write_graphml(graph, output_path)
    logger.info(f"Knowledge Graph saved in: {output_path.resolve()}")


    logger.info("Pipeline completed.")
    
if __name__ == "__main__":
    main()