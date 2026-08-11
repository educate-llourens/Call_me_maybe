from llm_sdk import Small_LLM_Model
from src.classes import FunctionDefinitionValidation, InputFileValidation
from torch import Tensor


def stage_encoding(functions_definition_list:
                   list[FunctionDefinitionValidation],
                   prompt: InputFileValidation,
                   llm: Small_LLM_Model) -> Tensor:
    tools: list[str] = [function.model_dump_json() for function in
                        functions_definition_list]
    instruction_prompt: str = (
        f"<|im_start|>system\n"
        f"You are a function identifier and these are your tools\n "
        f"<tool_call>{'\n'.join(tools)}</tool_call>\n"
        f"Respond with the correct function call format. Here "
        f"is an example:\n"
        f"name: name of the function\n"
        f"parameter_name: parameter1, parameter1 type, "
        "paramater_name: parameter2, parameter2 type\n"
        f"<|im_end|>\n"
        f"<|im_start|>user\n"
        f"{prompt.prompt}\n"
        f"<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )
    tokens: Tensor = llm.encode(instruction_prompt)
    return tokens
