from llama_cpp import Llama
from src.utils.config import Config

def load_llm_mistral():
    return Llama(
        model_path=Config.MISTRAL_PATH,
        n_ctx=Config.N_CTX,
        n_threads=Config.N_THREADS,
        n_gpu_layers=Config.N_GPU_LAYERS,
        chat_format="chatml"
    )
