from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


print(api_key)


client = OpenAI(api_key=str(api_key))
#Few-shot Prompting: The model is provided with a few examples before asking it to generate a response
SYSTEM_PROMPT = """
    You are an AI expert in Coding. You only know Python and nothing else.
    You help users in solving there python doubts only and nothing else.
    If user tried to ask something else apart from Python you can just roast them.

    Examples: 
    User: How to make a Tea?
    Assistant: What makes you think I am a chef you piece of crap.

    Examples:
    User: How to write a function in python
    Assistant: def fn_name(x: int) -> int:
                    pass #logic of the function
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role":"system", "content":SYSTEM_PROMPT},
        {"role":"user", "content":"Hey, My name is Biki"},
        {"role":"assistant", "content":"Hey Biki! How can I assist you with your Python coding today?"},
        {"role":"user", "content":r"Why 75% attendance is important for colleges"},
    ]
)

print(response.choices[0].message.content)