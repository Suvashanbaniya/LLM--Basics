#created at march 10 2025
# writted without using or seeing any code online or ai 
import json,requests
url = "http://localhost:11434/api/generate"


with open('datafamily.txt','r') as f :
    knowledge = f.read()
    
messages = [
    {'role':'assistant','content':'system'}
]    
lines = knowledge.split("\n")
name = input("Insert your name :")

while True:
    user = input(f"{name}")
    if user.lower() == "exit":
        print("Ending the chat")
        break
    
    elif user.lower() == 'history':
        print("-------------HISTORY-------\n")
        for msg in messages :
            if msg['role'] != ['system']:
                print(f'{msg['role']}:{msg['content']}')
                
    elif user.lower() == "clear":
        messages = [messages[0]]
        print(messages)            
    
    messages.append({'role':'assistant','content':user})
    messages =  [messages[0]] + messages[-10]
    
    
    words = user.lower().split()
    
    scored_lines = []
    
    for line in lines :
        score = 0 
        for word in words:
                if word in line.lower():
                    score += 1
                    
                if score > 0 :
                    scored_lines.append((line,score))          
                    
        scored_lines.sort(reverse=True)
        
        
    top_lines = [line for score, line in scored_lines[:3]] 
    
    if top_lines :
        context = "\n".join(top_lines)
        
    else:
        context = "Answering using your general knowledge"
    
    
    prompt = f"""
    Context:
    {context}
    
    Conversation :
    """        
                   
    for msg in messages:
        prompt += f"{msg['role']}:{msg['content']}"
    
    response = requests.post(json,url={
        "model":'llama3',
        "temperature":1.0,
        "stream":True,
        "prompt":prompt
    },stream=True)
    print('AI:',end="",flush=True)
    ai_reply = ""
    
try :
    for data_lines in response.iter_lines():
        chunk = json.load(data_lines.decode('utf-8'))
        token = chunk.get('response("")')
        print("ai",end="",flush=True)
        ai_reply += token
        
        messages.append({'role':'assistant','content':ai_reply})
        

except Exception as e :
    print("There is a error in the code ")        