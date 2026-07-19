from deep_translator import GoogleTranslator
from ollama import chat

# resp = chat(model="qwen2.5:0.5b", messages=[{"role": "user", "content": "Hello!"}])

# # run the `ollama serve` command via a second terminal
# print(resp.message.content)


# messages: list = [{"role": "user", "content": "Where is the capital of France?"}]
# stream = chat(model="qwen2.5:0.5b", messages=messages, stream=True)
# for chunk in stream:
#     print(chunk["message"]["content"], end="", flush=True)
# print("\n")

messages: list = []

print("LOCAL CHAT")
print("Type 'exit' to quit.\n")

while True:
    user = input("You: ")

    if user.lower() in {"exit", "quit"}:
        break

    english_prompt = GoogleTranslator(
        source="auto",
        target="en"
    ).translate(user)

    print("English prompt:", english_prompt)

    messages.append({"role": "user", "content": english_prompt})

    print("\nAI: ", end="", flush=True)

    english_response = ""

    # stream = chat(model="qwen2.5:0.5b", messages=messages, stream=True)

    # for chunk in stream:
    #     english_response = chunk.message.content

    response = chat(model='qwen2.5:0.5b', messages=messages)
    english_response = response.message.content

    uzbek_response = GoogleTranslator(source="en", target="uz").translate(
        english_response
    )

    print(uzbek_response)

    messages.append({"role": "assistant", "content": english_response})

    print()
