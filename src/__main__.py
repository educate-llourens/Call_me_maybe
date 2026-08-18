from src.input_checking import input_checking
from json import JSONDecodeError
from pydantic import ValidationError
from colorama import Fore
from src.encoding import function_name_encoding
from src.generation import generation
from src.decoding import decoding_function_name
from src.classes import (FunctionDefinitionValidation, InputFileValidation,
                         EncodingError, ProcessingError, DecodingError,
                         OutputFileError)
try:
    print(Fore.LIGHTBLUE_EX + "Starting LLM... ->" + Fore.RESET, end=" ")
    from llm_sdk import Small_LLM_Model
    print(Fore.GREEN + "LLM successfully started up" + Fore.LIGHTYELLOW_EX)
except ImportError as msg:
    print(Fore.RED + f"ImportError: {str(msg)}")


def call_me_maybe() -> None:
    """Delegates input checking, encoding, decoding and output file processes.
    It also manages the visualisation of the program's functions.
    """
    json_contents: tuple[list[FunctionDefinitionValidation],
                         list[InputFileValidation]]

    # Starting LLM ------------------------------------------------------------
    llm: Small_LLM_Model = Small_LLM_Model()
    if not llm:
        print(Fore.LIGHTBLUE_EX + "Initialising llm... ->" + Fore.RESET,
              end=" ")
        print(Fore.RED + "LLM Error: Could not initialise LLM")
        return
    else:
        print(Fore.LIGHTBLUE_EX + "Initialising llm... ->" + Fore.RESET,
              end=" ")
        print(Fore.GREEN + "LLM successfully initialised")

    # Check input -------------------------------------------------------------
    print(Fore.LIGHTBLUE_EX + "Checking input... ->", end=" ")
    try:
        json_contents = input_checking()
        print(Fore.GREEN + "Input verified" + Fore.YELLOW)
    except (FileExistsError, FileNotFoundError, JSONDecodeError,
            ValidationError, KeyError) as msg:
        print(Fore.RED + str(msg))
        return
    # TODO: Create loop going through list of tests
    # Start process -----------------------------------------------------------
    try:
        process_prompt_loop(json_contents, llm)
    except (EncodingError, ProcessingError, DecodingError,
            OutputFileError) as msg:
        print(Fore.RED + f"{str(msg)}" + Fore.RESET)
    print(Fore.LIGHTBLUE_EX + "All prompts processed. Please check the "
          "data/output folder" + Fore.RESET)

    # Debug printing ----------------------------------------------------------


def process_prompt_loop(
    json_contents: tuple[list[FunctionDefinitionValidation],
                         list[InputFileValidation]], llm: Small_LLM_Model
) -> None:
    # Encoding function name --------------------------------------------------
    print(Fore.LIGHTBLUE_EX + "Encoding function name... ->", end=" ")
    encoded_tokens: list[int] = (
        function_name_encoding(json_contents[0], json_contents[1][0], llm)
    )
    if encoded_tokens is not None:
        print(Fore.GREEN + "Successfully encoded function name" + Fore.RESET)
    else:
        raise EncodingError("Encoding function name failed")
    # Processing function name ------------------------------------------------
    print(Fore.LIGHTBLUE_EX + "Generating function logits... ->", end=" ")
    function_name_logits: list[int] = generation(llm, encoded_tokens)
    if function_name_logits:
        print(Fore.GREEN + "Function logits created" + Fore.RESET)
    else:
        raise ProcessingError("Function logits is empty")
    # Decoding function name --------------------------------------------------
    print(Fore.LIGHTBLUE_EX + "Decoding Function name... ->" + Fore.RESET,
          end=" ")
    function_name: str = decoding_function_name(function_name_logits, llm)
    if function_name != "" and function_name is not None:
        print(Fore.GREEN + "Successfully retrieved function name: "
              f"{function_name}")
    else:
        print(Fore.RED + "Could not retrieve function name" + Fore.RESET)
    # Debug printing ----------------------------------------------------------
    print(function_name, function_name_logits)


if __name__ == "__main__":
    call_me_maybe()
