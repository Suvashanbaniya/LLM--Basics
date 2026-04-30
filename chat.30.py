import requests
import json 

url = "http://localhost:11434/api/generate"

messages = [{
    'role':'system','content':'this is a sarcastic bot'
}]

with open('data.txt','r') as f :
     knowledge = f.read()
    
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    
    messages.append({'role':'user','content':user_input})   
    
    messages = messages[-10:]
    
    if user_input.lower() in knowledge.lower():
        context = knowledge
        
    else:
        context = "No relevant information found"
        
    prompt = f"""
Context:
{context}
    
Conversation:
"""         
    
    
    
    for msg in messages:
        prompt += f"{msg['role']} :{msg['content']}\n"
        
    response = requests.post(url,json={
        
        'model':'llama3',
        'temperature':1.0,
        'stream':True,
        'prompt':prompt},stream=True) 
    
    print("AI:",end="",flush=True)
    ai_reply = "" 
    try :
     for line  in response.iter_lines():
        if line:
            chunk = json.loads(line.decode("utf-8"))
            token = chunk.get('response',"") 
            print(token,end="",flush=True)
            ai_reply += token
            
     print()        
            
     messages.append({'role':'ai_assistant','content':ai_reply})    
            
    except:
        print("This is the error")       
            
            
        