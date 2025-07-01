import gradio as gr
from src.graph.graph_loader import load_graph
from src.graph.retriever import find_relevant_triples
from src.utils.config import Config
from src.core.model_mistral import load_llm_mistral
from src.core.prompt import build_prompt
from src.core.logger import log_interaction
from src.interface.theme import get_dark_blue_theme


graph = load_graph(Config.KNOWLEDGE_GRAPH_PATH)
llm = load_llm_mistral()

def chat_with_empuassistant(message, history):
    triples = find_relevant_triples(graph, message)
    if not triples:
        response_text = "Mi dispiace, non ho trovato informazioni utili nel grafo per rispondere alla tua domanda."
    else:
        prompt = build_prompt(message, triples)
        response = llm.create_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.3
        )
        response_text = response["choices"][0]["message"]["content"].strip()

    log_interaction(message, response_text, Config.MISTRAL_log)
    return response_text

chat_interface = gr.ChatInterface(
    fn=chat_with_empuassistant,
    title="🌐 EmPuAssistant",
    description="Scopri EmPuAssistant: il tuo alleato intelligente per navigare nella documentazione della piattaforma EmPULIA, con risposte rapide e chiare in linguaggio naturale.",
    examples=[
        "Come si accede alla nuova piattaforma?",
        "Cosa serve per partecipare a una manifestazione di interesse?",
        "Che differenza c’è tra gara aperta e gara ristretta?"
    ],
    theme=get_dark_blue_theme(),
)

if __name__ == "__main__":
    chat_interface.launch()
