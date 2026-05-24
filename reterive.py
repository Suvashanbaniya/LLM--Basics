#5/24/
import requests,json 
from sklearn.metrics.pairwise import cosine_similarity

embed_url = "http://localhost:11434/api/embeddings"


def get_embeddings(text):
    response = requests.post(embed_url,json={
        "model":"nomic-embed-text",
        "prompt":text
    })
    
    data = response.json()
    
    return data  ['embedding']

with open('datafamily.txt','r')as f :
    knowledge = f.read().split("\n")
    
knowledge_embeddings= []

for item in knowledge :
    if item.strip():
        emb = get_embeddings(item)
        knowledge_embeddings.append(emb)
        
print("Knowledge Loading")


name = input("Enter your name :")

while True :
    user = input(f'{name}: ')
    if user.lower() == 'exit':
        break;
    
    query_embedding = get_embeddings(user)
    similarities = []
    
    
for i in range (len(knowledge_embeddings)):
        score = cosine_similarity
        ([query_embedding],
         [knowledge_embeddings[i]])[0][0]
        
        
        similarities.append((score,knowledge[i]))
        
similarities.sort(reverse=True)
top_contexts = similarities[:3]
        
context = "\n".join([item[1]
                            for item in top_contexts])
print("\n \t Reterival score \t")
        
for score,text in top_contexts:
            print(f"\nContext:{text}")
            
            print(f"Similarities:{round(score,2)}")
            
            print("\n---------------------")
            
            prompt = """
            You are sarcastic AI 
            Use reterived Knowledge below.
            Context:
            {context}
            User :
            {user}
           
            """
            
local ="http://localhost:11434/api/generate",

response = requests.post(local,json={
            "model":"llama3",
            "temperature":4.0,
            "stream":True,
            "prompt":prompt,
        },stream=True)
        
print("AI:",end="",flush=True)
        
ai_reply = ""
        
for line in response.iter_lines(): 
            if line :
                chunk = json.loads(line.decode("utf-8"))
                token =chunk.get("response","")
                print(token,end="",flush=True)
                ai_reply += token
                print()
            messages.append({'role':'assistant','content':ai_reply})