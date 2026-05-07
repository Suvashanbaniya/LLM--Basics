#march7 


import requests,json
url = "http://localhost:11434/api/generate"

with open('datafamily.txt','r') as f :
    knowledge = f.read()
temperature = 1.0
system_prompt = "You are a sarcastic AI bot."
messages = [{
    'role':'system','content':system_prompt
}]
name = input("What is your name :")
lines = knowledge.split("\n")
while True:
    user = input(f"{name}") 
    if user.lower() =='exit':
        break
    
    if user.lower() == 'sad':
        temperature = 0.3
        system_prompt = "You are a Sad console AI bot."
        messages[0] = {"role": "system", "content": system_prompt}
        print("Now the AI bot will console you ")
        continue
    
    
    elif user.lower() == 'calm':
        temperature = 0.2
        system_prompt = "You are a calm and precide AI bot."
        messages[0] = {"role": "system", "content": system_prompt}
        print("Now this bot will chat you will clamly wiht you ")
        continue
    
    
    elif user.lower() == 'learning':
        temperature = 0.3
        system_prompt = "You are a learning and curious AI bot."
        messages[0] = {"role": "system", "content": system_prompt}
        print("Now the AI bot will help you to learn  you ")
        continue
    
    
    elif user.lower() == 'sad':
        temperature = 0.3
        system_prompt = "You are a Sad console AI bot."
        messages[0] = {"role": "system", "content": system_prompt}
        print("Now the AI bot will console you ")
        continue
    
    elif user.lower() == "history":
        print("\n ---Chat History ---")
        for msg in messages:
            if msg['role'] != 'system':
                print(f"{msg['role']}: {msg['content']}")
    
        print("-----------------\n")
        continue  
    
    elif user.lower() == 'clear':
        messages = [messages[0]]
        print(messages)
        
    elif user.lower() =='help':
        print("How can I  assist you senor ?"
              "We have different modes :")
        print(" 1. sad\n 2.calm\n 3.learning\n 4.sarcastic\n")
        
        
    
    messages.append({'role':'user','content':user})
    messages =[messages[0]] + messages[-8:]
    
    words = user.lower().split()
    
    scored_lines = []
    for line in lines:
        score = 0 
        for word in words:
            if word in line.lower():
                score += 1
        if score> 0 :
            scored_lines.append((score,line))
            
    scored_lines.sort(reverse=True)
    
    top_lines = [line for score , line in scored_lines[:3]]
    
    if top_lines :
        context = "\n".join(top_lines)
        
    else:
        context = "Answer using  your general knowledge"
        
    prompt = f"""
    Context:
    {context}
    
    Conversation :
    """
    
    for msg in messages:
        prompt += f"{msg['role']}:{msg['content']}\n"
         
    response = requests.post(url,json={
        "model":'llama3',
        "temperature":temperature,
        "stream":True,
        "prompt":prompt
    },stream=True)
    
    print("AI: ",end="",flush = True)
    
    ai_reply = ""
    try :
        for data_lines in response.iter_lines():
            chunk = json.loads(data_lines.decode('utf-8'))  
            token = chunk.get("response","")
            print(token,end = "",flush = True)
            ai_reply += token
            
        print() 
        
        messages.append({'role':'assistant','content':ai_reply})
        
    except Exception as e :
        print('Error',e)                                 
      
    