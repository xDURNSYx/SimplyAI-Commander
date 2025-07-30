# SimplyAI-Commander

SimplyAI-Commander converts natural language instructions into shell commands using OpenAI
and forwards them to a remote Flask server. This repository contains a simple
`orchestrator.py` script that communicates with the server.

## Requirements

- Python 3.8+
- An OpenAI API key
- A running Flask command server (default `http://3.134.181.62:5000`)

Install Python dependencies with:

```bash
pip install -r requirements.txt
```

## Configuration

Set your OpenAI API key in an environment variable `OPENAI_API_KEY`. On Windows,
you can use Command Prompt or PowerShell:

### Command Prompt

```cmd
setx OPENAI_API_KEY "sk-YOUR_OPENAI_API_KEY_HERE"
```

### PowerShell

```powershell
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-YOUR_OPENAI_API_KEY_HERE", "User")
```

(Optional) specify a different Flask server using the `FLASK_BASE` environment variable.

After setting the variable, restart your terminal for the change to take effect.

## Running

Navigate to the project directory and run the orchestrator:

```cmd
cd C:\Users\<USER>\Documents\commanderAI
py strategistAI\orchestrator.py
```

If using PowerShell, call Python explicitly or wrap the ampersand in quotes:

```powershell
& "C:\Users\<USER>\AppData\Local\Programs\Python\Python311\python.exe" strategistAI\orchestrator.py
```

The script will prompt for a high-level instruction, send it to OpenAI, and
relay the resulting command to the Flask server. Results are printed in the
terminal.

## Notes

- Ensure the Flask server is reachable from your machine.
- The default server address can be changed by setting `FLASK_BASE`.
- Use at your own risk; the script executes arbitrary shell commands on the
  server specified.
