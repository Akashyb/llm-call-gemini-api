import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Store instructions only once
conversation = [
    {
        "role": "user",
        "parts": [{
            "text": """
            You are a friendly movie recommendation assistant.

            Recommend 3 to 5 movies based on user preferences.
            Include the title, year, genre, a short spoiler-free
            description, and why the user might enjoy each movie.
            Consider language, mood, genre, actors, and favorite movies.
            Use simple English and avoid inventing movie details.
            """
        }]
    },
    {
        "role": "model",
        "parts": [{
            "text": "Understood. I will act as a movie recommendation assistant."
        }]
    }
]


def recommend_movies(user_message):
    conversation.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=conversation
        )

        reply = response.text or "No recommendations generated."

        conversation.append({
            "role": "model",
            "parts": [{"text": reply}]
        })

        return reply

    except Exception as e:
        conversation.pop()
        return f"Error: {e}"

# Main chatbot loop
print("=" * 45)
print("       MOVIE RECOMMENDATION CHATBOT")
print("=" * 45)
print("Tell me your movie preferences!")
print("Examples:")
print("- Recommend Telugu thriller movies")
print("- Suggest movies similar to Interstellar")
print("- Recommend feel-good comedy movies")
print("\nType 'exit' to quit.")
print("Type 'clear' to clear conversation history.")


while True:
    user_message = input("\nYou: ").strip()

    if user_message.lower() == "exit":
        break

    if user_message.lower() == "clear":
        # Preserve the initial instructions
        del conversation[2:]
        print("Conversation cleared.")
        continue

    if user_message:
        print("\nChatbot:", recommend_movies(user_message))