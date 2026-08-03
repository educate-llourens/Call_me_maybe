from argparse import ArgumentParser, Namespace
from pathlib import Path
from json import load
from src.classes import (FunctionDefinitionValidation,
                         InputFileValidation)
from typing import Any

def input_checking() -> None:
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
        input_json = load(input_file)
        validated_input_list = check_input_list(input_json)
    return (validated_definitions_list, validated_input_list)


def check_definitions_json(definitions_json: Any) -> list[Any]:
    validated_definition_list: list[Any] = []

    for definition in definitions_json:
        validated_definition = FunctionDefinitionValidation(
            name=definition["name"],
            description=definition["description"],
            parameters=definition["parameters"],
            returns=definition["returns"]
        )
        validated_definition_list.append(validated_definition)
    return validated_definition_list


def check_input_list(input_json: Any) -> list[Any]:
    validated_input_list: list[Any] = []

    for prompt in input_json:
        validated_input = InputFileValidation(prompt=prompt["prompt"])
        validated_input_list.append(prompt)
    return validated_input_list

# To do:
# If there is time, check for duplicates