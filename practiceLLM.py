import json
import requests

# LLM endpoint
url = "http://localhost:11434/api/generate"

# system prompt + memory
messages = ["This is a multi-personality chatbot (sarcastic, coder, formal)."]

while True:
    user_input = input("Which type of chatbot or message? ")

    if user_input.lower() == "exit":
        break

    # Add user input properly
    messages.append(f"You: {user_input}")

    # Keep only last 10 messages (FIXED)
    messages = messages[-10:]

    # Convert list -> prompt string
    conversation = "\n".join(messages)

    # Default system behavior
    system_instruction = "You are a helpful AI assistant."

    # Choose persona
    if user_input.lower() == "sarcastic":
        system_instruction = "You are a sarcastic, witty AI assistant."
        temperature = 1.0

    elif user_input.lower() == "coder":
        system_instruction = "You are an expert Python coding assistant."
        temperature = 0.1

    elif user_input.lower() == "formal":
        system_instruction = "You are a formal and professional assistant."
        temperature = 0.2

    else:
        temperature = 0.7

    # Final prompt = system + conversation
    final_prompt = system_instruction + "\n" + conversation

    response = requests.post(url, json={
        "model": "llama3",
        "prompt": final_prompt,
        "temperature": temperature,
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

        # store AI response AFTER completion
        messages.append(f"AI: {ai_reply}")

    except Exception as e:
        print("Error:", e)