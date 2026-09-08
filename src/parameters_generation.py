from llm_sdk import Small_LLM_Model
from numpy import argmax
from src.classes import FunctionDefinitionValidation, InputFileValidation
from torch import Tensor
from colorama import Fore, Back


def parameters_process(
    llm: Small_LLM_Model,
    functions_definition_list: list[FunctionDefinitionValidation],
    function_name: str,
    prompt: InputFileValidation
) -> dict:
    prompt_ids: list[int] = parameters_prompt_encoding(
        functions_definition_list, function_name, prompt, llm)
    
    return {}


def parameters_prompt_encoding(
    functions_definition_list: list[FunctionDefinitionValidation],
    function_name: str,
    prompt: InputFileValidation,
    llm: Small_LLM_Model
) -> list[int]:
    tools_list: list[str] = [
        function.model_dump_json() for function in functions_definition_list]
    tools_str: str = "".join(f"\n{tool}" for tool in tools_list)
    instruction_prompt: str = (
        "<|im_start|>system\n"
        f"<tools>{tools_str}\n</tools>\n\n"
        f"Return a string with only the parameters for {function_name}"
        "<tool_call></tool_call>\n"
        "#Example\n"
        "<tool_call>\n"
        "2 3"
        "</tool_call><|im_end|>\n"
        "<|im_start|>user\n"
        f"{prompt.prompt}<|im_end|>\n"
        "<|im_start|>assistant\n"
    )
    tokens: Tensor = llm.encode(instruction_prompt)
    return tokens[0].tolist()
