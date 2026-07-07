from llm_sdk import Small_LLM_Model
from argparse import ArgumentParser, Namespace


def call_me_maybe() -> None:
    parsing()
    encoding()
    # Feed to model
    # Get logits
    # Decoding
    # Format to JSON


def parsing() -> None:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("--functions_definition",
                        default="data/input/functions_definition.json")
    parser.add_argument("--input",
                        default="data/input/function_calling_tests.json")
    parser.add_argument("--output",
                        default="data/output/function_calls.json")
    args: Namespace = parser.parse_args()


def encoding() -> None:
    """Downloads the model from HuggingFace the first time we get an instance
        of the Small_LLM_Model class
    """
    llm: Small_LLM_Model = Small_LLM_Model(device="cpu")
    result = llm.encode("Hello, what is the world propulation right now?")
    print(f"Encoding result: {result}")


if __name__ == "__main__":
    call_me_maybe()