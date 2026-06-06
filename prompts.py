def get_prompt(context, question):
    return f"""You are a helpful assistant. Answer the user's question based ONLY on the context provided below.
If the answer is not in the context, say "I don't know based on the provided document."
Do not make up any information.

Context:
{context}

Question:
{question}

Answer:"""