# AI Agent

A small tool-using coding agent that can inspect files, write files, and run Python files inside the `calculator` working directory.

## Setup

Install the project dependencies with:

```sh
uv sync
```

Set `OPENROUTER_API_KEY` in a local `.env` file, then run the agent with:

```sh
uv run python main.py "What files are in the project?"
```

Add `--verbose` to include tool calls and token usage in the output.

## Tests

Run the calculator unit tests from its directory:

```sh
cd calculator
python3 -m unittest tests.py
```
