from pathlib import Path

class Config:
    """Central configuration of paths and model parameters."""

    # Directory paths
    BASE_URL = "http://www.empulia.it/tno-a/empulia/Empulia/SitePages/Guide%20pratiche.aspx"
    PDF_DIR = Path("data/PDF")
    TEXT_DIR = Path("data/TEXT")
    REPHRASE_DIR = Path("data/REPHRASE_TEXT")
    TRIPLE_DIR = Path("data/TRIPLES")
    KNOWLEDGE_GRAPH_PATH = Path("knowledge_graph/kg.graphml")
    LOCAL_MODEL_ANITA = Path("models/ANITA")

    # Model download & file info
    REPO_ID = "swap-uniba/LLaMAntino-3-ANITA-8B-Inst-DPO-ITA_GGUF"
    FILENAME = "LLaMAntino-3-ANITA-8B-Inst-DPO-ITA.Q4_K_M.gguf"
    MODEL_PATH = LOCAL_MODEL_ANITA / FILENAME
    EXPECTED_MAGIC = b"GGUF"
    MISTRAL_PATH = "models/mistral/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
    
    # Model runtime parameters
    N_CTX = 2048
    N_THREADS = 8
    N_GPU_LAYERS = 0
    MAX_TOKENS = 2000
    ENCODING = "utf-8"
