import requests
import json 

url = "http://localhost:11434/api/generate"

# 🔥 Default system + temperature
system_prompt = "You are a very sarcastic AI bot."
temperature = 1.0

messages = [{
    "role": "system",
    "content": system_prompt
}]

name = input("Enter your name: ")

while True:
    
    user = input(f"{name}: ")
    
    if user.lower() == "exit":
        break

    # 🔥 Mode control (temperature + personality)
    if user.lower() == "mode sarcastic":
        temperature = 1.0
        system_prompt = "You are a sarcastic AI bot."
        messages[0] = {"role": "system", "content": system_prompt}
        print("Mode changed to sarcastic")
        continue
    
    elif user.lower() == "mode formal":
        temperature = 0.2
        system_prompt = "You are a formal assistant."
        messages[0] = {"role": "system", "content": system_prompt}
        print("Mode changed to formal")
        continue
    
    elif user.lower() == "mode coder":
        temperature = 0.5
        system_prompt = "You are a coding assistant."
        messages[0] = {"role": "system", "content": system_prompt}
        print("Mode changed to coder")
        continue

    # 🔥 Save user message (FIXED role)
    messages.append({"role": "user", "content": user})
    messages = messages[-10:]  

    # 🔥 Build prompt (inside loop)
    prompt = ""
    for msg in messages:
        prompt += f"{msg['role']}: {msg['content']}\n"

    # 🔥 API call (use dynamic temperature)
    response = requests.post(url, json={
        "model": "llama3",
        "temperature": temperature,
        "prompt": prompt,
        "stream": True
    }, stream=True)

    print("AI:", end="", flush=True)

    ai_reply = ""

    try:
        # 🔥 Correct streaming loop
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line.decode("utf-8"))
                token = chunk.get("response", "")
                print(token, end="", flush=True)
                ai_reply += token

        print()

        # 🔥 Save AI response
        messages.append({"role": "assistant", "content": ai_reply})

    except Exception as e:
        print("Error:", e)