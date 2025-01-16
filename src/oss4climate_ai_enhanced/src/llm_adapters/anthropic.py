"""
Adapter to Anthropic's LLM

Note: this requires setting up an API key here: https://console.anthropic.com/settings/keys
"""

import os

from anthropic import Anthropic as _Anthropic

from oss4climate_ai_enhanced.src.llm_adapters import LlmAdapter, LlmPromptResult


class AnthropicLlmAdapter(LlmAdapter):
    def __init__(self, model: str = "claude-3-5-haiku-20241022"):
        super().__init__()
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if api_key is None:
            raise EnvironmentError(
                "An ANTHROPIC_API_KEY must be defined in environment for this to work"
            )
        self.__anthropic_client = _Anthropic(
            api_key=api_key,
        )
        self.__model = model

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
            model=self.__model,
        )
        return LlmPromptResult(
            text=raw_res.content[0].text,
        )
