import anthropic
import os
from dotenv import load_dotenv

load_dotenv() 

client = anthropic.Anthropic(api_key=os.getenv("API_KEY"))

message = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "hello world",
        }
    ],
)

print(message.model_dump_json(indent=2, exclude_none=True))

for block in message.content:
    if block.type == "text":
        print(block.text)