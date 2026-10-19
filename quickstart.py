from anthropic.types import MessageParam
from rich.console import Console
from rich.markdown import Markdown

from anthropic_client import AnthropicClient

console = Console()
system_prompt = console.input("[bold yellow]system (leave blank for no):[/] ")
client = AnthropicClient()


messages: list[MessageParam] = []

while True:
    user_input = console.input("[bold cyan]user:[/] ")
    messages.append(MessageParam(role="user", content=user_input))

    response = client.run_inference(messages, system_prompt)

    response_message = "".join(
        block.text for block in response.content if block.type == "text"
    )
    messages.append(MessageParam(role="assistant", content=response_message))
    console.print("[bold green]assistant: [/]", end="")
    label = "assistant: "
    console.print(Markdown(response_message), width=console.width - len(label))
    console.print()

    # print_json(response.model_dump_json(indent=2, exclude_none=True))
