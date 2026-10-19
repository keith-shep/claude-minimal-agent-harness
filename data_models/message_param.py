# based on anthropics MessageParam

from typing import TypedDict

from enums.role import Role


class Message(TypedDict):
    role: Role
    content: str
