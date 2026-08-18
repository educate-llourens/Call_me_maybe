from llm_sdk import Small_LLM_Model
from numpy import argmax


def generation(llm: Small_LLM_Model,
               encoded_tokens: list[int]) -> list[int]:
    """Takes the token id's, finds the highest logit and appends the token id
    of the logit to the end of the prompt id's

    Notes:
    - Yes/no or single-word answer → maybe 5-10 tokens
    - A sentence or short answer → 50-100 tokens
    - A paragraph → 200-500 tokens
    - An essay, long code file, or detailed explanation → 1000-4000+ tokens
    - argmax returns intp
    Args:
        llm (Small_LLM_Model): _description_
        encoded_tokens (Tensor): _description_

    Returns:
        list[int]: _description_
    """
    nbr_tokens: int = 50

    for _ in range(nbr_tokens):
        logits: list[float] = llm.get_logits_from_input_ids(encoded_tokens)
        next_id: int = int(argmax(logits))
        encoded_tokens.append(next_id)
        if next_id == int(llm.encode("<|im_end|>")[0][-1]):
            break
    return encoded_tokens
