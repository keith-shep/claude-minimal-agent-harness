import argparse

from anthropic.types.beta import BetaMessageParam

from anthropic_client import AnthropicClient
from modules import chat_io
from modules.tty_logger import open_terminal, tty_logger
from tools.registry import TOOLS

parser = argparse.ArgumentParser()
parser.add_argument(
    "--debug",
    action="store_true",
    help="open Terminal windows showing requests and responses",
)
args = parser.parse_args()

log = (
    tty_logger(request=open_terminal("request"), response=open_terminal("response"))
    if args.debug
    else None
)
client = AnthropicClient(log=log)

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
