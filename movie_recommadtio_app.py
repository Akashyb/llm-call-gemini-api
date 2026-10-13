
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Movie Recommendation Chatbot",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Movie Recommendation Chatbot")
st.caption("Discover movies based on your interests and mood!")

# Check API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found. Please check your .env file.")
    st.stop()

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Initialize conversation memory
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Function to get movie recommendations
def recommend_movies(user_message):
    conversation = st.session_state.conversation

    # Add user message to memory
    conversation.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    prompt = """
    You are a friendly movie recommendation assistant.

    Recommend movies based on the user's preferences, including
    genre, language, mood, actors, release period, and favorite movies.

    Instructions:
    - Recommend 3 to 5 suitable movies.
    - Give the movie title and release year when known.
    - Explain each recommendation in simple English.
    - Mention the genre and a short, spoiler-free description.
    - Ask a follow-up question if the user's preferences are unclear.
    - Do not invent movie details.
    - Keep the response concise and easy to read.
    """

    try:
        # Include instructions and conversation history
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

        reply = response.text or "Sorry, I could not generate recommendations."

        # Save assistant reply in conversation memory
        conversation.append({
            "role": "model",
            "parts": [{"text": reply}]
        })

        return reply

    except Exception as e:
        # Remove the failed user message
        conversation.pop()
        return f"Sorry, something went wrong: {e}"


# Display previous conversation
for message in st.session_state.conversation:
    role = "user" if message["role"] == "user" else "assistant"

    with st.chat_message(role):
        st.markdown(message["parts"][0]["text"])


# Movie preference input
user_message = st.chat_input(
    "Example: Recommend some feel-good Telugu movies..."
)

if user_message:
    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        with st.spinner("Finding movies for you... 🎥"):
            reply = recommend_movies(user_message)
            st.markdown(reply)

    st.rerun()


# Clear conversation
if st.button("Clear Chat"):
    st.session_state.conversation = []
    st.rerun()


# Optional quick suggestions
st.sidebar.header("🍿 Try these prompts")

suggestions = [
    "Recommend comedy movies",
    "Best Telugu thriller movies",
    "Movies similar to Interstellar",
    "Feel-good movies for the weekend",
    "Best science fiction movies",
    "Romantic movies with happy endings"
]

for suggestion in suggestions:
    if st.sidebar.button(suggestion, use_container_width=True):
        st.session_state.pending_prompt = suggestion
        st.rerun()

# Process sidebar suggestion
if "pending_prompt" in st.session_state:
    pending_prompt = st.session_state.pop("pending_prompt")

    with st.chat_message("user"):
        st.markdown(pending_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Finding movies for you... 🎥"):
            reply = recommend_movies(pending_prompt)
            st.markdown(reply)

    st.rerun()
