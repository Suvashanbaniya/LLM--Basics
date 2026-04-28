import requests 
import json 

url = "http://localhost:11434/api/generate"

messages=[{
    "role":"system","content":"You are a very sarcastic ai bot "
}]


while True :
    user = input("You: ")
    if user.lower() == "exit":
     break 
    

    messages.append({"role":"system","content":user})
    messages = messages[-10:]  

prompt = ""
for msg in messages:
    prompt +=f"{msg['role']}: {msg['content']}\n"
    
response = requests.post(url,json={
    "model":"llama3",
    "temperature":1.0,
    "prompt":prompt,
    "stream":True
},stream=True)




try:
    for line in requests.iter_lines():
        if line:
            chunk =json.loads(line.decode("utf-8")) 
            token  = chunk.get("response","")
            ai_response += token
            print(token,end="",flush=True)  
            ai_reply = ""
        print()
        messages.append({"role":"assistant","content":ai_reply})    
            
            
            
            
except Exception as e :
    print("Error:",e)            
            