
import openai

openai.api_key = "YOUR_API_KEY"

def legal_chat(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or your fine-tuned LLM
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]
