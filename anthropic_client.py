import os

import anthropic
from anthropic.types import Message, MessageParam
from dotenv import load_dotenv
from rich.console import Console

from effort import Effort
from enums.model import Model

load_dotenv()


class AnthropicClient(anthropic.Anthropic):
    def __init__(self, requests_ttys: str = "", response_ttys: str = "") -> None:
        super().__init__(api_key=os.getenv("API_KEY"))
        self.requests_ttys: str = requests_ttys
        self.responses_ttys: str = response_ttys

    def run_inference(
        self,
        messages: list[MessageParam],
        system_prompt: str = "",
        effort_level: Effort = "medium",
    ) -> Message:

        response = self.messages.create(
            model=Model.HAIKU,
            max_tokens=1000,
            messages=messages,
            system=system_prompt,
            output_config={"effort": effort_level},
        )
        if self.requests_ttys:
            with open(self.requests_ttys, "w") as tty:
                console = Console(file=tty, force_terminal=True)
                console.rule("request")
                console.print_json(
                    data={"system": system_prompt, "messages": messages}, default=str
                )

        if self.responses_ttys:
            with open(self.responses_ttys, "w") as tty:
                console = Console(file=tty, force_terminal=True)
                console.rule("response")
                console.print_json(response.model_dump_json(exclude_none=True))

        return response
