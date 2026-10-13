
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Streamlit page configuration
st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Gemini Chatbot")
st.caption("Chat with Gemini AI. Your conversation is remembered during this session.")

# Initialize conversation memory
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Function to generate a response
def chat(user_message):
    conversation = st.session_state.conversation

    # Add user message to conversation memory
    conversation.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=conversation
        )

        reply = response.text or "Sorry, I could not generate a response."

        # Store AI response in memory
        conversation.append({
            "role": "model",
            "parts": [{"text": reply}]
        })

        return reply

    except Exception as e:
        # Remove the failed user message so it can be retried
        conversation.pop()
        return f"Sorry, something went wrong: {e}"


# Display previous messages
for message in st.session_state.conversation:
    role = "user" if message["role"] == "user" else "assistant"

    with st.chat_message(role):
        st.markdown(message["parts"][0]["text"])


# Accept new user input
user_message = st.chat_input("Type your message here...")

if user_message:
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_message)

    # Generate and display the response
    with st.chat_message("assistant"):
        with st.spinner("Gemini is thinking..."):
            reply = chat(user_message)
            st.markdown(reply)

    # Refresh the app to display the updated conversation
    st.rerun()


# Clear conversation button
if st.button("Clear Chat"):
    st.session_state.conversation = []
    st.rerun()