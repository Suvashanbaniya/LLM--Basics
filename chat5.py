import requests,json
url = "http://localhost:11434/api/generate"

with open('datafamily.txt','r') as f :
    knowledge = f.read()
    
messages = [{
    'role':'system','content':'sarcastic bot'
    
}] 
name = input("Enter your name: ")   
lines = knowledge.split("\n")
while True:
    user = input(f"{name}:")
    if user.lower() == 'exit':
        break
    
    messages.append({'role':'user','content':user})
    messages = messages[-10:]
    
    words = user.lower().split()
    scored_lines = []
    match_lines =[ ]
    for line in lines:
        score = 0
        for word in words:
            
            if word in line.lower():
              score += 1
        if score > 0 :
            scored_lines.append((score,line))     
    scored_lines.sort(reverse=True)
    
    top_lines = [line for score, line in scored_lines[:]]
    
    if top_lines:
        context ="\n".join(top_lines)
               
    
    else:
        context = "Answer using Your general knowledge"
        
    prompt =f"Context:\n{context}\n\nConversation:\n"   
    
    for msg in messages:
        prompt += f"{msg['role']}: {msg['content']}\n"
        
        
    response = requests.post(url,json={
        "model":'llama3',
        'temperature':1.0,
        'stream':True,
        'prompt':prompt
    },stream=True)
    
    print("AI:",end="",flush= True)
    
    ai_reply = ""
    
    
    try:
     for line in response.iter_lines():
        if line:
            chunk = json.loads(line.decode('utf-8'))
            token = chunk.get("response","")
            print(token,end="",flush=True)
            ai_reply += token
     print()    
        
     messages.append({'role':'assistant','content':ai_reply})
        
    except Exception as e :
        print("There is error in the code ",e)                  
        
        
    