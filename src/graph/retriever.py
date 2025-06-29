import re
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words("italian"))

def clean_and_tokenize(text):
    words = re.findall(r"\w+", text.lower())
    return [w for w in words if w not in STOPWORDS]

def find_relevant_triples(graph, query: str, top_k=20) -> list:
    """
    Ritorna le triple più rilevanti rispetto alla query, ordinate per punteggio.
    """
    keywords = clean_and_tokenize(query)
    scored_triples = []

    for u, v, data in graph.edges(data=True):
        rel = data.get('label', '').lower()
        score = 0

        for kw in keywords:
            if kw in u.lower():
                score += 2  
            if kw in v.lower():
                score += 2  
            if kw in rel:
                score += 1  

        if score > 0:
            scored_triples.append(((u, rel, v), score))

    scored_triples.sort(key=lambda x: x[1], reverse=True)
    return [triple for triple, _ in scored_triples[:top_k]]
