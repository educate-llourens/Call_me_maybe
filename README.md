*This project has been created as part of the 42 curriculum by: lelouren*

# Description
A Python-based AI/ML project that introduces us to function calling in Large Language Models (LLMs). We need to build a constrained decoding engine that forces a small local LLM to reliably convert natural language prompts into valid, structured JSON.

# Algorithm explanation

# Instructions
1. Clone the repository: <br> 
`git clone https://github.com/educate-llourens/Call_me_maybe.git`

2. Install the necessary packages and dependencies: <br>
`make install`

3. Activate the virtual environment: <br>
`activate .venv/bin/activate`

4. Ensure that you have your function definitions file and your test prompts file in the data/input folder

5. Start the program with:
```make```

# Resources
## Documentation
- [Qwen3 Documentation](https://huggingface.co/Qwen/Qwen3-0.6B)
- [Python Documentation](https://docs.python.org/3/library/)
- [Pydantic documentation](https://pydantic.dev/docs/validation/latest/get-started/)
- [argparse tutorial](https://docs.python.org/3/howto/argparse.html#argparse-tutorial)

## Other resources
- [Handling JSON data. Here’s how they differ](https://medium.com/@jazeem.lk/handling-json-data-heres-how-they-differ-f3ca223c7851)

## AI Usage
- Creating lessons for parts of the project using scaffolding teaching methods (no code answers)
- Q & A sessions about topics I was not clear on
- Creating quizzes and notes for learning

# Example usage

# Performance analysis 

# Design decisions

# Challenges faced

# Testing strategy
I used unit tests with pytest as far as possible. Thereafter I used the provided testing program (Moulinette). 
## Pytest
| Command                       | What it tests |
| ----------------------------- | -------------- |
| `uv run pytest`               | All tests|
| `uv run pytest -m parsing`    | Only the parsing tests |
| `uv run pytest -m encoding`   | Only the encoding tests |
| `uv run pytest -m decoding`   | Only the decoding tests |
| `uv run pytest -m output`     | Only tests on the output JSON |

## Moulinette

# New Tools
- [Python Formatter Beautifier](https://codebeautify.org/python-formatter-beautifier)
- [colorama - Print coloured text](https://www.geeksforgeeks.org/python/introduction-to-python-colorama/)
