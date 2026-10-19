import anthropic
import os
from dotenv import load_dotenv
load_dotenv() 


class AnthropicClient(anthropic.Anthropic):
  def __init__(self) -> None:
        super().__init__(api_key=os.getenv("API_KEY"))
