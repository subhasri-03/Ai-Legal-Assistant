# chatbot.py
import os
from openai import OpenAI  # Updated import

# Initialize client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def legal_chat(prompt: str) -> str:
    try:
        response = client.chat.completions.create(  # Updated method chain
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content  # Updated response access
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

