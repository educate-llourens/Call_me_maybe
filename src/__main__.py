from src.input_checking import input_checking
from json import JSONDecodeError
from pydantic import ValidationError
from colorama import Fore


def call_me_maybe() -> None:

    print(Fore.LIGHTBLUE_EX + "Checking input... ->", end=" ")
    try:
        functions_definition_list, input_prompts_list = input_checking()
        print(Fore.GREEN + "Input verified")
    except (FileExistsError, FileNotFoundError, JSONDecodeError,
            ValidationError, KeyError) as msg:
        print(Fore.RED + str(msg))
        return
    for prompt_nbr, prompt in enumerate(input_prompts_list):
        print(Fore.LIGHTBLUE_EX +
              f"Processing prompt number {prompt_nbr + 1}...")
        print(Fore.GREEN + f"Prompt {prompt_nbr + 1}: Encoding...")
        print(f"Prompt {prompt_nbr + 1}: Being fed to the model...")
        print(f"Prompt {prompt_nbr + 1}: Processing logits...")
        print(f"Prompt {prompt_nbr + 1}: Decoding...")
        print(f"Prompt {prompt_nbr + 1}: Being added to the output file...")
    print(Fore.LIGHTBLUE_EX +
          "\nAll prompts have been processed. Please check the output file")


if __name__ == "__main__":
    call_me_maybe()
