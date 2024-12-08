from openai import OpenAI
import os

# Set your OpenAI API Key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Specify the model
MODEL = "gpt-4o-mini"

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ],
    temperature=0,
    max_tokens=100
)

print(response)
print(response.choices[0].message.content)