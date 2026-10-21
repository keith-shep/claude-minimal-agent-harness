import argparse

from anthropic.types.beta import BetaMessageParam

import chat_io
from anthropic_client import AnthropicClient
from tools.registry import TOOLS

parser = argparse.ArgumentParser()
parser.add_argument(
    "--requests-tty", help="terminal device for debug output, e.g. /dev/ttys008"
)
parser.add_argument(
    "--responses-tty", help="terminal device for debug output, e.g. /dev/ttys009"
)
args = parser.parse_args()

client = AnthropicClient(args.requests_tty, args.responses_tty)

chat_io.show_intro()
try:
    system_prompt = chat_io.ask_system_prompt()

    messages: list[BetaMessageParam] = []

    while True:
        user_input = chat_io.ask_user()
        if not user_input:
            continue
        messages.append(BetaMessageParam(role="user", content=user_input))

        with chat_io.waiting():
            response = client.run_inference(messages, system_prompt, "medium", TOOLS)

        response_message = "".join(
            block.text for block in response.content if block.type == "text"
        )
        messages.append(BetaMessageParam(role="assistant", content=response_message))
        chat_io.show_assistant(response_message)
except (KeyboardInterrupt, EOFError):
    chat_io.show_goodbye()
