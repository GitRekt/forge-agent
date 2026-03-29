# Forge

> An autonomous AI coding agent powered by Google Gemini 2.5 Flash

Forge is a command-line AI agent that takes a natural-language task and autonomously plans and executes it — reading files, writing code, and running Python scripts — until the job is done. No hand-holding required.

---

## Features

- **Agentic loop** — runs up to 20 reasoning iterations, chaining tool calls until it produces a final answer
- **Tool use** — backed by four built-in tools: list directory contents, read files, write/overwrite files, and execute Python scripts
- **Google Gemini 2.5 Flash** — fast, capable model with native function-calling support
- **Verbose mode** — optionally inspect every tool call and its response in real time
- **Sandboxed working directory** — all file operations are scoped to a target directory for safety

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Google Gemini 2.5 Flash (`google-genai`) |
| Language | Python 3.9+ |
| Package manager | [uv](https://github.com/astral-sh/uv) |
| Config | `.env` via `python-dotenv` |

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/forge-agent.git
cd forge-agent
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Add your Gemini API key

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your_key_here
```

Get a free key at [aistudio.google.com](https://aistudio.google.com/).

---

## Usage

```bash
uv run main.py "Your task here"
```

**Examples:**

```bash
# Ask it to explain a file
uv run main.py "What does the calculator module do?"

# Ask it to fix a bug
uv run main.py "The tests in calculator/tests.py are failing. Find and fix the bug."

# Ask it to add a feature
uv run main.py "Add a square root function to the calculator package and a test for it."

# Enable verbose output to see every tool call
uv run main.py "Run the tests and summarize the results" --verbose
```

---

## How It Works

```
User prompt
    │
    ▼
Gemini 2.5 Flash  ──── decides what tool to call
    │
    ▼
Tool executor  ──── runs: list_files / read_file / write_file / run_python
    │
    ▼
Result fed back into conversation
    │
    ▼
Repeat (up to 20 iterations) until Gemini returns plain text
    │
    ▼
Final answer printed to stdout
```

Forge uses Gemini's native **function-calling** API. On each iteration, if the model returns a function call instead of text, Forge executes the corresponding tool, appends the result to the conversation, and loops. When the model produces a plain-text response, the loop exits and the answer is displayed.

---

## Project Structure

```
forge-agent/
├── main.py                  # Entry point & agentic loop
├── prompts.py               # System prompt
├── config.py                # Shared constants
├── functions/
│   ├── call_function.py     # Tool dispatcher
│   ├── get_files_info.py    # Tool: list directory
│   ├── get_file_content.py  # Tool: read file
│   ├── write_file.py        # Tool: write file
│   └── run_python_file.py   # Tool: execute Python
└── calculator/              # Sample codebase the agent works on
    ├── main.py
    ├── tests.py
    └── pkg/
        ├── calculator.py
        └── render.py
```

---

## License

MIT
