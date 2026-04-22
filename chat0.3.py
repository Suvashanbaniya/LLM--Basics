import json
import requests

url = "http://localhost:11434/api/generate"

messages = ["You are a sarcastic AI assistant"]

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    # Add user message
    messages.append(f"You: {user_input}")

    # Keep last 10 messages
    messages = messages[-10:]

    # Convert to prompt
    conversation = "\n".join(messages)

    # Send request
    response = requests.post(url, json={
        "model": "llama3",
        "prompt": conversation,
        "temperature": 1.0,
        "stream": True
    }, stream=True)

    print("AI:", end=" ", flush=True)

    ai_reply = ""

    try:
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line.decode("utf-8"))
                token = chunk.get("response", "")

                print(token, end="", flush=True)
                ai_reply += token

        print()

        # Add AI reply AFTER full response
        messages.append(f"AI: {ai_reply}")

    except Exception as e:
        print("Error:", e)