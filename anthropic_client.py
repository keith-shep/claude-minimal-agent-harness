import os

import anthropic
from anthropic.types import Message, MessageParam
from dotenv import load_dotenv
from rich.console import Console

from enums.model import Model

load_dotenv()


class AnthropicClient(anthropic.Anthropic):
    def __init__(self) -> None:
        super().__init__(api_key=os.getenv("API_KEY"))

    def run_inference(
        self,
        messages: list[MessageParam],
        system_prompt: str = "",
        requests_ttys: str = "",
        responses_ttys: str = "",
    ) -> Message:

        response = self.messages.create(
            model=Model.HAIKU,
            max_tokens=1000,
            messages=messages,
            system=system_prompt,
        )
        if requests_ttys:
            with open(requests_ttys, "w") as tty:
                console = Console(file=tty, force_terminal=True)
                console.rule("request")
                console.print_json(
                    data={"system": system_prompt, "messages": messages}, default=str
                )

        if responses_ttys:
            with open(responses_ttys, "w") as tty:
                console = Console(file=tty, force_terminal=True)
                console.rule("response")
                console.print_json(response.model_dump_json(exclude_none=True))

        return response
