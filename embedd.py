# learning the embedding of the text data  march 10/ 2026

import requests
import json
url = "http://localhost:11434/api/embeddings"
text = "happy person"

respones = requests.post(
    url,
    json ={
        "model":"nomic-embed-text",
        "prompt":text
    }
)

data = respones.json()
embedding = data["embedding"]

print("Frist 10 embedding numbers:\n")
    
print(embedding[:10])