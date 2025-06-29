from langchain_community.llms import LlamaCpp  

# Parametri del modello
MODEL_PATH = "models/LLaMAntino-3-ANITA-8B-Inst-DPO-ITA.Q4_K_M.gguf"
N_CTX = 2048
N_THREADS = 8
N_GPU_LAYERS = 0
MAX_TOKENS = 1500
TEMPERATURE = 0.7

def load_llm():
    return LlamaCpp(
        model_path=MODEL_PATH,
        n_ctx=N_CTX,
        n_threads=N_THREADS,
        n_gpu_layers=N_GPU_LAYERS,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE
    )

def build_prompt(user_query, triples):
    triples_str = "\n".join([f"- {s} — {r} — {o}" for s, r, o in triples])
    return (
        "Rispondi alla seguente domanda usando le triple del knowledge graph.\n\n"
        f"Domanda: {user_query}\n\n"
        "Knowledge Graph:\n"
        f"{triples_str}\n\n"
        "Risposta:"
    )

def ask_llm(llm, user_query, triples):
    prompt = build_prompt(user_query, triples)
    return llm.invoke(prompt) 
