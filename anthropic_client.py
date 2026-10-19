import os

import anthropic
from anthropic.types import Message, MessageParam
from dotenv import load_dotenv

from enums.model import Model

load_dotenv()


class AnthropicClient(anthropic.Anthropic):
    def __init__(self) -> None:
        super().__init__(api_key=os.getenv("API_KEY"))

    def run_inference(self, messages: list[MessageParam]) -> Message:
        return self.messages.create(
            model=Model.HAIKU,
            max_tokens=1000,
            messages=messages,
        )
