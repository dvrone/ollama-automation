from ollama import chat

# resp = chat(model="qwen2.5:0.5b", messages=[{"role": "user", "content": "Hello!"}])

# # run the `ollama serve` command via a second terminal
# print(resp.message.content)


messages: list = [{"role": "user", "content": "Where is the capital of France?"}]
stream = chat(model="qwen2.5:0.5b", messages=messages, stream=True)
for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)
print("\n")