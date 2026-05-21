import requests,json
from sklearn.metrics.pairwise import cosine_similarity


llm_url = "http://localhost:11434/api/generate"

embed_url = "http://localhost:11434/api/embeddings"

def get_embedding(text):
    response = requests.post(
        embed_url,
        json={
            "model": 'nomic-embed-text',
            "prompt": text
        }
    )

    data = response.json()
    return data['embedding']

with open('data.txt','r') as f :
    knowledge = f.read().split('\n')
    
knowledge_embeddings = []
for item in knowledge :
    if item.strip():
        emb = get_embedding(item)  
        knowledge_embeddings.append(emb)  
print("Knowledge loading")


messages = [{
    'role':'system',
    'content':'you are an sarcastic bot '
}]  


name = input("Enter your name")
print("\n Chatbot Ready ")


while True :
    user = input(f'{name}')
    
    if user.lower() == 'exit':
        break 
    
    messages.append({
        'role':'user',
        'content':user
    })
    
    
    messages = messages[-10:]
    
    
    query_embedding = get_embedding(user)
    
    similarities = []
    
    for i in range(len(knowledge_embeddings)):
        score = cosine_similarity(
            [query_embedding],
            [knowledge_embeddings[i]]
        )[0][0]
        
        similarities.append(
            (score,knowledge[i])
        )
    similarities.sort(reverse=True)  
    top_context = similarities[0][1]
    
    
    history = ""
    
    for msg in messages:
        history += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        ) 
        
        
    prompt = f"""
You are an Sarcastic AI 
Context:
{top_context}

Conversation History :
{history}

Current User Question :
{user}

Answer naturally
"""

    response = requests.post(
        llm_url,json={
            "model":"llama3",
            "prompt":prompt,
            "stream":True
        },
        stream=True
    )   
    
    print("AI:",end='',flush=True)
    ai_reply = ''
    
    
    
    try : 
        for line in response.iter_lines():
            if line :
                chunk = line.decode('utf-8')
                data= json.loads(chunk)
                
                token = data.get(
                    "response",""
                )
                print(token,end='',flush=True)
                
                ai_reply += token
                
                
        print()
            
            
        messages.append({
                'role':'assistant',
                'content':ai_reply
            })    
            
    except Exception as e :
        print("Error",e )    