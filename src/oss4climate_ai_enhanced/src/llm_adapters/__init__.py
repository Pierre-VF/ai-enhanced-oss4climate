import json
from dataclasses import dataclass


@dataclass
class LlmPromptResult:
    text: str


class LlmAdapter:
    """
    This is a template for what needs to be implemented for adapter classes
    """

    def __init__(self):
        pass

    def _llm_prompt(self, system_request: str, user_request: str) -> LlmPromptResult:
        raise NotImplementedError("This must be implemented in children methods")

    def extract_use_cases(
        self,
        readme_str: str,
        n_use_cases: int = 5,
    ) -> list[str]:
        x = self._llm_prompt(
            system_request=f"""
            You are an expert at classifying readme text from code repositories into applications that the associated code relates to. 
            Your input is a raw readme file from a repository. 
            For each request, your output is given single JSON formatted list of {int(n_use_cases)} use-cases as strings. Omit any additional text.
            """,
            user_request=readme_str,
        )
        out = json.loads(x.text)
        return out

    def extract_topics(
        self,
        readme_str: str,
        n_topics: int = 5,
    ) -> list[str]:
        x = self._llm_prompt(
            system_request=f"""
            You are an expert at classifying readme text from code repositories into topics that the associated code relates to. 
            Your input is a raw readme file from a repository. 
            For each request, your output is given single JSON formatted list of {int(n_topics)} n_topics as strings. Omit any additional text.
            """,
            user_request=readme_str,
        )
        out = json.loads(x.text)
        return out
