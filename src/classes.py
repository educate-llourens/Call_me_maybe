from pydantic import BaseModel, ValidationError, model_validator
from typing import Any
from enum import Enum


class ParsingError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"Parsing Error: {msg}")


class EncodingError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"Encoding Error: {msg}")


class FunctionDefinitionValidation(BaseModel):
    name: str
    description: str
    parameters: dict[str, dict[str, str]]
    returns: dict[str, str]

    @model_validator(mode="after")
    def parameter_validation(self) -> FunctionDefinitionValidation:
        for key in self.parameters.keys():
            if 'type' not in self.parameters[key]:
                raise ValidationError("Cannot find the parameter "
                                      f"type for {key}")
        return self


class InputFileValidation(BaseModel):
    prompt: str
