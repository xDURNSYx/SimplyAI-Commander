# SimplyAI-Commander
Voice-activated autonomous app builder and deployer that makes decisions and performs actions based on user intent.

## Requirements

- Python 3.9+
- A valid `OPENAI_API_KEY` environment variable for the OpenAI SDK
- Network access to the remote executor service at `http://3.134.181.62:5000`

Install dependencies:

```bash
pip install openai requests
```

## Usage

```bash
python orchestrator.py
```

1. Provide a high-level instruction when prompted.
2. The orchestrator will request a shell command from OpenAI's `gpt-4o-mini`.
3. If the suggested command appears risky (e.g., destructive patterns or multiline), you will be asked to confirm it before execution.
4. Once confirmed, the command is dispatched to the remote executor and the result is printed when available.

### Troubleshooting

- **Missing API key** – Ensure `OPENAI_API_KEY` is exported in your shell.
- **Timeouts** – The orchestrator waits up to 5 minutes for a response from the remote executor. Check network connectivity or the remote service if you see timeout errors.
- **Unexpected commands** – Decline the confirmation prompt and re-run the tool with a clarified instruction.
