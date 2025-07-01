import os
from datetime import datetime

def log_interaction(question, answer, log_path):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]\n")
        f.write(f"Domanda: {question}\n")
        f.write(f"Risposta: {answer}\n")
        f.write("-" * 40 + "\n")
