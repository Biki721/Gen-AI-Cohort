from dotenv import load_dotenv,find_dotenv
from openai import OpenAI
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


print(api_key)


client = OpenAI(api_key=str(api_key))

text = "dog chases cat"
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=text
)

print(response)
