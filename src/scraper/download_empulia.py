import os
import logging
import requests
import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from src.utils.config import Config
from src.utils.logging_config import setup_logging

def pdfs_already_downloaded() -> bool:
    """Check if there are already PDF files in the download directory."""
    if not os.path.exists(Config.PDF_DIR):
        return False
    return any(fname.endswith(".pdf") for fname in os.listdir(Config.PDF_DIR))

def download_pdf_from_page():
    setup_logging()
    logger = logging.getLogger("EmpuliaScraper")

    logger.info("Checking existing PDF files...")
    if pdfs_already_downloaded():
        logger.info(f"PDFs already present in '{Config.PDF_DIR}', skipping download.")
        return

    logger.info("Sending request to Empulia page...")
    try:
        response = requests.get(Config.BASE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
    except requests.RequestException as e:
        logger.exception(f"Failed to fetch the page: {e}")
        return

    logger.info("Looking for PDF links...")
    link_pdf = soup.find_all("a", href=True)

    for link in tqdm.tqdm(link_pdf, desc="Downloading PDFs"):
        href = link["href"]
        if href.endswith(".pdf"):
            url_pdf = urljoin(Config.BASE_URL, href)
            file_name = href.split("/")[-1]
            file_path = os.path.join(Config.PDF_DIR, file_name)

            if not os.path.exists(file_path):
                logger.info(f"Downloading: {file_name}")
                try:
                    pdf_data = requests.get(url_pdf)
                    pdf_data.raise_for_status()
                    with open(file_path, "wb") as f:
                        f.write(pdf_data.content)
                except requests.RequestException as e:
                    logger.error(f"Failed to download {url_pdf}: {e}")
            else:
                logger.info(f"{file_name} already exists. Skipping.")

if __name__ == "__main__":
    download_pdf_from_page()
