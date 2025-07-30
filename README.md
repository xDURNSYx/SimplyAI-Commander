# SimplyAI-Commander

A voice-activated autonomous app builder and deployer that turns high-level user instructions into shell commands executed on a remote EC2 instance.

## Installation

1. Install the Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Export your OpenAI API key so the orchestrator can access the OpenAI service:
   ```bash
   export OPENAI_API_KEY=your-key-here
   ```

## Usage

Run the orchestrator script and provide a high-level instruction when prompted:

```bash
python orchestrator.py
```

Example session:

```
📝 Enter your high-level instruction: Check free disk space
[GPTˁ] → df -h
[Orchestrator] Command sent, polling for result…
📤 Result from EC2:
Filesystem      Size  Used Avail Use% Mounted on
...
```

The script sends your instruction to OpenAI to generate a shell command, executes it remotely, and prints back the output.
