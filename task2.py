import requests
import json
from sklearn.metrics.pairwise import cosine_similarity

embed_url = "http://localhost:11434/api/embeddings"
llm_url = "http://localhost:11434/api/generate"

temperature = 0.3


def get_embedding(text):
    response = requests.post(
        embed_url,
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    data = response.json()
    return data["embedding"]


with open("datafamily.txt", "r") as f:
    knowledge = f.read()


chunk_size = 2

lines = knowledge.split("\n")

chunks = []

for i in range(0, len(lines), chunk_size):
    chunk = "\n".join(lines[i:i + chunk_size])

    if chunk.strip():
        chunks.append(chunk)

print("Chunks created:", len(chunks))


chunk_embeddings = []

for chunk in chunks:
    emb = get_embedding(chunk)
    chunk_embeddings.append(emb)

print("Chunk embeddings ready")


messages = []

name = input("Enter your name: ")

while True:

    user = input(f"{name}: ")

    if user.lower() == "exit":
        print("Leaving chat...")
        break

    query_embedding = get_embedding(user)

    similarities = []

    for i in range(len(chunk_embeddings)):

        score = cosine_similarity(
            [query_embedding],
            [chunk_embeddings[i]]
        )[0][0]

        similarities.append(
            (score, chunks[i])
        )

    similarities.sort(reverse=True)

    top_chunks = similarities[:3]

    context = "\n".join(
        [item[1] for item in top_chunks]
    )

    print("\n---- Retrieved Chunks ----")

    for score, text in top_chunks:
        print("\nChunk:")
        print(text)
        print("Similarity:", round(score, 2))

    prompt = f"""
You are a helpful AI.

Use retrieved context.

Context:
{context}

User Question:
{user}

Answer naturally.
"""

    response = requests.post(
        llm_url,
        json={
            "model": "llama3",
            "temperature": temperature,
            "stream": True,
            "prompt": prompt
        },
        stream=True
    )

    print("\nAI:", end="", flush=True)

    ai_reply = ""

    for line in response.iter_lines():

        if line:

            chunk = json.loads(
                line.decode("utf-8")
            )

            token = chunk.get(
                "response",
                ""
            )

            print(
                token,
                end="",
                flush=True
            )

            ai_reply += token

    print()

    messages.append(
        {
            "role": "user",
            "content": user
        }
    )

    messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )