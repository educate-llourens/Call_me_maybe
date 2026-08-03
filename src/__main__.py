from src.input_checking import input_checking
from src.classes import ParsingError
from typing import Any
from json import JSONDecodeError
from pydantic import ValidationError
from colorama import Fore


def call_me_maybe() -> None:

    print(Fore.LIGHTBLUE_EX + "Checking input... ->", end=" ")
    try:
        functions_definition_list, input_prompts_list = input_checking()
        print(Fore.GREEN + "Input verified")
    except (FileExistsError, FileNotFoundError, JSONDecodeError,
            ValidationError) as msg:
        print(Fore.RED + msg)
        return
    print(Fore.LIGHTBLUE_EX + "Encoding... ->", end=" " + Fore.WHITE)
    print(functions_definition_list)
    print("----------------------------")
    print(input_prompts_list)
    # Feed to model
    # Get logits
    # Decoding
    # Format to JSON


if __name__ == "__main__":
    call_me_maybe()
