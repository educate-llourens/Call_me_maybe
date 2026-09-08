from llm_sdk import Small_LLM_Model
from numpy import argmax
from src.classes import FunctionDefinitionValidation, InputFileValidation
from torch import Tensor
from colorama import Fore


def function_name_process(
    llm: Small_LLM_Model,
    functions_definition_list: list[FunctionDefinitionValidation],
    prompt: InputFileValidation
) -> str:
    max_nbr_tokens = 10
    remaining_functions: list[str] = [
        function.name for function in functions_definition_list]
    generated_tokens_str: str = ""
    prompt_ids: list[int] = function_name_encoding(
        functions_definition_list, prompt, llm)
    for _ in range(max_nbr_tokens):
        allowed_ids: set[int] = set()
        for function in remaining_functions:
            remainder = function[len(generated_tokens_str):]
            if remainder:
                first_token_id = llm.encode(remainder)[0].tolist()[0]
                allowed_ids.add(first_token_id)
        logits: list[float] = llm.get_logits_from_input_ids(prompt_ids)
        for i in range(len(logits)):
            if i not in allowed_ids:
                logits[i] = float("-inf")
        next_id: int = int(argmax(logits))
        generated_tokens_str += llm.decode([next_id])
        prompt_ids += [next_id]
        print(Fore.LIGHTGREEN_EX + "Generated tokens string: " + Fore.RESET +
              f"{generated_tokens_str}")
        remaining_functions = [
            function for function in remaining_functions
            if function.startswith(generated_tokens_str)
        ]
        print(Fore.LIGHTGREEN_EX + "remaining functions: " +
              Fore.RESET + f"{remaining_functions}" + Fore.RESET)
        if len(remaining_functions) == 1:
            return (remaining_functions[0])
        elif not remaining_functions:
            print(f"We could not find a matching function for {prompt}")
    return ""


def function_name_encoding(
    functions_definition_list: list[FunctionDefinitionValidation],
    prompt: InputFileValidation,
    llm: Small_LLM_Model
) -> list[int]:
    tools_list: list[str] = [function.model_dump_json() for function in
                             functions_definition_list]
    tools_str: str = "".join(f"\n{tool}" for tool in tools_list)
    instruction_prompt: str = (
        "<|im_start|>system\n"
        # "# Tools\n\n"
        # "You are provided with function signatures within <tools></tools> "
        f"<tools>{tools_str}\n</tools>\n\n"
        "Return a string only containing the function name"
        "<tool_call></tool_call>\n"
        "#Example\n"
        "<tool_call>\n"
        "fn_add_numbers\n"
        "</tool_call><|im_end|>\n"
        "<|im_start|>user\n"
        f"{prompt.prompt}<|im_end|>\n"
        "<|im_start|>assistant\n"
    )
    tokens: Tensor = llm.encode(instruction_prompt)
    return tokens[0].tolist()
