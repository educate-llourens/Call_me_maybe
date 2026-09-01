from llm_sdk import Small_LLM_Model
from numpy import argmax
from src.classes import FunctionDefinitionValidation, InputFileValidation
from torch import Tensor


def function_name_process(
    llm: Small_LLM_Model,
    functions_definition_list: list[FunctionDefinitionValidation],
    prompt: InputFileValidation
) -> None:
    max_nbr_tokens = 48
    remaining_functions: list[str] = [
        function.name for function in functions_definition_list]
    generated_tokens_str: str = ""
    prompt_ids: list[int] = function_name_encoding(
        functions_definition_list, prompt, llm)

    for _ in range(max_nbr_tokens):
        allowed_ids: set[int] = set()
        for name in remaining_functions:
            allowed_ids.update(llm.encode(name)[0].tolist())

        logits: list[float] = llm.get_logits_from_input_ids(prompt_ids)
        for i in range(len(logits)):
            if i not in allowed_ids:
                logits[i] = float("-inf")

        next_id: int = int(argmax(logits))
        generated_tokens_str += llm.decode([next_id])   # build up, not reset
        prompt_ids += [next_id]                          # advance the input

        for function in remaining_functions:
            if not function.startswith(generated_tokens_str):
                remaining_functions.remove(function)

        if len(remaining_functions) == 1:
            print(remaining_functions[0])
            return
        elif not remaining_functions:
            print("Could not find function")
            return
    print(generated_tokens_str)
    print("Could not find function")


# Utility functions -----------------------------------------------------------
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


def parameter_encoding(
    function_definition: FunctionDefinitionValidation,
    prompt: InputFileValidation,
    input_tests_list: list[InputFileValidation],
    llm: Small_LLM_Model
) -> Tensor:
    instruction_prompt: str = (
        "<|im_start|>system\n"
        f"<tools>{function_definition}\n</tools>\n\n"
        "Return a string with only the parameters"
        " within <tool_call></tool_call>\n"
        "#Example\n"
        "<tool_call>\n"
        "2 3\n"
        "</tool_call><|im_end|>\n"
        "<|im_start|>user\n"
        f"{prompt.prompt}<|im_end|>\n"
        "<|im_start|>assistant\n"
        "<tool_call>\n"
    )
    tokens: Tensor = llm.encode(instruction_prompt)
    return tokens


def get_allowed_tokens_str(functions_definition_list:
                           list[FunctionDefinitionValidation]) -> str:
    allowed_tokens_str = ""
    function_names_list: list[str] = [
        function.name for function in functions_definition_list
    ]
    for function_name in function_names_list:
        allowed_tokens_str += function_name + " "
    return allowed_tokens_str
