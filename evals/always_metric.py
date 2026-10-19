import re
from concurrent.futures import ThreadPoolExecutor

from anthropic.types import MessageParam
from rich.console import Console
from rich.markup import escape

from anthropic_client import AnthropicClient

SYSTEM_PROMPTS = [
    "Use metric units only. Give small amounts in ml or grams, never teaspoons or tablespoons.",
    # "Use metric units only: grams for weight, ml for volume, °C for temperature, cm for size. Don't add notes about measurements.",
    # (
    #     "Use metric units only. Write ingredients like this:\n"
    #     "- 200 g flour\n"
    #     "- 10 g baking powder\n"
    #     "- 5 ml vanilla extract\n"
    #     "Don't add notes about measurements."
    # ),
    # "Use metric units only. Give small amounts in ml or grams, never teaspoons or tablespoons. Don't add notes or explanations about measurements. Instead of saying 2 tbsp milk (about 30 ml), just say 30ml milk",
]
RUNS = 10

TEST_INPUTS = [
    "give me a cake recipe",
    "give me a cocktail recipe",
    "give me a bread recipe",
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


def run_job(job: tuple[str, int]) -> str:
    user_input, _run = job
    return get_reply(user_input, system_prompt)


passed = 0
total = 0
console = Console()

MAX_WORKERS = 8

for system_prompt in SYSTEM_PROMPTS:
    console.rule(system_prompt[:60])

    jobs: list[tuple[str, int]] = [
        (user_input, run) for user_input in TEST_INPUTS for run in range(1, RUNS + 1)
    ]

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        replies = list(pool.map(run_job, jobs))

    passed = 0
    passed = 0
    for (user_input, run), reply in zip(jobs, replies):
        leaks = find_leaks(reply)

        status = "[bold green]PASS[/]" if not leaks else f"[bold red]FAIL {leaks}[/]"
        console.print(f"\\[{run}/{RUNS}] {status}  {user_input}")

        if not leaks:
            passed += 1
        else:
            for line in reply.splitlines():
                if IMPERIAL.search(line):
                    highlighted = IMPERIAL.sub(
                        lambda m: f"[bold red]{m.group(0)}[/]", escape(line)
                    )
                    console.print(f"    [dim]>[/] {highlighted}")

    console.print(f"\nscore: {passed}/{len(jobs)}\n")
