import logging
from src.utils.logging_config import setup_logging
from src.graph.graph_loader import load_graph
from src.graph.retriever import find_relevant_triples
from src.llm.llm_interface import load_llm, ask_llm
from src.utils.config import Config

setup_logging()
logger = logging.getLogger(__name__)

def main():
    logger.info("Loading Knowledge Graph...")
    graph = load_graph(Config.KNOWLEDGE_GRAPH_PATH)
    llm = load_llm()

    while True:
        user_query = input("\nEnter your question (or type 'exit' to quit): ")
        if user_query.lower() in ("exit", "esci", "quit"):
            break

        triples = find_relevant_triples(graph, user_query)
        if not triples:
            print("No relevant information found in the knowledge graph.")
            continue

        answer = ask_llm(llm, user_query, triples)
        print(f"\nAnswer: {answer.strip()}")

if __name__ == "__main__":
    main()
