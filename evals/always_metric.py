import re

from anthropic.types import MessageParam
from rich.console import Console

from anthropic_client import AnthropicClient

SYSTEM_PROMPT = "use metric units. never use imperial units"
RUNS = 3

TEST_INPUTS = [
    "give me a cake recipe",
]

IMPERIAL = re.compile(
    r"\b(cups?|oz|ounces?|lbs?|pounds?|sticks? of butter|"
    r"tsps?|tbsps?|teaspoons?|tablespoons?|"
    r"inch(es)?|quarts?|pints?|fahrenheit)\b|°\s?F\b|\d+\s?F\b",
    re.IGNORECASE,
)

client = AnthropicClient()


def get_reply(user_input: str) -> str:
    messages: list[MessageParam] = [MessageParam(role="user", content=user_input)]
    response = client.run_inference(messages, SYSTEM_PROMPT)
    return "".join(b.text for b in response.content if b.type == "text")


def find_leaks(reply: str) -> list[str]:
    return sorted({m.group(0).lower() for m in IMPERIAL.finditer(reply)})


passed = 0
total = 0
console = Console()
for user_input in TEST_INPUTS:
    for run in range(1, RUNS + 1):
        reply = get_reply(user_input)
        leaks = find_leaks(reply)
        total += 1
        if not leaks:
            passed += 1
        status = "[bold green]PASS[/]" if not leaks else f"[bold red]FAIL {leaks}[/]"
        console.print(f"\\[{run}/{RUNS}] {status}  {user_input}")

print(f"\nscore: {passed}/{total}")
