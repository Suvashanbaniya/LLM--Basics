import requests,json

from sklearn.metrics.pairwise import cosine_similarity

llm_url = "http://localhost:11434/api/generate"
embed_url = "http://localhost:11434/api/embeddings"

temperature = 0.5

def get_embedding(text):
    response = requests.post(embed_url,json={
        "model":"nomic=embed-text",
        "prompt":text,
    })
    
    data = response.json()
    return data ['embedding']
def load_data():
    try:
        with open('family_data.json','r') as f:
            return json.load(f)
        
    except FileNotFoundError:
        return{}
    
    def save_data ():
        with open("family_data.json",'w') as f:
            json.dump(data,f,indent=2)
family_data = load_data()            
    
knowledge_embedding = []
for item in family_data:
    if item.strip(): 
        emb = get_embedding(item) 
        knowledge_embedding.append(item)  
        
print("Knowledge Ready")   


messages = [{
    'role':'system',
    'context':'helpful bot',
}]     
    
name = input("Enter the name :")

while True :
    user = input(f"{name} :")
    
    if user.lower()== 'exit':
        break
        
    found = False
    answer = None
    
    for key , value in family_data.items():
        if key.lower() in user.lower():
            answer = value
            found = True
            break
    if found :
        print("AI:",answer)
    else:
        print("AI: I dont have answer to the question")
        print("AI: Please provide it so I can remember it .")
        
        new_info = input("Enter info you want to add : ")
        
        parts = new_info.split()
        
        if len(parts) >=3 :
            key = parts[0]
            name = parts[1]
            age = parts[2]
            
            
            family_data[key] = {
                "name":name,
                "age":age
            }     
            save_data(family_data)
            print("AI: The information that you gave is saved into the database")   
        
    if user.lower() == 'info':
        print("This is the LLM project created by suvashan Baniya \n")
        print("This chatbot will show you the data of your family member as you store the data into the database"\
            "The current available information available right is just some random text")
        continue
        
    
    
    {json.dumps(family_data, indent=2)}
    
    
    data = {
        'model':'llama3',
        'prompt':prompt,
        'stream':False,
    }
    
    response = requests.post(embed_url,json=data)
    result  = response.json()
    print("\nAI:", result["response"])
    
    history = ""
    for msg in messages:
        history += (
            f"{msg['role']}:"
            f"{msg['context']}:\n"
        )


prompt = f"""
    You are a  Family assistant AI.
    Answer only using the family data 
    
    Conversation history:
    {history}
    
    Current User Question
    {user}
    
    Answer naturally
    
    

"""        

response = requests.post(llm_url,json={
    'model':'llama3',
    'prompt':prompt,
    'stream':True,
    
},flush=True)

print("AI:",end="",flush=True)

ai_reply = ""

try :
    for line in response.iter_lines():
        if line :
            chunk = line.decode('utf-8')
            data = json.loads(chunk)
            token = data.get("response",(""))
            
            print(token,end="",flush=True)
            ai_reply += token
            
    print()
    messages.append({
        'role':'user',
        'system':user
    })
except Exception as e :
    print("Error",e )    