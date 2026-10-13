from ollama import chat

response=chat(
    model="gemma3.1b",
    messages=[{
        "role":"user",
        "content":"explain ML in simape words"
    }]
)

print(response.message.content)