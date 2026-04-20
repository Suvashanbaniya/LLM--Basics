import requests
import json 


url = "http://localhost:11434/api/generate"
conversation = "You are a chill , sarcastic and dark sense humor  AI .\n"


while True:
    user_input = input("You:")
    if user_input.lower() =="exit":
        break
    conversation+= f"You: {user_input}\n"
    response = requests.post(url, json={
        "model":"llama3",
        "prompt":conversation,
        "temperature":1.5,
        "stream":False
        
    })
    try :
        data = json.loads(response.text)
        ai_reply = data["response"]
        print("AI:",ai_reply)
        
        conversation+= f"AI: {ai_reply}\n"
    except Exception as e:
        print("Error:",e)
        print("Response:",response.text)    
    