 

import requests 
import json

url = "http://localhost:11434/api/generate"


with open("data.txt", "r") as f :
    context = f.read()
    
    
messages = [{"role":"system","content":"You are a personal assistant"}]
name = input("Enter your name :")
while True:
    user = input(f"{name}:")
    if user.lower() =="exit":
        break
    #  Mode control (temperature + personality)
    if user.lower() == "mode sarcastic":
        temperature = 1.0
        system_prompt = "You are a sarcastic AI bot."
        messages[0] = {"role": "system", "content": system_prompt}
        print("Mode changed to sarcastic")
        continue
    
    elif user.lower() == "mode formal":
        temperature = 0.2
        system_prompt = "You are a formal assistant."
        messages[0] = {"role": "system", "content": system_prompt}
        print("Mode changed to formal")
        continue
    
    elif user.lower() == "mode coder":
        temperature = 0.5
        system_prompt = "You are a coding assistant."
        messages[0] = {"role": "system", "content": system_prompt}
        print("Mode changed to coder")
        continue

    messages.append({'role':"user","content":user})
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
    
