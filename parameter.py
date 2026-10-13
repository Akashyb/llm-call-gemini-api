from google import genai

client = genai.Client()

response = client.interactions.create(
    model="gemini-3.5-flash",
    input="Name any 3 titles for book",
    generation_config = {
        "temperature":1.0,
        "max_output_tokens":3000
    }
)

print(response.output_text)