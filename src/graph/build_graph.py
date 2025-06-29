import csv
import networkx as nx
from pathlib import Path
from tqdm import tqdm
import logging
from src.utils.config import Config
from src.utils.logging_config import setup_logging  

setup_logging()
logger = logging.getLogger(__name__)

def load_all_triples(folder_path: Path) -> nx.MultiDiGraph:
    """
    Loads all triples from all CSV files in the specified folder
    and builds a directed graph with the triples.
    """
    graph = nx.MultiDiGraph()
    csv_files = list(folder_path.glob("*.csv"))
    if not csv_files:
        logger.warning(f"No CSV files found in {folder_path}.")

    for csv_file in tqdm(csv_files, desc="CSV Processing"):
        logger.info(f"Triple loading from {csv_file.name}")
        with open(csv_file, newline='', encoding=Config.ENCODING) as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) != 3:
                    continue
                subj, rel, obj = [cell.strip() for cell in row]
                graph.add_node(subj, label="entity")
                graph.add_node(obj, label="entity")
                graph.add_edge(subj, obj, label=rel)
    
    return graph

