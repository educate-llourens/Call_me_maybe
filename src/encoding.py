from llm_sdk import Small_LLM_Model
from src.classes import FunctionDefinitionValidation, InputFileValidation
from torch import Tensor


def function_name_encoding(
    functions_definition_list: list[FunctionDefinitionValidation],
    prompt: InputFileValidation,
    llm: Small_LLM_Model
) -> Tensor:
    tools_list: list[str] = [function.model_dump_json() for function in
                             functions_definition_list]
    tools_str: str = "".join(f"\n{tool}" for tool in tools_list)
    instruction_prompt: str = (
        "<|im_start|>system\n"
        "# Tools\n\n"
        "You may call one function to assist with the user query.\n\n"
        "You are provided with function signatures within <tools></tools> "
        "XML tags:\n"
        f"<tools>{tools_str}\n</tools>\n\n"
        "For each function call, return a string with function name "
        "within <tool_call></tool_call> XML tags:\n"
        "<tool_call>\n"
        '<function-name>\n'
        "</tool_call><|im_end|>\n"
        "<|im_start|>user\n"
        f"{prompt.prompt}<|im_end|>\n"
        "<|im_start|>assistant\n"
    )
    tokens: Tensor = llm.encode(instruction_prompt)
    return tokens


def parameter_encoding(
    function_definition: FunctionDefinitionValidation,
    prompt: InputFileValidation,
    input_tests_list: list[InputFileValidation],
    llm: Small_LLM_Model
) -> Tensor:
    instruction_prompt: str = (
        "<|im_start|>system\n"
        "# Tools\n\n"
        "You are provided with function signatures within <tools></tools> "
        "XML tags:\n"
        f"<tools>{function_definition}\n</tools>\n\n"
        "For each function call, return a string with the parameters"
        " within <tool_call></tool_call> XML tags:\n"
        "<tool_call>\n"
        '<parameter 1>, <parameter 2>\n'
        "</tool_call><|im_end|>\n"
        "<|im_start|>user\n"
        f"{prompt.prompt}<|im_end|>\n"
        "<|im_start|>assistant\n"
    )
    tokens: Tensor = llm.encode(instruction_prompt)
    return tokens

# TODO: Add error handling
# TODO: Add doctrings
