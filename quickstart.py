from rich import print_json
from enums.model import Model
from anthropic.types import MessageParam
from typing import cast
from anthropic.types import TextBlock
from anthropic_client import AnthropicClient


client = AnthropicClient()

messages: list[MessageParam] = []
messages.append(MessageParam(role='user', content="what is the answer to life, the universe and everything"))

response = client.messages.create(
    model=Model.HAIKU,
    max_tokens=1000,
    messages=messages,
)

response_message = cast(TextBlock, response.content[0]).text

messages.extend([
  MessageParam(role='assistant', content=response_message),
  MessageParam(role='user', content="thanks for that"),
])


response = client.messages.create(
    model=Model.HAIKU,
    max_tokens=1000,
    messages=messages,
)

print_json(response.model_dump_json(indent=2, exclude_none=True))
