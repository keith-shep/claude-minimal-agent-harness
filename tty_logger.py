from rich.console import Console


def log_to_tty(tty_path: str, title: str, data: object) -> None:
    if not tty_path:
        return
    with open(tty_path, "w") as tty:
        console = Console(file=tty, force_terminal=True)
        console.rule(title)
        console.print_json(data=data, default=str)
