import re

from anthropic.types import MessageParam
from rich.console import Console
from rich.markup import escape

from anthropic_client import AnthropicClient

SYSTEM_PROMPTS = [
    "Use metric units only. Give small amounts in ml or grams, never teaspoons or tablespoons.",
    "Use metric units only: grams for weight, ml for volume, °C for temperature, cm for size. Don't add notes about measurements.",
    (
        "Use metric units only. Write ingredients like this:\n"
        "- 200 g flour\n"
        "- 10 g baking powder\n"
        "- 5 ml vanilla extract\n"
        "Don't add notes about measurements."
    ),
]
RUNS = 10

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


def get_reply(user_input: str, system_prompt: str) -> str:
    messages: list[MessageParam] = [MessageParam(role="user", content=user_input)]
    response = client.run_inference(messages, system_prompt)
    return "".join(b.text for b in response.content if b.type == "text")


def find_leaks(reply: str) -> list[str]:
    return sorted({m.group(0).lower() for m in IMPERIAL.finditer(reply)})


passed = 0
total = 0
console = Console()
for system_prompt in SYSTEM_PROMPTS:
    console.rule(system_prompt[:60])
    passed = 0
    total = 0
    for user_input in TEST_INPUTS:
        for run in range(1, RUNS + 1):
            reply = get_reply(user_input, system_prompt)
            leaks = find_leaks(reply)
            total += 1
            if not leaks:
                passed += 1
            else:
                for line in reply.splitlines():
                    if IMPERIAL.search(line):
                        highlighted = IMPERIAL.sub(
                            lambda m: f"[bold red]{m.group(0)}[/]", escape(line)
                        )
                        console.print(f"    [dim]>[/] {highlighted}")
            status = (
                "[bold green]PASS[/]" if not leaks else f"[bold red]FAIL {leaks}[/]"
            )
            console.print(f"\\[{run}/{RUNS}] {status}  {user_input}")

print(f"\nscore: {passed}/{total}")
