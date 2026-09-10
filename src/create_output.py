from json import dump
from pathlib import Path
from colorama import Fore, Back
from src.classes import InputFileValidation


def create_function_output_dict(
    function_name: str, parameters_dict: dict, prompt: InputFileValidation
) -> dict:
    """Creates the correct dictionary structure for the processed prompt

    Args:
        function_name (str): Name of the function to call
        parameters_dict (dict): The dictionary of parameters
        prompt (InputFileValidation): The prompt that was processed

    Returns:
        dict: The correctly filled out dict for the output of the
        processed prompt
    """
    function_dict: dict = {
        "prompt": prompt.prompt,
        "name": function_name,
        "parameters": parameters_dict
    }
    return function_dict


def create_output_file(output_function_list: list[dict],
                       output_file_path: Path) -> None:
    """Created the directories and the output file with the correct json

    Args:
        output_function_list (list[dict]): The list of output dictionaries
        output_file_path (Path): The file path to create the output file

    Raises:
        FileExistsError: If there is an issue with the path and it cannot
        create the file, therefore cannot be read, it will throw this error.
    """
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
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
