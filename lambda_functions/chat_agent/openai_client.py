import os
import openai

openai.api_key = os.environ['OPENAI_KEY']


def ask_agent(message: str, user_id: str) -> str:
    # Ejemplo de llamada simple a OpenAI completions
    response = openai.ChatCompletion.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': 'Eres un asistente que guía cuestionarios de madurez.'},
            {'role': 'user', 'content': message}
        ]
    )
    return response.choices[0].message.content.strip()