from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


print(api_key)


client = OpenAI(api_key=str(api_key))


#Chain of Thought: The model is encouraged to break down its reasoning process step by step before arriving at an answer
SYSTEM_PROMPT = """
    You are an helpful AI assistant who is specialized in resolving user query.
    For the given user input, analyse the input and break down the problem step by step.

    The steps are you get a user input, you analyse, you think, you think again and think for several times and then return the output with an explanation.

    Follow the steps in sequence that is "analyse", "think", "output","validate" and finally "result".

    Rules:
    1. Follow the strict JSON output as per schema.
    2. Always perform one step at a time and wait for the next input.
    3. Carefully analyse the user query.

    Output Format:
    {{"step":"string", "content":"string"}}


    Example:
    Input: What is 2 + 2
    Output: {{"step": "analyse", "content":"Alright! The user is interested in math query and he is asking  a basic arithmetic operation"}}
    Output: {{"step": "think", "content":"To perform this addition, I must go from left to right and add all the operands"}}
    Output: {{"step": "output", "content":"4"}}
    Output: {{"step": "validate", "content":"Seems like 4 is a correct ans for 2 + 2"}}
    Output: {{"step": "result", "content":"2 + 2 = 4 and this is calculated by adding all the numbers"}}
    
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    response_format={"type":"json_object"},
    messages=[
        {"role":"system", "content":SYSTEM_PROMPT},
        {"role":"user", "content":"what is 5/2 *3 to the power 4"},
        {"role":"assistant", "content":json.dumps({"step": "analyse", "content": "The user is asking for the evaluation of the arithmetic expression 5/2 * 3 to the power 4. This involves division, multiplication, and exponentiation."})},
        {"role":"assistant", "content":json.dumps({"step": "think", "content": "To solve 5/2 * 3^4, I need to perform the exponentiation first, then the division and multiplication in order from left to right."})},
        {"role":"assistant", "content":json.dumps({"step": "think", "content": "Calculate 3 to the power 4: 3^4 = 3*3*3*3 = 81. Then, multiply 5/2 by 81: (5/2) * 81 = 5 * 81 / 2 = 405 / 2 = 202.5."})},
        {"role":"assistant", "content":json.dumps({"step": "output", "content": "The value of 5/2 * 3^4 is 202.5."})},
        {"role":"assistant", "content":json.dumps({"step": "validate", "content": "Rechecking calculations: 3^4 = 81, 5/2 = 2.5, 2.5 * 81 = 202.5. The calculation is correct."})},
    ]
)

print(response.choices[0].message.content)