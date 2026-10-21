import os
from collections.abc import Callable

import anthropic
from anthropic.lib.tools import BetaFunctionTool
from anthropic.types.beta import BetaMessage, BetaMessageParam

from effort import Effort
from enums.model import Model
from modules.tty_logger import tty_logger


class AnthropicClient(anthropic.Anthropic):
    def __init__(
        self, requests_tty: str | None = None, responses_tty: str | None = None
    ) -> None:
        super().__init__(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.log = tty_logger(request=requests_tty, response=responses_tty)

    def run_inference(
        self,
        messages: list[BetaMessageParam],
        system_prompt: str = "",
        effort_level: Effort = "medium",
        tools: list[BetaFunctionTool[Callable[..., str]]] | None = None,
    ) -> BetaMessage:
        self.log(request={"system": system_prompt, "messages": messages})

        runner = self.beta.messages.tool_runner(
            model=Model.HAIKU,
            max_tokens=1000,
            messages=messages,
            system=system_prompt,
            output_config={"effort": effort_level},
            tools=tools or [],
        )
        response = runner.until_done()
        self.log(response=response)

        return response
