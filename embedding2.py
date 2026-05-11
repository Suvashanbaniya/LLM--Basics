import requests
import json 
# this help to find how similar the words and its meaning are 

from sklearn.metrics.pairwise import cosine_similarity

url = "http://localhost:11434/api/embeddings"

def get_embedding(text):
    response = requests.post(
        url,
        json={
            "model":"nomic-embed-text",
            "prompt":text
        }
    )
    
    data = response.json()
    return data["embedding"]

text1 = "happy person"
text2 = " sad person "
text3 = " joyful person "

embedding1 = get_embedding(text1)
embedding2 = get_embedding(text2)
embedding3 = get_embedding(text3)

similarity_1_2 = cosine_similarity(
    [embedding1],
    [embedding2],
    
)    

similarity_1_3 = cosine_similarity(
    [embedding1],
    [embedding3],
)

print("\nSimilarity between")

print(f"'{text1}' and '{text2}'")

print(similarity_1_2)

print("\n--------------")
print("\nSimilarity between :")

print(f"'{text1}' and '{text3}'")

print(similarity_1_3)
