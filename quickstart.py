from typing import cast

from anthropic.types import MessageParam, TextBlock
from rich.console import Console
from rich.markdown import Markdown

from anthropic_client import AnthropicClient

client = AnthropicClient()

console = Console()
messages: list[MessageParam] = []

system_prompt = console.input("[bold yellow]system (leave blank for no):[/] ")
user_input = console.input("[bold cyan]user:[/] ")
while True:
    messages.append(MessageParam(role="user", content=user_input))

    response = client.run_inference(messages)

    response_message = cast(TextBlock, response.content[0]).text
    messages.append(MessageParam(role="assistant", content=response_message))
    console.print("[bold green]assistant: [/]", end="")
    label = "assistant: "
    console.print(Markdown(response_message), width=console.width - len(label))
    console.print()

    # print_json(response.model_dump_json(indent=2, exclude_none=True))
