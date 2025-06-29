import os
import logging
import fitz  
import tqdm
from src.utils.config import Config
from src.utils.logging_config import setup_logging

def extract_text_from_pdf():
    setup_logging()
    logger = logging.getLogger("PDFTextExtractor")

    logger.info("Ensuring output directory exists...")
    os.makedirs(Config.TEXT_DIR, exist_ok=True)

    logger.info(f"Scanning PDF directory: {Config.PDF_DIR}")
    for pdf_file in tqdm.tqdm(os.listdir(Config.PDF_DIR), desc="Extracting text"):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(Config.PDF_DIR, pdf_file)
            txt_filename = pdf_file.replace(".pdf", ".txt")
            txt_path = os.path.join(Config.TEXT_DIR, txt_filename)
            
            if os.path.exists(txt_path):
                logger.info(f"TXT file already exists: {txt_path}, skipping.")
                continue
            
            logger.info(f"Extracting from: {pdf_file}")
            try:
                with fitz.open(pdf_path) as doc:
                    text = ""
                    for page in doc:
                        text += page.get_text()

                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(text)

                logger.info(f"Saved text to: {txt_path}")
            except Exception as e:
                logger.exception(f"Failed to extract text from {pdf_file}: {e}")

if __name__ == "__main__":
    extract_text_from_pdf()