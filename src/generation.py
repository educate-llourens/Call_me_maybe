from llm_sdk import Small_LLM_Model
from numpy import argmax
from src.classes import FunctionDefinitionValidation, InputFileValidation
from torch import Tensor


def function_name_process(llm: Small_LLM_Model,
                          functions_definition_list:
                              list[FunctionDefinitionValidation],
                          prompt: InputFileValidation) -> None:
    max_nbr_tokens: int = 1200
    allowed_tokens_str = ""

    function_names_list: list[str] = [function.name for function in
                                      functions_definition_list]
    for function_name in function_names_list:
        allowed_tokens_str += function_name
    allowed_tokens: list[int] = llm.encode(allowed_tokens_str)[0].tolist()
    stop_token: int = llm.encode("<|im_end|>\n")[0].tolist()[0]
    function_name_prompt_id_list: list[int] = function_name_encoding(
            functions_definition_list, prompt, llm)
    mask_count = 0
    step = 0
    for _ in range(max_nbr_tokens):
        logits: list[float] = (
            llm.get_logits_from_input_ids(function_name_prompt_id_list))
        next_id: int = int(argmax(logits))
        while next_id not in allowed_tokens and next_id != stop_token:
            logits[next_id] = float("-inf")
            next_id = int(argmax(logits))
            mask_count += 1
            step += 1
        print(f"[outer step {step}] next_id={next_id}  masked={mask_count}")
        if next_id == stop_token:
            break
        function_name_prompt_id_list.append(next_id)
    print(llm.decode(function_name_prompt_id_list))


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