import os
import chainlit as cl
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Optional, Dict  # Corrected Dict import

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

# Initialize Gemini model
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# OAuth Callback Function
@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: Dict[str, str],  # Corrected `row_user_data` to `raw_user_data`
    default_user: cl.User,
) -> Optional[cl.User]:  # Corrected `=>` to `->`
    """
    Handle the OAuth callback from GitHub.
    Return the user object if Authentication is successful, None otherwise.
    """
    print(f"Token: {token}")  # Corrected `Toekn` typo
    print(f"User data: {raw_user_data}")

    return default_user  # Fixed indentation issue

# On Chat Start
@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])  # Initialize empty history
    await cl.Message(content="Hello! How can I help you today?").send()

# On Message Received
@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")

    # Append user message to history
    history.append({"role": "user", "content": message.content})

    # Corrected variable name
    formatted_history = [{"role": msg["role"], "parts": [{"text": msg["content"]}]} for msg in history]

    # Generate response using Gemini API
    response = model.generate_content(formatted_history)
    
    # Extract response text
    response_text = response.text if hasattr(response, "text") else ""

    # Append assistant response to history
    history.append({"role": "assistant", "content": response_text})
    cl.user_session.set("history", history)

    # Send response back to user
    await cl.Message(content=response_text).send()
