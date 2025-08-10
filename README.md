# AI Code Assistant

A lightweight AI agent built with Google's Gemini API to explore the fundamentals of agentic AI development. This project demonstrates how to create an autonomous coding assistant that can navigate codebases, read and write files, and execute Python code.

## Purpose

This educational project serves two goals:
1. **Learning objective**: Understand the architecture and implementation of AI agents
2. **Practical application**: Provide an AI assistant that can help debug, modify, and understand Python projects

The agent operates within a sandboxed `calculator` directory, demonstrating safe file system operations while maintaining practical utility.

## Features

- Navigate and list directory contents
- Read and analyze source code files  
- Create and modify files
- Execute Python scripts with arguments
- Sandboxed operations for security

## Setup

1. **Clone the repository**
   ```bash
   git clone git@github.com:carterdea/building-an-ai-agent.git
   cd building-an-ai-agent
   ```

2. **Install dependencies**
   ```bash
   uv sync
   # This will install all dependencies from pyproject.toml
   ```

3. **Set up your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your Gemini API key:
   # GEMINI_API_KEY=your-api-key-here
   ```

## Usage

Run the agent with a natural language prompt:

```bash
# Basic usage
uv run main.py "explain how the calculator renders output"

# Verbose mode for debugging
uv run main.py "fix the calculator tests" --verbose

# Complex tasks
uv run main.py "add a factorial function to the calculator"
```

## How It Works

The agent uses a conversation loop with the Gemini API, where:
1. Your prompt is analyzed to create an execution plan
2. The agent calls appropriate functions (read files, write code, etc.)
3. Results are fed back to continue the conversation
4. The process repeats until the task is complete

## Project Structure

```
├── main.py                # Entry point and conversation loop
├── call_function.py       # Function routing and execution
├── prompts.py             # System prompt configuration
├── config.py              # Application settings
├── functions/             # Available agent capabilities
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python.py
│   └── write_file.py
└── calculator/            # Sandboxed working directory
```

## Security

All file operations are restricted to the `calculator/` directory to prevent unintended system modifications. The agent cannot access or modify files outside this sandbox.

## License

MIT