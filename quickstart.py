import anthropic
import os
from dotenv import load_dotenv
from rich import print_json
from enums.role import Role

load_dotenv() 

client = anthropic.Anthropic(api_key=os.getenv("API_KEY"))

message = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=1000,
    messages=[
        {
            "role": Role.USER,
            "content": "what is the answer to life, the universe and everything",
        }
    ],
)

print_json(message.model_dump_json(indent=2, exclude_none=True))

# for block in message.content:
#     if block.type == "text":
#         print(block.text)