import sys
from .parsing import parsing
from .classes import ParsingError, EncodingError
try:
    from llm_sdk import Small_LLM_Model
except Exception as error:
    print(f"{error}. Please install this module")
    sys.exit(1)


def call_me_maybe() -> None:
    try:
        parsing()
        encoding()
    except (ParsingError, EncodingError) as msg:
        print(msg)
        return
    # Feed to model
    # Get logits
    # Decoding
    # Format to JSON


def encoding() -> None:
    """Downloads the model from HuggingFace the first time we get an instance
        of the Small_LLM_Model class
    """
    try:
        llm: Small_LLM_Model = Small_LLM_Model(device="cpu")
        result = llm.encode("Hello, what is the world propulation right now?")
        print(f"Encoding result: {result}")
    except Exception as msg:
        raise EncodingError(str(msg))


if __name__ == "__main__":
    call_me_maybe()
