from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


print(api_key)

client = OpenAI(api_key=api_key)

#Zero-shot Prompting: the model is given direct question or task
SYSTEM_PROMPT = """
    You are an AI expert in Coding. You only know Python and nothing else.
    You help users in solving there python doubts only and nothing else.
    If user tried to ask something else apart from Python you can just roast them.
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role":"system", "content":SYSTEM_PROMPT},
        {"role":"user", "content":"Hey, My name is Biki"},
        {"role":"assistant", "content":"Hey Biki! How can I assist you with your Python coding today?"},
        {"role":"user", "content":"How to make a tea?"},
        {"role":"assistant", "content":"I'm here to help you with Python coding, not tea recipes! If you have any Python questions, feel free to ask!"},
        {"role":"user", "content":"How to add two numbers is Python"},

    ]
)

print(response.choices[0].message.content)