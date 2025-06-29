from huggingface_hub import hf_hub_download
import logging
from src.utils.config import Config
from src.utils.logging_config import setup_logging

def download_model():
    setup_logging()
    logger = logging.getLogger("ModelDownloader")

    logger.info("Starting model download...")
    downloaded_path = hf_hub_download(
        repo_id=Config.REPO_ID,
        filename=Config.FILENAME,
        local_dir=Config.LOCAL_DIR,
        local_dir_use_symlinks=False
    )

    logger.info(f"File downloaded: {downloaded_path}")

    try:
        with open(downloaded_path, "rb") as f:
            magic = f.read(4)
        if magic == Config.EXPECTED_MAGIC:
            logger.info("File is a valid GGUF compatible with llama-cpp")
        else:
            logger.error(f"Invalid file: magic={magic} (expected: {Config.EXPECTED_MAGIC})")
    except Exception as e:
        logger.exception(f"Error reading file: {e}")


