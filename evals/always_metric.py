import re

from anthropic.types import MessageParam

from anthropic_client import AnthropicClient

SYSTEM_PROMPT = "use metric units"
RUNS = 3

TEST_INPUTS = [
    "give me a cake recipe",
]

IMPERIAL = re.compile(
    r"\b(cups?|oz|ounces?|lbs?|pounds?|sticks? of butter|"
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

for user_input in TEST_INPUTS:
    for run in range(1, RUNS + 1):
        reply = get_reply(user_input)
        leaks = find_leaks(reply)
        total += 1
        if not leaks:
            passed += 1
        status = "PASS" if not leaks else f"FAIL {leaks}"
        print(f"[{run}/{RUNS}] {status}  {user_input}")

print(f"\nscore: {passed}/{total}")
