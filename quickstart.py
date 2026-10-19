from typing import cast

from anthropic.types import MessageParam, TextBlock

from anthropic_client import AnthropicClient

client = AnthropicClient()

messages: list[MessageParam] = []

while True:
    user_input = input("user: ")

    messages.append(MessageParam(role="user", content=user_input))

    response = client.run_inference(messages)

    response_message = cast(TextBlock, response.content[0]).text
    messages.append(MessageParam(role="assistant", content=response_message))
    print("assistant:", response_message)

    # user_input = input("You: ")
    # messages.extend(
    #     [
    #         MessageParam(role="assistant", content=response_message),
    #         MessageParam(role="user", content=user_input),
    #     ]
    # )

    # response = client.run_inference(messages)

    # response_message = cast(TextBlock, response.content[0]).text
    # print(response_message)

    # print_json(response.model_dump_json(indent=2, exclude_none=True))
