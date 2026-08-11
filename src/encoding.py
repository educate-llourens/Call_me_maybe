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
        f"Here are the tools you have: {'\n'.join(tools)}\n"
        f"Here is the test prompt: {prompt.prompt}\n"
        "Respond with the correct function call in correct JSON format. Here "
        "is an example:\n"
        "{'name': 'function_name',\n"
        "'parameters': {'s': 'hello'}"
        "}"
    )
    tokens: Tensor = llm.encode(instruction_prompt)
    return tokens
