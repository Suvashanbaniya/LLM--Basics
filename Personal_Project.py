
import requests,json



llm_url = "http://localhost:11434/api/generate"
embed_url = "http://localhost:11434/api/embeddings"

temperature = 0.5

def get_embedding(text):
    response = requests.post(embed_url,json={
        "model":"nomic-embed-text",
        "prompt":text,
    })
    
    data = response.json()
    return data['embedding']

def load_data():
    try:
        with open('family_data.json','r') as f:
            return json.load(f)
        
    except FileNotFoundError:
        return {}
    

# FIXED:
# Added parameter "data"
def save_data(data):
    
    with open("family_data.json",'w') as f:
        json.dump(data,f,indent=2)


family_data = load_data()            
    
knowledge_embedding = []

for item in family_data.keys():

    if item.strip(): 
        
        emb = get_embedding(item) 
        
        knowledge_embedding.append({
            "text":item,
            "embedding":emb
        })
        
print("Knowledge Ready")   


messages = [{
    'role':'system',
    'context':'helpful bot',
}]     
    

name = input("Enter the name :")


def get_intent(user):
    prompt = f"""
    You are intent classifier.
    Classify the message into :
    - casual_chat 
    -family_question
    -add_information
    
    Message:
    {user}
    Return only one word 
    
    """
    
    response = requests.post(llm_url,json={
        "model":"llama3",
        "prompt":prompt,
        "stream":False
    })
    
    result = response.json()
    return result["response"].strip().lower().replace(" ","_")

while True :
    
    
    user = input(f"{name} :")
    
    if user.lower()== 'exit':
        break
    
    intent = get_intent(user)
    print("Debug Intent:",intent)
    
    if intent =="casual_chat":
        print("AI: Hey how can we help you ?")
        continue
    
    elif intent  == "family_question":
        found = False
        for key , value in family_data.items():
            if key.lower() in user.lower():
                print("AI:",value)
                found = True
                break
        if not found :
            print("AI: Unable to recognize the family member")
        
        continue
    
    elif intent == "add_information":
       new_info = input("Enter the information you want to add :")
       parts = new_info.split()
       
       if len(parts) >= 3 :
           key = parts[0]
           person_name = parts[1]
           age = parts[2]
           
           family_data[key] = {
               "name" : person_name,
               "age" : age,
              }
           save_data(family_data)
           print("AI : Saved successfully")
           
       continue
        
    
    history = ""
    
    for msg in messages:
        
        history += (
            f"{msg['role']}:"
            f"{msg['context']}:\n"
        )


    prompt = f"""
    You are a Family assistant AI.
    
    Answer only using the family data.
    
    Family Data:
    
    {json.dumps(family_data, indent=2)}
    
    Conversation history:
    
    {history}
    
    Current User Question:
    
    {user}
    
    Answer naturally.
    """
    
    
    data = {
        'model':'llama3',
        'prompt':prompt,
        'stream':True,
    }
    
    
    # FIXED:
    # You were using embed_url instead of llm_url
    
    response = requests.post(
        llm_url,
        json=data,
        stream=True
    )
    

    print("\nAI:",end="",flush=True)
    
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

        
        # FIXED:
        # Changed system -> context
        
        messages.append({
            'role':'user',
            'context':user
        })

        messages.append({
            'role':'assistant',
            'context':ai_reply
        })

        
    except Exception as e :
        
        print("Error",e)

