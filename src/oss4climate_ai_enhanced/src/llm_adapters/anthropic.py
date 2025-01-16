import os

from anthropic import Anthropic as _Anthropic

from . import LlmAdapter, LlmPromptResult


class AnthropicAdapter(LlmAdapter):
    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if api_key is None:
            raise EnvironmentError(
                "An ANTHROPIC_API_KEY must be defined in environment for this to work"
            )
        self.__anthropic_client = _Anthropic(
            api_key=api_key,
        )

    def _llm_prompt(self, system_request: str, user_request: str) -> LlmPromptResult:
        raw_res = self.__anthropic_client.messages.create(
            max_tokens=1024,
            system=system_request,
            messages=[
                {
                    "role": "user",
                    "content": user_request,
                },
            ],
            model="claude-3-5-haiku-20241022",
        )
        return LlmPromptResult(
            text=raw_res.content[0].text,
        )
