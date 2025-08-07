## Streaming Subgraph Demo (LangChain + LangGraph)

This repo contains a minimal example that demonstrates how to preserve token-by-token streaming when calling a LangGraph subgraph. The script contrasts a "broken" pattern vs the exact "updated" pattern that uses `stream_mode="messages"`.

### What's inside
- `new_streaming_example.py`: runnable demo comparing broken vs fixed streaming behavior
- `requirements.txt`: Python dependencies (LangChain, LangGraph, OpenAI SDK, dotenv)

### Prerequisites
- Python 3.10+ recommended
- An OpenAI API key with access to the model used in the script (defaults to `gpt-4o-mini`)

### Setup
1) Create and activate a virtual environment

- macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

- Windows (PowerShell):
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

2) Install dependencies
```bash
pip install -r requirements.txt
```

3) Provide environment variables

The script loads environment variables from a local `.env` file if present. Create a file named `.env` in the repository root with your keys:

```dotenv
# Required
OPENAI_API_KEY=your-openai-api-key

# Optional LangSmith (for tracing/observability)
LANGSMITH_PROJECT=default
LANGSMITH_API_KEY=your-langsmith-api-key
LANGCHAIN_TRACING_V2=true
```

Never commit real secrets. If you're using git, ensure `.env` is ignored.

### Run the demo
```bash
python new_streaming_example.py
```
You should see two sections:
- BROKEN: shows the non-streaming behavior when invoking the subgraph directly
- FIXED: shows chunked streaming when using `stream_mode="messages"`

### Troubleshooting
- "Module not found": Ensure your virtual environment is activated and dependencies are installed.
- No streaming observed in the FIXED path: Confirm your `langgraph` version is >= 0.6.4.
  ```bash
  python -c "import langgraph; print(langgraph.__version__)"
  ```
- Authentication errors: Verify `OPENAI_API_KEY` is set in `.env` or your shell environment and that your key has access to the chosen model.

### Notes
- This example mirrors the fix described by LangGraph maintainers for preserving streaming from subgraphs by explicitly requesting messages streaming: `subgraph.stream(state, stream_mode="messages")`.
