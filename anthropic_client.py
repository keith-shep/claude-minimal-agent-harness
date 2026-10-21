import os
from collections.abc import Callable

import anthropic
from anthropic.lib.tools import BetaFunctionTool
from anthropic.types.beta import BetaMessage, BetaMessageParam

from effort import Effort
from enums.model import Model
from modules.tty_logger import TtyLog, tty_logger


class AnthropicClient(anthropic.Anthropic):
    def __init__(self, log: TtyLog | None = None) -> None:
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        super().__init__()
        self.log = log or tty_logger()

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
