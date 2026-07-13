from argparse import ArgumentParser, Namespace
from pathlib import Path
from .classes import (ParsingError, FunctionCallingValidator,
                      FunctionsDefinitionValidator)
from json import load as json_load, JSONDecodeError
from typing import Any
from pydantic import ValidationError


def input_checking() -> tuple[Any, Any]:
    parser: ArgumentParser
    args: Namespace
    functions_def_path: Path
    function_calls_path: Path
    fn_definitions: list[dict]
    fn_calls: list[dict]
    validated_fn_definitions: list[FunctionsDefinitionValidator] = []
    validated_fn_calls: list[dict] = []

    parser = ArgumentParser()
    parser.add_argument("--functions_definition",
                        default="data/input/functions_definition.json")
    parser.add_argument("--input",
                        default="data/input/function_calling_tests.json")
    parser.add_argument("--output",
                        default="data/output/function_calls.json")
    args = parser.parse_args()
    functions_def_path = Path(args.functions_definition)
    function_calls_path = Path(args.input)
    if not functions_def_path.exists() or not function_calls_path.exists():
        raise FileExistsError("Functions definitions file does not exist")
    try:
        with open(functions_def_path, "r") as definitions_file:
            fn_definitions = json_load(definitions_file)
            for definition in fn_definitions:
                validated_fn_definitions.\
                    append(FunctionsDefinitionValidator(**definition))
    except (PermissionError, JSONDecodeError) as msg:
        raise ParsingError(str(msg))
    return (validated_fn_definitions, validated_fn_calls)
