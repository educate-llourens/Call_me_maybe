from pydantic import BaseModel
from typing import Any


class ParsingError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"Parsing Error: {msg}")


class EncodingError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"Encoding Error: {msg}")


class FunctionCallingValidator(BaseModel):
    prompt: dict


class FunctionsDefinitionValidator(BaseModel):
    name: str
    description: str
    parameters: dict[Any, Any]
