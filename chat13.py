#wrote on 13 march 
import requests ,json
from sklearn.metrics.pairwise import cosine_similarity
url = "http://localhost:11434/api/embeddings"

def get_embedding(text):
    response = requests.post(url,json={
        "model":"nomic-embed-text",
        "prompt":text
    })
    return response.json()["embedding"]


with open('datapk.txt','r') as f :
    knowledge = f.read().split('\n')
    
knowledge_embeddings = []

for item in knowledge:
    if item.strip() :
        knowledge_embeddings.append(get_embedding(item))
     
    
print("Semantic Search Engine Ready ")

while True :
    query = input("Ask Something :")
    if query.lower() == "exit":
        break 
    query_emb = get_embedding(query)
    similarities = []
    
    for i in range(len(knowledge)):
        sim = cosine_similarity(
            [query_emb],
            [knowledge_embeddings[i]]
        )[0][0]
        
        similarities.append((sim,knowledge[i]))
        
        
        
    similarities.sort(reverse=True)
        
    best_match = similarities[0]
    print("Best Match :") 
    print(best_match[1])
    print("score:",best_match[0])
    print("\n============\n")      