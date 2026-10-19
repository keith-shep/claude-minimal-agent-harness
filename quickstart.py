import anthropic
import os
from dotenv import load_dotenv
from rich import print_json
from enums.role import Role
from enums.model import Model
from anthropic.types import MessageParam

load_dotenv() 

client = anthropic.Anthropic(api_key=os.getenv("API_KEY"))

messages: list[MessageParam] = [
    {
        "role": 'user',
        "content": "what is the answer to life, the universe and everything",
    }
]

response = client.messages.create(
    model=Model.HAIKU,
    max_tokens=1000,
    messages=messages,
)

response_message = response.content[0].text

messages.extend([{"role":'assistant', "content":response_message}, {"role": 'user', "content": "thanks for that"}])


response = client.messages.create(
    model=Model.HAIKU,
    max_tokens=1000,
    messages=messages,
)

print_json(response.model_dump_json(indent=2, exclude_none=True))
