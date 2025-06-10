from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")



openai_client = OpenAI(api_key=openai_api_key)
gemini_client = OpenAI(api_key=gemini_api_key,base_url="https://generativelanguage.googleapis.com/v1beta/openai/") 




#Chain of Thought: The model is encouraged to break down its reasoning process step by step before arriving at an answer
SYSTEM_PROMPT = """
    You are an helpfull AI assistant who is specialized in resolving user query.
    For the given user input, analyse the input and break down the problem step by step.

    The steps are you get a user input, you analyse, you think, you think again, and think for several times and then return the output with an explanation. 

    Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".

    Rules:
    1. Follow the strict JSON output as per schema.
    2. Always perform one step at a time and wait for the next input.
    3. Carefully analyse the user query,

    Output Format:
    {{ "step": "string", "content": "string" }}

    Example:
    Input: What is 2 + 2
    Output: {{ "step": "analyse", "content": "Alight! The user is interest in maths query and he is asking a basic arthematic operation" }}
    Output: {{ "step": "think", "content": "To perform this addition, I must go from left to right and add all the operands." }}
    Output: {{ "step": "output", "content": "4" }}
    Output: {{ "step": "validate", "content": "Seems like 4 is correct ans for 2 + 2" }}
    Output: {{ "step": "result", "content": "2 + 2 = 4 and this is calculated by adding all numbers" }}

    Example:
    Input: What is 2 + 2 * 5 / 3
    Output: {{ "step": "analyse", "content": "Alight! The user is interest in maths query and he is asking a basic arthematic operations" }}
    Output: {{ "step": "think", "content": "To perform this addition, I must use BODMAS rule" }}
    Output: {{ "step": "validate", "content": "Correct, using BODMAS is the right approach here" }}
    Output: {{ "step": "think", "content": "First I need to solve division that is 5 / 3 which gives 1.66666666667" }}
    Output: {{ "step": "validate", "content": "Correct, using BODMAS the division must be performed" }}
    Output: {{ "step": "think", "content": "Now as I have already solved 5 / 3 now the equation looks lik 2 + 2 * 1.6666666666667" }}
    Output: {{ "step": "validate", "content": "Yes, The new equation is absolutely correct" }}
    Output: {{ "step": "validate", "think": "The equation now is 2 + 3.33333333333" }}
    and so on.....

"""
# openai 
def initialize_openai_client(messages):
    response = openai_client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type":"json_object"},
        messages=messages
    )
    return response

# gemini sdk
def initialize_gemini_client(validation_prompt):
    response = gemini_client.chat.completions.create(
        model="gemini-2.0-flash-001",
        response_format={"type":"json_object"},
        messages=[
        {"role": "system", "content": "You are a validation expert. Review the provided content for logical correctness and provide a concise validation. Do not generate JSON."},
        {"role": "user", "content": validation_prompt}
    ]
    )
    return response

openai_messages = [
        {"role":"system", "content":SYSTEM_PROMPT},
    ]

query = input(">  ")
openai_messages.append({ "role": "user", "content": query })

while True:
    openai_response = initialize_openai_client(openai_messages)
    
    openai_messages.append({"role":"assistant", "content":openai_response.choices[0].message.content})
    openai_parsed_response = json.loads(openai_response.choices[0].message.content)

    if (openai_parsed_response.get("step")=="validate"):
        print("------------------GEMINI USED------------------------")
        
        validation_prompt = f"Given the user's original query: '{query}' and the current step in the thought process: '{openai_parsed_response.get('content')}', please validate if this step is logically correct. Provide a short, concise validation or suggest an improvement. Your response should just be the validation text."
        print("          🧠:", openai_parsed_response.get("content"))
        gemini_response = initialize_gemini_client(validation_prompt)
        openai_messages.append({"role":"assistant", "content":gemini_response.choices[0].message.content})
        
        continue

    if (openai_parsed_response.get("step")!="result"):
        print("          🧠:", openai_parsed_response.get("content"))
        continue

    print("🤖:", openai_parsed_response.get("content"))
    break