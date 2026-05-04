import requests,json
url = "http://localhost:11434/api/generate"

messages= [
    {'role':'system','content':'This is a sarcasic bot '},
]

name = input("Enter your name ")
with open ('data.txt','r') as f :
    knowledge = f.read()
    
lines = knowledge.split("\n")

while True:
    user =input(f"{name} :")
    if user.lower() == "exit":
        break
    
    messages.append({'role':'user','content':user})
    messages = messages[-10:]
    
    
    words = user.lower().split()
    
    match_lines = []
    for line in lines:
        for word in words:
            if word in line.lower():
                match_lines.append(line)
                break
            
    if match_lines:
            context = "\n".join(match_lines)
    else:
            context = "Answer using your general knowledge"
            
    prompt = f"Context:\n{context}\n\nConversation:\n"
        
    for msg in messages:
            prompt +=f"{msg['role']}: {msg['content']}\n"
            
            response = requests.post(url,json={
            "model":"llama3",
            "prompt":prompt,
            "temperature":0.7,
            "stream":True,
        },stream=True)
        
    print("AI: ",end="",flush=True)
    ai_reply = ""
        
    try:
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode("utf-8"))
                    token = chunk.get("response","")
                    print(token,end="",flush=True)
                    ai_reply += token
            print()
                    
            messages.append({'role':'assistant','content':ai_reply})
                    
                    
                    
    except Exception as e :
            print("Error: ",e)
    
    