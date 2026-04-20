import requests

url = "http://localhost:11434/api/generate"

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = requests.post(url, json={
        "model": "llama3",
        "prompt": user_input,
        "stream": False
    })

    print("AI:", response.json()["response"])