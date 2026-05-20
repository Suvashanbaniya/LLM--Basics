import requests,json 
from sklearn.metrics.pairwise import cosine_similarity

embed_url = "http://localhost:11434/api/embeddings"

llm_url = "http://localhost:11434/api/generate"

def get_embedding(text):
    response = requests.post(
        embed_url,json={
            'model':'llama3',
            'prompt':text
        }
        
    )
    data = response.json() 
    return data['embedding']

with open ('datapk.txt','r') as f :
    knowledge = f.read()
    
knowledge_embeddings = []

for item in knowledge:
    emb = get_embedding(item)
    knowledge_embeddings.append(emb)  
    
print("\n RAG Chatbot Ready !\n")

while True :
    query = input("You:")
    if query.lower() == 'quit':
        break
    
    query_embedding = get_embedding(query)
    
# reterival search chat 

results = []

for i in range(len(knowledge)):
    score = cosine_similarity(
        [query_embedding],
        [knowledge_embeddings[i]]
    )[0][0]
    
results.append((score,knowledge[i]))

results.sort(reverse=True)

top_context = results[0][1]

prompt = f"""
You are a helpful AI 
Use the context below to answer the question 

Context:
{top_context}   

User Question:
{query}
"""


response = requests.psot(llm_url,json={
    'model':'llama3',
    'prompt':prompt,
    'stream':False
})

data = response.json()
answer = data["response"]

print("\n AI: ",answer)
print("\n---------------------")