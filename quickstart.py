import argparse

from anthropic.types.beta import BetaMessageParam
from rich.console import Console
from rich.markdown import Markdown

from anthropic_client import AnthropicClient
from tools.registry import TOOLS

parser = argparse.ArgumentParser()
parser.add_argument(
    "--requests-tty", help="terminal device for debug output, e.g. /dev/ttys008"
)
parser.add_argument(
    "--responses-tty", help="terminal device for debug output, e.g. /dev/ttys009"
)
args = parser.parse_args()

client = AnthropicClient(args.requests_tty, args.responses_tty)

console = Console()
console.print()
console.print("[green]Setting up...")
console.print("[green]Press Ctrl+C to end")
try:
    system_prompt = console.input("[bold yellow]system prompt (enter for none):[/] ")

    messages: list[BetaMessageParam] = []

    while True:
        user_input = console.input("[bold cyan]user:[/] ")
        if not user_input:
            continue
        messages.append(BetaMessageParam(role="user", content=user_input))

        with console.status("Waiting for model response...", spinner="dots"):
            response = client.run_inference(messages, system_prompt, "medium", TOOLS)

        response_message = "".join(
            block.text for block in response.content if block.type == "text"
        )
        messages.append(BetaMessageParam(role="assistant", content=response_message))
        console.print("[bold green]assistant: [/]", end="")
        label = "assistant: "
        console.print(Markdown(response_message), width=console.width - len(label))
        console.print()
except (KeyboardInterrupt, EOFError):
    console.print("\n[dim]bye![/]")
