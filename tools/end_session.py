import sys

from anthropic import beta_tool


@beta_tool
def end_session_tool() -> str:
    """End the chat session and exit the program. Use when the user says goodbye or asks to quit or exit."""
    print("running end_session()")

    sys.exit()
