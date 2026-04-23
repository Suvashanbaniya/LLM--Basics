import requests
import json

url = "http://localhost:11434/api/generate"

# Default settings
temperature = 0.7
system_prompt = "You are a helpful AI assistant."

# Message memory
messages = [
    {"role": "system", "content": system_prompt}
]

while True:
    user_input = input("You: ")

    # EXIT
    if user_input.lower() == "exit":
        break

    # ---------------- COMMANDS ---------------- #

    # CLEAR MEMORY
    if user_input.lower() == "/clear":
        messages = [{"role": "system", "content": system_prompt}]
        print("Memory cleared.")
        continue

    # SHOW HISTORY
    if user_input.lower() == "/history":
        print("\n--- Chat History ---")
        for msg in messages:
            print(f"{msg['role']}: {msg['content']}")
        print("--------------------\n")
        continue

    # HELP
    if user_input.lower() == "/help":
        print("""
Available commands:
/clear      → Clear memory
/history    → Show conversation
/persona X  → Change personality (sarcastic, coder, formal)
/temp X     → Set temperature (e.g. /temp 0.2)
/exit       → Quit
""")
        continue

    # CHANGE PERSONA
    if user_input.startswith("/persona"):
        try:
            persona = user_input.split(" ")[1].lower()

            if persona == "sarcastic":
                system_prompt = "You are a sarcastic, witty AI assistant."
            elif persona == "coder":
                system_prompt = "You are an expert Python programmer."
            elif persona == "formal":
                system_prompt = "You are a formal and professional assistant."
            else:
                print("Unknown persona.")
                continue

            # Reset memory when persona changes
            messages = [{"role": "system", "content": system_prompt}]
            print(f"Switched to {persona} mode.")
            continue

        except:
            print("Usage: /persona [sarcastic|coder|formal]")
            continue

    # CHANGE TEMPERATURE
    if user_input.startswith("/temp"):
        try:
            temperature = float(user_input.split(" ")[1])
            print(f"Temperature set to {temperature}")
        except:
            print("Usage: /temp 0.5")
        continue

    # ---------------- CHAT ---------------- #

    # Add user message
    messages.append({"role": "user", "content": user_input})

    # Limit memory
    messages = messages[-10:]

    # Build prompt
    prompt = ""
    for msg in messages:
        prompt += f"{msg['role']}: {msg['content']}\n"

    # API call
    response = requests.post(
        url,
        json={
            "model": "llama3",
            "temperature": temperature,
            "stream": True,
            "prompt": prompt
        },
        stream=True
    )

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

        # Save AI response
        messages.append({"role": "assistant", "content": ai_reply})

    except Exception as e:
        print("Error:", e)