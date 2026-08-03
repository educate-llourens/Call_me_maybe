*This project has been created as part of the 42 curriculum by: lelouren*

# Description

# Algorithm explanation
???
To do: Remove after project submission

# Instructions
1. Clone the repository: <br> 
`git clone https://github.com/educate-llourens/Call_me_maybe.git`

2. Install the necessary packages and dependencies: <br>
`make install`

3. Activate the virtual environment: <br>
`activate .venv/bin/activate`

# Resources
## Documentation
- [Qwen3 Documentation](https://huggingface.co/Qwen/Qwen3-0.6B)
- [Python Documentation](https://docs.python.org/3/library/)
- [Pydantic documentation](https://pydantic.dev/docs/validation/latest/get-started/)
- [argparse tutorial](https://docs.python.org/3/howto/argparse.html#argparse-tutorial)

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
