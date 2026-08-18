from llm_sdk import Small_LLM_Model
from torch import Tensor
import numpy


def stage_generation(llm: Small_LLM_Model,
                     encoded_tokens: Tensor) -> list[int]:
    max_tokens: int = len(encoded_tokens * 2)
    encoded_tokens_int: list[int] = encoded_tokens[0].tolist()
    end_token: int | float = llm.encode("<|im_end|>")[0][-1].item()
    next_token_id: int = 0

    for i in range(max_tokens):
        logits: list[float] = llm.get_logits_from_input_ids(encoded_tokens_int)
        next_token_id = int(numpy.argmax(logits))
        encoded_tokens_int.append(next_token_id)
        if next_token_id == end_token:
            break
    return encoded_tokens_int
