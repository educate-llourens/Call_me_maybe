from llm_sdk import Small_LLM_Model
from numpy import argmax
from src.classes import (
    FunctionDefinitionValidation, InputFileValidation, DecodingError)
from torch import Tensor
from colorama import Fore, Back
from typing import Any


def parameters_process(
    llm: Small_LLM_Model,
    functions_definition_list: list[FunctionDefinitionValidation],
    function_name: str,
    prompt: InputFileValidation
) -> dict:
    """Extracts the parameters for the given prompt based on the function name
    and its definition dict.

    Args:
        llm (Small_LLM_Model): LLM Instance
        functions_definition_list (list[FunctionDefinitionValidation]):
        List of validated function definitions
        function_name (str): Name of the function to extract the parameters
        for
        prompt (InputFileValidation): The validated prompt

    Returns:
        dict: The dict of parameters
    """
    fn_def: FunctionDefinitionValidation = (
        next(
            function
            for function in functions_definition_list
            if function.name == function_name))
    base_prompt_ids = parameters_prompt_encoding(
        functions_definition_list, function_name, prompt, llm)
    return_dict: dict = {}

    for param_name in fn_def.parameters:
        prompt_ids = (
            base_prompt_ids + llm.encode(f'"{param_name}": ')[0].tolist())
        print("")
        print(Fore.LIGHTGREEN_EX + f"Getting {param_name} value...")
        value_str = generate_value(llm, prompt_ids, param_name)
        return_dict[param_name] = (
            parse_value(value_str, fn_def.parameters[param_name]["type"]))
        print(Fore.LIGHTGREEN_EX +
              "Return dict parameters keys: " +
              Fore.RESET +
              f"{return_dict.keys()}")
        print(
            Fore.LIGHTGREEN_EX +
            "Return dict parameters: " +
            Fore.RESET +
            f"{return_dict}")
    print(Back.LIGHTGREEN_EX + "Return json: " + Back.RESET + f"{return_dict}")
    return return_dict


def parse_value(value_str: str, param_type: str) -> Any:
    """
    Converts the raw generated string into the correct Python type,
    based on the parameter's declared type.
    """
    value_str = value_str.strip().strip('"').strip("'")

    try:
        if param_type == "number":
            return float(value_str)
        elif param_type == "integer":
            return int(float(value_str))
        elif param_type == "string":
            return value_str
        elif param_type == "boolean":
            return value_str.lower() == "true"
        else:
            raise DecodingError(f"parse_value | unknown type {param_type}")
    except ValueError as msg:
        raise DecodingError(f"Value Error | {value_str}: {msg}")


def generate_value(llm: Small_LLM_Model, prompt_ids: list[int],
                   paramater_name: str, max_nbr_tokens: int = 20) -> str:
    """Generates the value for the parameter name

    Args:
        llm (Small_LLM_Model): LLM instance
        prompt_ids (list[int]): List of id's from the encoded prompt
        paramater_name (str): The name or key that we need to find the value
        for max_nbr_tokens (int, optional): The maximum number of tokens to
        loop through to keep processing minimal and ensure it does not
        take too much time and resources. Defaults to 20.

    Returns:
        str: The generated value as a string.
    """
    generated_str = ""
    for _ in range(max_nbr_tokens):
        logits: list[float] = llm.get_logits_from_input_ids(prompt_ids)
        next_id = int(argmax(logits))
        prompt_ids += [next_id]
        generated_str += llm.decode([next_id])
        print(
            Fore.LIGHTGREEN_EX +
            "Generated value: {" +
            f"'{paramater_name}': " +
            Fore.RESET +
            f"{generated_str}")
        stop_positions = [
            generated_str.find(ch) for ch in (",", "}") if ch in generated_str]
        if stop_positions:
            generated_str = generated_str[:min(stop_positions)]
            break
    return generated_str.rstrip(", }").strip()


def parameters_prompt_encoding(
    functions_definition_list: list[FunctionDefinitionValidation],
    function_name: str,
    prompt: InputFileValidation,
    llm: Small_LLM_Model
) -> list[int]:
    """Creates the prompt to look for parameters and encodes the prompt

    Args:
        functions_definition_list (list[FunctionDefinitionValidation]):
        List of validated function definitions
        function_name (str): Name of the function we need to call
        prompt (InputFileValidation): Validated prompt we need to extract the
        parameters from
        llm (Small_LLM_Model): LLM instance

    Returns:
        list[int]: List of id's from the encoded prompt
    """
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
        "Case sensitivity is important"
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
