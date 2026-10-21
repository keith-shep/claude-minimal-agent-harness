import subprocess
from collections.abc import Callable

from pydantic import BaseModel
from rich.console import Console

TtyLog = Callable[..., None]


def open_terminal(title: str) -> str:
    """Open a new macOS Terminal window and return its tty path."""
    script = f"""
        tell application "Terminal"
            set t to do script "clear"
            set custom title of t to "{title}"
            return tty of t
        end tell
    """
    result = subprocess.run(
        ["osascript", "-e", script], capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def tty_logger(**tty_paths: str | None) -> TtyLog:
    # kept open for the life of the process
    consoles = {
        title: Console(file=open(path, "w"), force_terminal=True)  # noqa: SIM115
        for title, path in tty_paths.items()
        if path
    }

    def log(**data: object) -> None:
        for title, value in data.items():
            console = consoles.get(title)
            if console is None:
                continue
            if isinstance(value, BaseModel):
                value = value.model_dump(mode="json", exclude_none=True)
            console.rule(title)
            console.print_json(data=value, default=str)

    return log
