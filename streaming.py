from google import genai

client = genai.Client()

stream = client.interactions.create(
    model="gemini-3.5-flash",
    input="Explain ChatGPT in 10 paragraghs.",
    stream=True
)

for event in stream:
    if event.event_type=="step.delta":
        if event.delta.type=="text":
            print(event.delta.text,end="",flush=True)