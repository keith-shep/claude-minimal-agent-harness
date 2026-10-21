import os
from collections.abc import Callable

import anthropic
from anthropic.lib.tools import BetaFunctionTool
from anthropic.types.beta import BetaMessage, BetaMessageParam
from rich.console import Console

from effort import Effort
from enums.model import Model


class AnthropicClient(anthropic.Anthropic):
    def __init__(self, requests_ttys: str = "", response_ttys: str = "") -> None:
        super().__init__(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.requests_ttys: str = requests_ttys
        self.responses_ttys: str = response_ttys

    def run_inference(
        self,
        messages: list[BetaMessageParam],
        system_prompt: str = "",
        effort_level: Effort = "medium",
        tools: list[BetaFunctionTool[Callable[..., str]]] | None = None,
    ) -> BetaMessage:

        runner = self.beta.messages.tool_runner(
            model=Model.HAIKU,
            max_tokens=1000,
            messages=messages,
            system=system_prompt,
            output_config={"effort": effort_level},
            tools=tools or [],
        )
        response = runner.until_done()
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
