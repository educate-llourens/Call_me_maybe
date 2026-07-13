from src.input_checking import input_checking
from src.classes import ParsingError
from typing import Any


def call_me_maybe() -> None:

    try:
        input_checking()
    except (FileExistsError, FileNotFoundError) as msg:
        print(msg)
        return
    # Feed to model
    # Get logits
    # Decoding
    # Format to JSON


if __name__ == "__main__":
    call_me_maybe()
