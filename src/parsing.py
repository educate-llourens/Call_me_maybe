from argparse import ArgumentParser, Namespace
from pathlib import Path
from .classes import (ParsingError, FunctionCallingValidator,
                      FunctionsDefinitionValidator)
from json import load as json_load, JSONDecodeError
from typing import Any


def parsing() -> tuple[Any, Any]:
    args_file_list: list[Path] = []
    parser: ArgumentParser
    args: Namespace
    # fn_definitions_valid: list[Any] = []
    # fn_calling_tests_valid: list[Any] = []

    # To do: Check out type.path instead of this long as way around
    parser = ArgumentParser()
    parser.add_argument("--functions_definition",
                        default="data/input/functions_definition.json")
    parser.add_argument("--input",
                        default="data/input/function_calling_tests.json")
    parser.add_argument("--output",
                        default="data/output/function_calls.json")
    args = parser.parse_args()
    args_file_list.append(Path(args.functions_definition))
    args_file_list.append(Path(args.input))
    for path in args_file_list:
        if path.exists() is False:
            raise ParsingError("Functions definitions file does not exist")
    try:
        with open(args_file_list[0], "r") as file:
            fn_definitions_valid = (
                FunctionsDefinitionValidator(**(json_load(file))))
        with open(args_file_list[1], "r") as file:
            fn_calling_tests_valid = (
                FunctionCallingValidator(**(json_load(file))))
    except (FileExistsError, PermissionError, JSONDecodeError) as msg:
        raise ParsingError(str(msg))
    return (fn_definitions_valid, fn_calling_tests_valid)
