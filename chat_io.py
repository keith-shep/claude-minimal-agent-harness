from rich.console import Console
from rich.markdown import Markdown
from rich.status import Status

SYSTEM_PROMPT_LABEL = "system prompt (enter for none): "
USER_LABEL = "user: "
ASSISTANT_LABEL = "assistant: "

console = Console()


def show_intro() -> None:
    console.print()
    console.print("[green]Setting up...")
    console.print("[green]Press Ctrl+C to end")


def ask_system_prompt() -> str:
    return console.input(f"[bold yellow]{SYSTEM_PROMPT_LABEL}[/]")


def ask_user() -> str:
    return console.input(f"[bold cyan]{USER_LABEL}[/]")


def waiting() -> Status:
    return console.status("Waiting for model response...", spinner="dots")


def show_assistant(text: str) -> None:
    console.print(f"[bold green]{ASSISTANT_LABEL}[/]", end="")
    console.print(Markdown(text), width=console.width - len(ASSISTANT_LABEL))
    console.print()


def show_goodbye() -> None:
    console.print("\n[dim]bye![/]")
