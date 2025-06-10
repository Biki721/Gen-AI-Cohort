from google import genai

client = genai.Client(api_key="AIzaSyCX71EPCiIl7l4xSPOxNcl-mGwwfddscxA")

response = client.models.generate_content(
    model="gemini-2.0-flash-001", contents="Why is the sky blue"
)

print(response.text)