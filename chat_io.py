from rich.console import Console
from rich.markdown import Markdown
from rich.status import Status
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

SYSTEM_PROMPT_LABEL = "system prompt (enter for none): "
USER_LABEL = "user: "
ASSISTANT_LABEL = "assistant: "

theme = Theme(
    {
        "system": "bold yellow",
        "user": "bold cyan",
        "assistant": "bold green",
    }
)

console = Console(theme=theme)


def show_intro() -> None:
    console.print()
    console.print("[green]Setting up...")
    console.print("[green]Press Ctrl+C to end")


def ask_system_prompt() -> str:
    return console.input(f"[system]{SYSTEM_PROMPT_LABEL}[/]")


def ask_user() -> str:
    return console.input(f"[user]{USER_LABEL}[/]")


def waiting() -> Status:
    return console.status("Waiting for model response...", spinner="dots")


def show_assistant(text: str) -> None:
    grid = Table.grid()
    grid.add_column(no_wrap=True)
    grid.add_column()
    grid.add_row(Text(ASSISTANT_LABEL, style="assistant"), Markdown(text))
    console.print(grid)
    console.print()


def show_goodbye() -> None:
    console.print("\n[dim]bye![/]")
