
import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Conversation memory
conversation = []

# Movie recommendation function
def recommend_movies(user_message):
    # Add user message to memory
    conversation.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    prompt = """
    You are a friendly movie recommendation assistant.

    Recommend 3 to 5 movies based on the user's preferences.

    For each movie, provide:
    - Movie title and release year
    - Genre
    - Short description without spoilers
    - Why the user might enjoy it

    Consider the user's preferred language, genre, mood,
    favorite actors, and favorite movies.

    Use simple English and avoid inventing movie details.
    """

    try:
        # Send prompt and conversation history to Gemini
        contents = [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ] + conversation

        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=contents
        )

        reply = response.text or "Sorry, no recommendations generated."

        # Save assistant response in memory
        conversation.append({
            "role": "model",
            "parts": [{"text": reply}]
        })

        return reply

    except Exception as e:
        # Remove failed user message
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

    if not user_message:
        print("Please enter your preferences.")
        continue

    if user_message.lower() == "exit":
        print("Chatbot: Goodbye! Enjoy your movies!")
        break

    if user_message.lower() == "clear":
        conversation.clear()
        print("Chatbot: Conversation history cleared.")
        continue

    print("\nChatbot: Finding recommendations...\n")

    reply = recommend_movies(user_message)
    print(reply)
