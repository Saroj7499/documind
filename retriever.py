import os
import chromadb
from groq import Groq
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from prompts import get_prompt

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")

def get_embedding(text):
    return embedding_model.encode(text).tolist()

def retrieve_and_answer(question):
    print("Embedding the question...")
    question_embedding = get_embedding(question)

    print("Searching for relevant chunks...")
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    chunks = results["documents"][0]
    context = "\n\n".join(chunks)

    print("Sending to Groq...")
    prompt = get_prompt(context, question)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": chunks
    }