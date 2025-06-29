import gradio as gr
from gradio.themes.base import Base
from llama_cpp import Llama
from src.graph.graph_loader import load_graph
from src.graph.retriever import find_relevant_triples
from src.utils.config import Config



# Carica il grafo e il modello
graph = load_graph(Config.KNOWLEDGE_GRAPH_PATH)

llm = Llama(
    model_path=Config.MISTRAL_PATH,
    n_ctx=2048,
    n_threads=8,
    n_gpu_layers=0,
    chat_format="chatml"
)

def build_prompt(user_query, triples):
    triples_str = "\n".join([f"- {s} — {r} — {o}" for s, r, o in triples])
    return (
        f"Domanda: {user_query}\n"
        f"Knowledge Graph:\n{triples_str}\n\n"
        f"Rispondi in italiano in modo chiaro e sintetico, come se parlassi a un utente inesperto."
    )

def chat_with_empuassistant(message, history):
    triples = find_relevant_triples(graph, message)
    if not triples:
        return "Mi dispiace, non ho trovato informazioni utili nel grafo per rispondere alla tua domanda."
    prompt = build_prompt(message, triples)
    response = llm.create_chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.3
    )
    return response["choices"][0]["message"]["content"].strip()


dark_blue_theme = Base(
    primary_hue="blue",
    neutral_hue="slate",
    font=["Inter", "sans-serif"],
).set(
    body_background_fill="#0D1B2A",
    body_text_color="#FFFFFF",
    input_background_fill="#1B263B",
    input_border_color="#415A77",
    block_background_fill="#1B263B",
    block_title_text_color="#E0E1DD",
    border_color_primary="#778DA9",
)

chat_interface = gr.ChatInterface(
    fn=chat_with_empuassistant,
    title="🌐 EmPuAssistant",
    description="EmPuAssistant è un assistente intelligente in grado di rispondere a domande in linguaggio naturale sulla documentazione tecnica della piattaforma EmPULIA.",
    examples=[
        "Come si accede alla nuova piattaforma?",
        "Cosa serve per partecipare a una manifestazione di interesse?",
        "Che differenza c’è tra gara aperta e gara ristretta?"
    ],
    theme=dark_blue_theme,
)

if __name__ == "__main__":
    chat_interface.launch()
