from typing import Any
from llm_sdk import Small_LLM_Model
from json import dumps


def stage_encoding(functions_definition_list: list[Any],
                   prompt: Any,
                   llm: Small_LLM_Model) -> list[int]:
    prompt_str = create_prompt(functions_definition_list, prompt)
    return []


def create_prompt(functions_definition_list: list[Any], prompt) -> str:
    definition_list_json = ([dumps(function) for
                            function in functions_definition_list])
    return ""
