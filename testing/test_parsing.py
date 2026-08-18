import sys
from pytest import raises, MonkeyPatch
from src.input_checking import input_checking, check_definitions_json
from src.classes import FunctionDefinitionValidation, InputFileValidation


set_definition_list: list[FunctionDefinitionValidation] = [FunctionDefinitionValidation(name='fn_add_numbers', description='Add two numbers together and return their sum.', parameters={'a': {'type': 'number'}, 'b': {'type': 'number'}}, returns={'type': 'number'}), FunctionDefinitionValidation(name='fn_greet', description='Generate a greeting message for a person by name.',parameters={'name': {'type': 'string'}}, returns={'type': 'string'}), FunctionDefinitionValidation(name='fn_reverse_string', description='Reverse a string and return the reversed result.', parameters={'s': {'type': 'string'}}, returns={'type': 'string'}), FunctionDefinitionValidation(name='fn_get_square_root', description='Calculate the square root of a number.', parameters={'a': {'type': 'number'}}, returns={'type': 'number'}), FunctionDefinitionValidation(name='fn_substitute_string_with_regex', description='Replace all occurrences matching a regex pattern in a string.', parameters={'source_string': {'type': 'string'}, 'regex': {'type': 'string'}, 'replacement': {'type': 'string'}}, returns={'type': 'string'})]
set_calling_list: list[InputFileValidation] = [InputFileValidation(prompt='What is the sum of 2 and 3?'), InputFileValidation(prompt='What is the sum of 265 and 345?'), InputFileValidation(prompt='Greet shrek'), InputFileValidation(prompt='Greet john'), InputFileValidation(prompt="Reverse the string 'hello'"), InputFileValidation(prompt="Reverse the string 'world'"), InputFileValidation(prompt='What is the square root of 16?'), InputFileValidation(prompt='Calculate the square root of 144'), InputFileValidation(prompt='Replace all numbers in "Hello 34 I\'m 233 years old" with NUMBERS'), InputFileValidation(prompt="Replace all vowels in 'Programming is fun' with asterisks"),InputFileValidation(prompt="Substitute the word 'cat' with 'dog' in 'The cat sat on the mat with another cat'")]


def test_calling_tests(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["call_me_maybe"])
    na_list, input_test_list = input_checking()
    assert input_test_list == set_calling_list


def test_definitions_list(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["call_me_maybe"])
    definitions_list, na_list = input_checking()
    assert definitions_list == set_definition_list


def test_correct_files(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["call_me_maybe", "--functions_definition", "testing/test_data/test_def_list.json", "--input", "testing/test_data/test_call_tests.json"])
    definitions_list, input_call_list = input_checking()
    assert definitions_list == set_definition_list and input_call_list == set_calling_list

# TODO: File exists but is empty ("" or [])
# TODO: File has malformed JSON (trailing comma, missing bracket)
# TODO: File is valid JSON but wrong shape (e.g. an object {} instead of an array [])
# TODO: Path passed via --input / --functions_definition doesn't exist
# TODO:Duplicate function names in the definitions file
