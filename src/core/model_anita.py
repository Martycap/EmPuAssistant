from llama_cpp import Llama
from src.utils.config import Config

def load_llm_anita():
    return Llama(
        model_path=Config.ANITA_PATH,
        n_ctx=Config.N_CTX,
        n_threads=Config.N_THREADS,
        n_gpu_layers=Config.N_GPU_LAYERS,
        chat_format="chatml"
    )
