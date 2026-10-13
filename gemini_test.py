from dotenv import load_dotenv
load_dotenv()
from google import genai

client = genai.Client()

response = client.interactions.create(
    model="gemini-3.7-flash",
    input="Explain ChatGPT in 3 sentences."
)

print(response.output_text)

