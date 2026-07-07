from argparse import ArgumentParser, Namespace
from pathlib import Path
from .classes import ParsingError


def parsing() -> None:
    args_file_list: list[Path] = []
    parser: ArgumentParser
    args: Namespace

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
    args_file_list.append(Path(args.output))
    for path in args_file_list:
        if path.exists() is False:
            raise ParsingError("Functions definitions file does not exist")
    for path in args_file_list:
        try:
            fd = open(path, "r")
            fd.close()
        except (FileExistsError, PermissionError) as msg:
            raise ParsingError(str(msg))
