import requests, json

from sklearn.metrics.pairwise import cosine_similarity

llm_url = "http://localhost:11434/api/generate"

embed_url = "http://localhost:11434/api/embeddings"

temperature = 0.5

def get_embedding(text):
    response = requests.post(
        embed_url,json={
            'model':'nomic-embed-text',
            'prompt':text,
            
        }
    )
    
    data = response.json()
    return data ['embedding']


with open('datafamily.txt','r') as f :
    knowledge = f.read().split("\n")
    
knowledge_embeddings = []
for item in knowledge :
    if item.strip():
        
        emb = get_embedding(item)
        knowledge_embeddings.append(emb)
        
        
print("Knowledge Loaded")
    
    
    #chat history 
    
    
messages = [{
    'role':'system',
    'content':' helpful bot'
}]    

name = input("Enter your name :")

while True :
    user = input(f'{name}\t:')   
    
    if user.lower() == 'exit':
        
        break ; 
    
    
    elif user.lower() == "friend":
        temperature = 0.5
        system_prompt = "You are a friendly assistant."
        messages[0] = {"role": "system", "content": system_prompt}
        print("Mode changed to formal")
        continue
    
    elif user.lower() == "teacher":
        
        temperature = 0.3
        system_prompt = "You are a formal AI bot  "
        messages[0]= {
            'role':'system','content':system_prompt
        }
        
      
    elif user.lower() == "sarcastic":
        
        temperature = 0.3
        system_prompt = "You are a sarcastic AI bot  "
        messages[0]= {
            'role':'system','content':system_prompt
        } 
        
        
      
    elif user.lower() == "clear":
        messages = [messages[0]]
        print("The history is cleared")
          
     
    elif user.lower() == "help":
        print("This is AI bot that can be chat according to the user input \n")     
        
    elif user.lower() == 'history':
        print("Chat History:")
        for msg in messages:
            print(f"{msg['role']}:{msg['content']}")
    
    elif user.lower() == 'save':
        with open ('wdata.txt','w') as f :
            for msg in messages :
                f.write(
                    f"{msg['role']}:"
                    f"{msg['content']}\n"
                )
            
            
            
                
            
        messages.append({
        'role':'user',
        'content':user

    })     
    
    messages = [messages[0]]+ messages[-10:]
    
    #this reterive the best context 
    query_embedding = get_embedding(user)
    
    similarities = []
    for i in range(len(knowledge)):
        score = cosine_similarity(
            [query_embedding],
            [knowledge_embeddings[i]]
            
        )[0][0]
        
        
        similarities.append((score,knowledge[i]))
        
    similarities.sort(reverse=True)
        
    top_context = similarities[0][1]
        
    history = ""
    for msg in messages:
            history += (
                f"{msg['role']}:"
                f"{msg['content']}:\n"
            )
            
    prompt = f"""
        You are helpful AI .f
        Context:
        {top_context}
        
        Conversation history :
        {history}
        
        Current User Question :
        {user}
        
        Answer naturally .
        """
        
        
    response = requests.post(llm_url,json={
            'model':'llama3',
            'prompt':prompt,
            'stream':True,
            'temperature':temperature,
        },stream=True)
        
        
        
    print("AI:",end="",flush=True)
        
    ai_reply = ""
        
    try :
            for line in response.iter_lines():
                if line :
                    chunk = line.decode('utf-8')
                    data = json.loads(chunk)
                    token = data.get("response","")
                    
                    print(token,end="",flush=True)
                    
                    ai_reply += token 
                    
            print()
                
            messages.append({
                    'role':'assistant',
                    'content':ai_reply,
                })    
                
                
    except Exception as e :
            print('Error',e)