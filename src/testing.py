from llm_sdk import Small_LLM_Model


def encoding() -> None:
    """Downloads the model from HuggingFace the first time we get an instance
        of the Small_LLM_Model class
    """
    llm: Small_LLM_Model = Small_LLM_Model(device="cpu")
    result = llm.encode("Hello, what is the world propulation right now?")
    print(result)

if __name__ == "__main__":
    encoding()