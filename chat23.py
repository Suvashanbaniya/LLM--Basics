import requests 
import json 

url = "http://localhost:11434/api/generate"

messages = [
    {"role":"system","content":"You are a sarcastic AI assistant."}
    
]
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break 
    messages.append({"role":"user","content":user_input})
    messages =messages[-10:]
    
    
    prompt=" "
    for msg in messages:
        prompt += f"{msg['role']}: {msg['content']}\n"
        
    response = requests.post(url,json= {
            "model":"llama3",
            "temperature":1.0,
            "stream":True,
            "prompt":prompt,
            
            
        },stream=True)
        
    print("AI:" ,end=" ",flush=True)
    ai_reply = " "
    try :
        for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode("utf-8"))
                    token = chunk.get("response","")
                    
                    print(token,end="",flush=True)
                    ai_reply += token
        print()
        
        messages.append({"role":"assistant","content":ai_reply})
        
    except Exception as e :
        print("Error:",e)                
        