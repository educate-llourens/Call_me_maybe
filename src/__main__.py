from src.input_checking import input_checking
from json import JSONDecodeError
from pydantic import ValidationError
from colorama import Fore
from typing import Any
from src.encoding import stage_encoding
from llm_sdk import Small_LLM_Model


def call_me_maybe() -> None:
    json_contents = tuple[list[Any], list[Any]]
    functions_definition_list: list[Any]
    input_prompts_list: list[Any]
    llm: Small_LLM_Model
    encoded_tokens: list[int]

    print(Fore.LIGHTBLUE_EX + "Checking input... ->", end=" ")
    try:
        json_contents = input_checking()
        functions_definition_list, input_prompts_list = json_contents
        print(Fore.GREEN + "Input verified")
    except (FileExistsError, FileNotFoundError, JSONDecodeError,
            ValidationError, KeyError) as msg:
        print(Fore.RED + str(msg))
        return
    print(Fore.LIGHTBLUE_EX + "Starting LLM... ->" + Fore.WHITE)
    llm = Small_LLM_Model()
    for prompt_nbr, prompt in enumerate(input_prompts_list):
        print(Fore.LIGHTBLUE_EX +
              f"Processing prompt number {prompt_nbr + 1}...")
        print(Fore.GREEN + f"Prompt {prompt_nbr + 1}: Encoding...")
        encoded_tokens = stage_encoding(functions_definition_list, prompt, llm)
        print(f"Prompt {prompt_nbr + 1}: Being fed to the model...")
        print(f"Prompt {prompt_nbr + 1}: Processing logits...")
        print(f"Prompt {prompt_nbr + 1}: Decoding...")
        print(f"Prompt {prompt_nbr + 1}: Being added to the output file...")
    print(Fore.LIGHTBLUE_EX +
          "\nAll prompts have been processed. Please check the output file")


if __name__ == "__main__":
    call_me_maybe()
