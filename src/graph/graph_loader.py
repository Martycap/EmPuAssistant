import networkx as nx
from pathlib import Path

def load_graph(graph_path: Path) -> nx.MultiDiGraph:
    return nx.read_graphml(graph_path)
