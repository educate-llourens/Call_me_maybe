from json import dump
from pathlib import Path
from colorama import Fore, Back


def create_function_output_dict(
    function_name: str, parameters_dict: dict, prompt: InputFileValidation
) -> dict:
    function_dict: dict = {
        "prompt": prompt.prompt,
        "name": function_name,
        "parameters": parameters_dict
    }
    return function_dict


def create_output_file(output_function_list: list[dict],
                       output_file_path: Path) -> None:
    output_file_path.parent.mkdir(parents=True, exist_ok=True)   # .parent added
    print(Fore.LIGHTBLUE_EX +
          "Creating output file... " +
          Fore.RESET, end="")
    try:
        with open(output_file_path, "w") as output_file:
            dump(output_function_list, output_file, indent=4)
            print(Back.GREEN +
                  "File successfully created" +
                  Back.RESET)
    except FileExistsError as msg:
        raise FileExistsError(f"File not created | {msg}")
