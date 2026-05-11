import requests
from sklearn.metrics.pairwise import cosine_similarity

url = "http://localhost:11434/api/embeddings"


def get_embedding(text):
    response = requests.post(
        url,
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )
    return response.json()["embedding"]


name = input("Enter your name: ")

print("\nType how you feel (any sentence). Example: I am excited\n")

# Precompute embeddings ONCE
excited_emb = get_embedding("excited person")
curious_emb = get_embedding("curious person")
sad_emb = get_embedding("sad person")


while True:
    user = input("How are you feeling today? : ")

    if user.lower() == "exit":
        print("Goodbye!")
        break

    user_emb = get_embedding(user)

    sim_excited = cosine_similarity([user_emb], [excited_emb])[0][0]
    sim_curious = cosine_similarity([user_emb], [curious_emb])[0][0]
    sim_sad = cosine_similarity([user_emb], [sad_emb])[0][0]

    if sim_excited > sim_curious and sim_excited > sim_sad:
        print(f"{name}, you seem excited 😊")

    elif sim_curious > sim_sad:
        print(f"{name}, you seem curious 🤔")

    else:
        print(f"{name}, you seem sad 😔")