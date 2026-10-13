
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()

st.set_page_config(
    page_title="AI Recipe Generator",
    page_icon="🍲",
    layout="centered"
)

st.title("🍲 AI Recipe Generator")
st.write("Generate a recipe using the ingredients available in your kitchen.")

# Initialize Gemini client
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)


# Function to generate a recipe
def generate_recipe(ingredients, cuisine, diet):
    """
    Generate a recipe using the provided ingredients.
    Cuisine: Italian, Mexican, Indian, Any, etc.
    Diet: Vegan, Vegetarian, Jain, Any, etc.
    """

    prompt = f"""
    Generate one food recipe using these ingredients in simple english.:
    {', '.join(ingredients)}

    Requirements:
    - Keep the recipe within 100 words.
    - Cuisine: {cuisine}
    - Diet: {diet}
    - Include a recipe name.
    - Include brief preparation instructions.
    - Use the provided ingredients as the main ingredients.
    - Respect the selected dietary preference.
    """

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt
    )

    return response.text


# User inputs
st.subheader("🥕 Enter Your Ingredients")

ingredients_input = st.text_input(
    "Ingredients",
    placeholder="e.g., rice, tomato, onion, potato"
)

cuisine = st.selectbox(
    "Select Cuisine",
    ["Any", "Indian", "Italian", "Mexican", "Chinese", "Japanese"]
)

diet = st.selectbox(
    "Select Diet",
    ["Any", "Vegetarian", "Vegan", "Jain", "Non-Vegetarian"]
)

# Generate button
if st.button("Generate Recipe", type="primary"):
    if not ingredients_input.strip():
        st.warning("Please enter at least one ingredient.")
    else:
        ingredients = [
            item.strip()
            for item in ingredients_input.split(",")
            if item.strip()
        ]

        try:
            with st.spinner("Preparing your recipe... 🍳"):
                recipe = generate_recipe(
                    ingredients,
                    cuisine,
                    diet
                )

            st.subheader("🍽️ Your Recipe")
            st.markdown(recipe)

        except Exception as e:
            st.error(f"Unable to generate recipe: {e}")
