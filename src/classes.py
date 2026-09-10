from pydantic import BaseModel, ValidationError, model_validator


class ParsingError(Exception):
    def __init__(self, msg: str):
        """Tags the error message as part of the parsing section

        Args:
            msg (str): The error message to tag and return
        """
        super().__init__(f"Parsing Error: {msg}")


class EncodingError(Exception):
    def __init__(self, msg: str):
        """Tags the error message as part of the encoding section
        Args:
            msg (str): The error message to tag and return
        """
        super().__init__(f"Encoding Error: {msg}")


class ProcessingError(Exception):
    def __init__(self, msg: str):
        """Tags the error message as part of the processing section

        Args:
            msg (str): The error message to tag and return
        """
        super().__init__(f"Processing Error: {msg}")


class DecodingError(Exception):
    def __init__(self, msg: str):
        """Tags the error message as part of the decoding section

        Args:
            msg (str): The error message to tag and return
        """
        super().__init__(f"Decoding Error: {msg}")


class OutputFileError(Exception):
    def __init__(self, msg: str):
        """Tags the error message as part of the output section

        Args:
            msg (str): The error message to tag and return
        """
        super().__init__(
            f"Output File Error Error: {msg}")


class FunctionDefinitionValidation(BaseModel):
    """Validates the function definitions

    Args:
        BaseModel (_type_): The Base Model

    Raises:
        ValidationError: If the structure of the function definition
        is incorrect

    Returns:
        self: Returns its object
    """
    name: str
    description: str
    parameters: dict[str, dict[str, str]]
    returns: dict[str, str]

    @model_validator(mode="after")
    def parameter_validation(self) -> "FunctionDefinitionValidation":
        for key in self.parameters.keys():
            if 'type' not in self.parameters[key]:
                raise ValidationError("Cannot find the parameter "
                                      f"type for {key}")
        return self


class InputFileValidation(BaseModel):
    """Validates the structure of the prompt

    Args:
        BaseModel (_type_): The Base Model
    """
    prompt: str
