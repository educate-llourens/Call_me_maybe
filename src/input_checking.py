from argparse import ArgumentParser, Namespace
from pathlib import Path
from json import load
from src.classes import (FunctionDefinitionValidation,
                         InputFileValidation)
from typing import Any


def input_checking() -> tuple[list[Any], list[Any], Path]:
    """Handles argumant flags and checks input is correct

    Returns:
        tuple[list[Any], list[Any], Path]: Returns the list of function
        definitions, list of prompts and the path for the output file.
    """
    parser = ArgumentParser()
    parser.add_argument("--functions_definition",
                        default="data/input/functions_definition.json")
    parser.add_argument("--input",
                        default="data/input/function_calling_tests.json")
    parser.add_argument("--output",
                        default="data/output/function_calls.json")
    args: Namespace = parser.parse_args()
    path_function_def = Path(args.functions_definition)
    path_input_def = Path(args.input)
    with open(path_function_def, "r") as definitions_file:
        definitions_json = load(definitions_file)
        validated_definitions_list = check_definitions_json(definitions_json)
    with open(path_input_def, "r") as input_file:
        input_json: list[dict] = load(input_file)
        validated_input_list = check_input_list(input_json)
    return (validated_definitions_list, validated_input_list,
            Path(args.output))


def check_definitions_json(definitions_json: list[dict]) -> (
                            list[FunctionDefinitionValidation]):
    """Checks the functions definitions are correct

    Args:
        definitions_json (list[dict]): list of function definitions
        as a list of unchecked dicts

    Raises:
        KeyError: Raises a KeyError of the function definition is not
        the correct format.

    Returns:
        list[FunctionDefinitionValidation]: The validated list of
        function definitions
    """
    validated_definition_list: list[FunctionDefinitionValidation] = []

    try:
        for definition in definitions_json:
            validated_definition = FunctionDefinitionValidation(
                name=definition["name"],
                description=definition["description"],
                parameters=definition["parameters"],
                returns=definition["returns"]
            )
            validated_definition_list.append(validated_definition)
    except KeyError as msg:
        raise KeyError("Key Error: In definitions JSON file, "
                       f"{msg} is a missing key")
    return validated_definition_list


def check_input_list(input_json: list[dict]) -> list[InputFileValidation]:
    """Checks the list of prompts

    Args:
        input_json (list[dict]): The list of prompts

    Returns:
        list[InputFileValidation]: The validated list of prompts
    """
    validated_input_list: list[InputFileValidation] = []

    for prompt in input_json:
        validated_input = InputFileValidation(prompt=prompt["prompt"])
        validated_input_list.append(validated_input)
    return validated_input_list
