def build_prompt(user_query, triples):
    triples_str = "\n".join([f"- {s} — {r} — {o}" for s, r, o in triples])
    return (
        f"Domanda: {user_query}\n"
        f"Knowledge Graph:\n{triples_str}\n\n"
        f"Rispondi in italiano in modo chiaro e sintetico, come se parlassi a un utente inesperto."
    )
