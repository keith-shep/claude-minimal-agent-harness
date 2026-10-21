import atexit
import subprocess
from collections.abc import Callable

from pydantic import BaseModel
from rich.console import Console

TtyLog = Callable[..., None]


def _terminal(script: str) -> str:
    result = subprocess.run(
        ["osascript", "-e", f'tell application "Terminal"\n{script}\nend tell'],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def open_terminal(title: str) -> str:
    """Open a new macOS Terminal window, closed again when this process exits,
    and return its tty path."""
    tty_path = _terminal(f"""
        set t to do script "clear"
        set custom title of t to "{title}"
        return tty of t
    """)
    atexit.register(
        _terminal,
        f"""
        repeat with w in windows
            if tty of selected tab of w is "{tty_path}" then
                close w
                exit repeat
            end if
        end repeat
        """,
    )
    return tty_path


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
