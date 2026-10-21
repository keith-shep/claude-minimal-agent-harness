from rich.console import Console
from rich.markdown import Markdown
from rich.status import Status
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

from enums.role import Role

SYSTEM_PROMPT_STYLE = "system_prompt"
SYSTEM_PROMPT_LABEL = "system prompt (enter for none): "
USER_LABEL = f"{Role.USER}: "
ASSISTANT_LABEL = f"{Role.ASSISTANT}: "

theme = Theme(
    {
        SYSTEM_PROMPT_STYLE: "bold yellow",
        Role.USER: "bold cyan",
        Role.ASSISTANT: "bold green",
    }
)

console = Console(theme=theme)


def show_intro() -> None:
    console.print()
    console.print("[green]Setting up...")
    console.print("[green]Press Ctrl+C to end")


def show_debug_opening() -> None:
    console.print("[dim]Debug: opening request and response terminals...")


def show_debug_closing() -> None:
    console.print("[dim]Debug: closing request and response terminals...")


def ask_system_prompt() -> str:
    return console.input(f"[{SYSTEM_PROMPT_STYLE}]{SYSTEM_PROMPT_LABEL}[/]")


def ask_user() -> str:
    return console.input(f"[{Role.USER}]{USER_LABEL}[/]")


def waiting() -> Status:
    return console.status("Waiting for model response...", spinner="dots")


def show_assistant(text: str) -> None:
    grid = Table.grid()
    grid.add_column(no_wrap=True)
    grid.add_column()
    grid.add_row(Text(ASSISTANT_LABEL, style=Role.ASSISTANT), Markdown(text))
    console.print(grid)
    console.print()


def show_goodbye() -> None:
    console.print("\n[dim]bye![/]")
