from src.input_checking import input_checking
from json import JSONDecodeError
from pydantic import ValidationError
from colorama import Fore, Back  # type: ignore[import-untyped]
from src.encoding import stage_encoding
from llm_sdk import Small_LLM_Model
from src.classes import FunctionDefinitionValidation, InputFileValidation
from torch import Tensor


def call_me_maybe() -> None:
    json_contents: tuple[list[FunctionDefinitionValidation],
                         list[InputFileValidation]]
    functions_definition_list: list[FunctionDefinitionValidation]
    input_prompts_list: list[InputFileValidation]
    llm: Small_LLM_Model
    encoded_tokens: Tensor

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
        print(Back.BLUE +
              f"Processing prompt number {prompt_nbr + 1}..." + Back.RESET)
        print(Fore.LIGHTBLUE_EX + "Encoding... ->", end=" ")
        encoded_tokens = stage_encoding(functions_definition_list, prompt, llm)
        print(Fore.GREEN + "Encoding complete" + Fore.WHITE)
        print(Fore.LIGHTBLUE_EX + "Being fed to the model... ->", end=" ")
        print(Fore.GREEN + "Model was successfully fed")
        print(Fore.LIGHTBLUE_EX + "Processing logits... ->", end=" ")
        print(Fore.GREEN + "Logits successfully processed")
        print(Fore.LIGHTBLUE_EX + "Decoding...", end=" ")
        print(Fore.GREEN + "Successfully decoded")
        print(Fore.LIGHTBLUE_EX + "Being added to the output file... ->",
              end=" ")
        print(Fore.GREEN + "Successfully added to the output file" +
              Fore.WHITE)
    print(encoded_tokens)
    print(Fore.LIGHTBLUE_EX +
          "\nAll prompts have been processed. Please check the output file")


if __name__ == "__main__":
    call_me_maybe()
