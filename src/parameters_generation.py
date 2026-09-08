from llm_sdk import Small_LLM_Model
from numpy import argmax
from src.classes import FunctionDefinitionValidation, InputFileValidation, DecodingError
from torch import Tensor
from colorama import Fore, Back
from json import loads, JSONDecodeError
from typing import Any


# Test ------------------------------------------------------------------------
def parameters_process(
    llm: Small_LLM_Model,
    functions_definition_list: list[FunctionDefinitionValidation],
    function_name: str,
    prompt: InputFileValidation
) -> dict:
    fn_def = next(function for function in functions_definition_list if function.name == function_name)
    base_prompt_ids = parameters_prompt_encoding(
        functions_definition_list, function_name, prompt, llm)

    result: dict = {}

    for param_name in fn_def.parameters:          # you supply the key, not the model
        prompt_ids = base_prompt_ids + llm.encode(f'"{param_name}": ')[0].tolist()
        value_str = generate_value(llm, prompt_ids)
        result[param_name] = parse_value(value_str, fn_def.parameters[param_name]["type"])
    print(result)
    return result


def parse_value(value_str: str, param_type: str) -> Any:
    """
    Converts the raw generated string into the correct Python type,
    based on the parameter's declared type.
    """
    value_str = value_str.strip().strip('"').strip("'")

    match param_type:
        case "number":
            return float(value_str)
        case "integer":
            return int(float(value_str))   # handles "2.0" -> 2 safely
        case "string":
            return value_str
        case "boolean":
            return value_str.lower() == "true"
        case _:
            raise DecodingError(f"parse_value | unknown type {param_type!r}")


def generate_value(llm: Small_LLM_Model, prompt_ids: list[int],
                    max_nbr_tokens: int = 20) -> str:
    generated = ""
    for _ in range(max_nbr_tokens):
        logits = llm.get_logits_from_input_ids(prompt_ids)
        if len(prompt_ids) >= 2 and prompt_ids[-1] == prompt_ids[-2]:
            logits = logits[:]
            logits[prompt_ids[-1]] = float("-inf")
        next_id = int(argmax(logits))
        next_token = llm.decode([next_id])
        prompt_ids += [next_id]
        generated += next_token
        stop_positions = [generated.find(ch) for ch in (",", "}") if ch in generated]
        if stop_positions:
            generated = generated[:min(stop_positions)]
            break
    return generated.rstrip(", }").strip()
# -----------------------------------------------------------------------------


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
        "You are given a function name and its parameters. "
        "Extract the parameter values from the user's message and "
        "return ONLY a JSON object in this exact format:\n"
        "<parameters></parameters>\n"
        "#Example\n"
        "<parameters>\n"
        '{"parameters": {"a": 2.0, "b": 3.0}}\n'
        "If the parameter name is 'regex', return a JSON object in"
        "this format:\n"
        "#Example\n"
        "<parameters>\n"
        '{"parameters": {"regex": "\\d+", ...}}\n'
        "</parameters><|im_end|>\n"
        "<|im_start|>user\n"
        f"{prompt.prompt}<|im_end|>\n"
        "<|im_start|>assistant\n"
        f"<tool_call>\n{function_name}\n</tool_call>\n"
        "<parameters>\n"
        '{"parameters": '
    )
    tokens: Tensor = llm.encode(instruction_prompt)
    return tokens[0].tolist()
