import requests 
import json

url = "http://localhost:11434/api/generate"

conversation = "You are an random chill ,sarcastic and a troller AI.\n"


while True:
    User_input = input("Your:")
    if User_input.lower() =="exit":
        break 
    conversation  += f"You:{User_input}\n"
    response = requests.post(url,json={
        "model":"llama3",
        "prompt":conversation,
        "temperature":1.0,
        "stream":True
    },stream=True)
    print("AI:",end="",flush=True)
    ai_reply = ""
    try:
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line.decode("utf-8"))
                token = chunk.get("response","")
                print(token.replace("\n",""),end="",flush=True)
                ai_reply += token
        print()
        conversation += f"AI:{ai_reply}\n"
       
    except Exception as  e : 
        print("Error:", e)
        print("Response:",response.text)
