from typing import Any
from llm_sdk import Small_LLM_Model


def stage_encoding(functions_definition_list: list[Any],
                   input_prompts_list: list[Any],
                   llm: Small_LLM_Model) -> list[int]:
    encode_string: str

    encode_string = (
        'You can only choose one function from this ordered list to solve the '
        'prompt. Return the number of the correct function, and the parameters'
        ' in this format: "parameters": {"a": 2.0, "b": 3.0}'
    )
    return []
