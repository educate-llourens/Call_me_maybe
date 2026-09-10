from src.input_checking import input_checking
from json import JSONDecodeError
from pydantic import ValidationError
from colorama import Fore, Back
from time import perf_counter
from pathlib import Path
from src.function_name_generation import function_name_process
from src.parameters_generation import parameters_process
from src.create_output import create_function_output_dict, create_output_file
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
                         list[InputFileValidation], Path]
    output_function_list: list[dict] = []

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
    print("")
    # Start process -----------------------------------------------------------
    start_time = perf_counter()
    function_definitions, prompts_list, output_file_path = json_contents
    try:
        i = 1
        for prompt in prompts_list:
            print(Fore.LIGHTMAGENTA_EX + f"Prompt {i}: " + Fore.RESET)
            print(Fore.LIGHTBLUE_EX + "Fetching function name..." + Fore.RESET)
            function_name: str = function_name_process(
                llm, function_definitions, prompt)
            print(Back.LIGHTGREEN_EX + "Function name:" + Back.RESET +
                  f" {function_name}")
            print("")
            print(Fore.LIGHTBLUE_EX + "Fetching parameters..." + Fore.RESET)
            parameters_dict: dict = parameters_process(
                llm, function_definitions, function_name, prompt)
            i += 1
            print("")
            function_output_dict: dict = create_function_output_dict(
                function_name, parameters_dict, prompt)
            output_function_list.append(function_output_dict)
    except (EncodingError, ProcessingError, DecodingError,
            OutputFileError) as msg:
        print(Fore.RED + f"{str(msg)}" + Fore.RESET)
    try:
        create_output_file(output_function_list, output_file_path)
    except (OutputFileError, FileExistsError) as msg:
        print(Fore.RED + f"{str(msg)}" + Fore.RESET)
    end_time = perf_counter()
    print(Fore.LIGHTBLUE_EX + "All prompts processed in "
          f"{(end_time - start_time) / 60:.2f} minutes. "
          "Please check the data/output folder" + Fore.RESET)

    # Debug printing ----------------------------------------------------------


if __name__ == "__main__":
    call_me_maybe()
