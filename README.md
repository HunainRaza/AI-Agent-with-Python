# AI Agent with Python 🤖

A custom, autonomous AI agent built using Python and the newly released `google-genai` SDK. This agent features a continuous reasoning loop and tool-calling capabilities, allowing the LLM to autonomously interact with the local file system and execute code based on user prompts.

## ✨ Features

- **Continuous Agent Loop:** The agent can reason, call tools, analyze the output, and continue working until the user's request is fully resolved.
- **File System Interaction:** Safely list directory contents, read file contents, and write/overwrite files within a protected working directory.
- **Python Execution:** The agent can execute Python scripts (`.py` files) with optional command-line arguments and read the `stdout` and `stderr` outputs.
- **Built with `uv`:** Uses the fast `uv` package manager for isolated and reproducible virtual environments.

## 🛠️ Prerequisites

- Python 3.12+
- [`uv` package manager](https://docs.astral.sh/uv/)
- A Gemini API Key from Google AI Studio

## 🚀 Installation & Setup

1. **Clone the repository:**
```bash
   git clone <your-repo-url>
   cd AI-Agent-with-Python
```

2. **Set up the environment:**
Ensure your packages are synced using uv:
```bash
   uv sync
```

3. **Configure Environment Variables:**
Create a .env file in the root directory (ensure this is in your .gitignore!) and add your API key:
```Code snippet
   GEMINI_API_KEY=your_api_key_here
```

## 💻 Usage
Run the agent from your terminal by passing a prompt as an argument. You can also use the --verbose flag to see the agent's internal thought process and tool calls!
Standard Run:
```bash
   uv run main.py "how does the calculator app work?"
```

Verbose Run (See the Agent Loop in action):
```bash
   uv run main.py "run the tests for the calculator app" --verbose
```

## 📂 Project Structure
- `main.py`: The entry point containing the agent loop and CLI setup.

- `prompts.py`: Contains the system instructions that guide the agent's behavior.

 - `functions/`: Directory containing all the tools the LLM can use:

   - `call_function.py`: The router that matches LLM requests to actual Python functions.

   - `get_files_info.py`: Tool for listing directories.

   - `get_file_content.py`: Tool for reading files.

   - `write_file_content.py`: Tool for writing files.

   - `run_python_file.py`: Tool for executing Python scripts.

- `calculator/:` A sample directory containing a dummy app for the agent to interact with.

## How It Works

- **Agent Loop:** The entrypoint `main.py` runs a loop that sends the user prompt to a Gemini model, examines the model's response, executes any requested tool calls (functions), injects the tool outputs back into the conversation, and continues until a final response is produced or a maximum iteration limit is reached.
- **Tools:** The agent exposes sandboxed tools in `functions/` that allow safe file listing, file reading, file writing, and executing Python scripts inside a protected working directory (`./calculator` by default).

## Tools (available under `functions/`)

- **`get_files_info`**: List files in a directory with file sizes and whether items are directories. See [functions/get_files_info.py](functions/get_files_info.py#L1).
- **`get_file_content`**: Read a file (safely truncated at 10,000 characters). See [functions/get_file_content.py](functions/get_file_content.py#L1).
- **`run_python_file`**: Execute a Python script with optional command-line arguments and capture `stdout`/`stderr`. See [functions/run_python_file.py](functions/run_python_file.py#L1).
- **`write_file`**: Write or overwrite a file under the working directory (creates parents if needed). See [functions/write_file_content.py](functions/write_file_content.py#L1).

## Configuration

- Create a `.env` file in the project root with your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

- The agent expects `GEMINI_API_KEY` to be present. If it is missing, `main.py` will raise an error.

## Usage

- Run the agent with a prompt:

```bash
uv run main.py "how does the calculator app work?"
```

- Show verbose output (internal thoughts, tool calls):

```bash
uv run main.py "run the tests for the calculator app" --verbose
```

## Examples & Quick Checks

- Run the sample calculator app directly:

```bash
python calculator/main.py "3 + 5"
```

- Run the small quick script that demonstrates arithmetic:

```bash
python calculator/calculate.py
```

## Running the included tests

This repository includes small standalone test scripts (not `pytest`-based) that demonstrate the behavior of the utilities. Run them with plain Python:

```bash
python test_get_file_content.py
python test_get_files_info.py
python test_run_python_file.py
python test_write_file.py
python test_function_calls.py
```

Note: The functions operate relative to a secure working directory (by default `calculator`) which prevents reading or writing files outside that folder.

## Security and Safety

- All tool calls in `functions/` validate that requested paths are inside the configured `working_directory` to avoid arbitrary file system access.
- `get_file_content` truncates large files to avoid returning excessive data to the model.
- `run_python_file` restricts execution to `.py` files and runs them with a 30s timeout.

## Development

- Sync dependencies with `uv` (if using the recommended environment):

```bash
uv sync
```

- To run the agent locally without `uv`, ensure your Python environment has the required packages from `pyproject.toml`, and run:

```bash
python main.py "your prompt here"
```

## Files to Inspect

- `main.py` — agent loop and CLI
- `prompts.py` — system instructions used as the agent's system prompt
- `functions/` — tool implementations the model can call
- `calculator/` — sample app and demo working directory

---
## ⚠️ Disclaimer & Warning:
This AI agent is capable of executing arbitrary Python code and modifying files on your local machine. It does not run in a sandboxed environment. Do not run this agent in a directory containing sensitive files or important system data. The creator assumes no liability for any data loss, system damage, or unintended consequences resulting from the use of this software. Use strictly at your own risk in an isolated environment.