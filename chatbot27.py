# this is my frist mini RAG chatbot it is very basic and have my my some personal data 

import requests 
import json

url = "http://localhost:11434/api/generate"


with open("data.txt", "r") as f :
    context = f.read()
    
    
messages = [{"role":"system","content":"You are a personal assistant"}]

while True:
    user_input = input("You: ")
    if user_input.lower() =="exit":
        break
    
    messages.append({'role':"user","content":user_input})
    messages = [messages[0]] +messages[-10:]
    prompt = f"""
Context:
{context}  

Converation:
"""  
    for msg in messages:
        prompt += f"{msg['role']} :{msg['content']}\n"
    
    response = requests.post(url, json={
        "model":"llama3",
        "prompt":prompt,
        "temperature":1.0,
        "stream":True
    },stream=True)
    
    print("AI:", end="",flush=True)
    ai_reply = ""
    
    
    try:
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
    
