"""Interactive orchestrator for delegating high-level tasks to a remote executor."""

from __future__ import annotations

import os
import sys
import time
from typing import Iterable

import requests
from openai import OpenAI
from openai import OpenAIError


FLASK_BASE = "http://3.134.181.62:5000"
DEFAULT_TIMEOUT = 10
MAX_RESULT_WAIT_SECONDS = 300


class OrchestratorError(RuntimeError):
    """Base error for orchestrator failures."""


def _ensure_openai_client() -> OpenAI:
    """Return an OpenAI client, validating configuration ahead of time."""

    if not os.getenv("OPENAI_API_KEY"):
        raise OrchestratorError(
            "OPENAI_API_KEY is not set. Please export your API key before running the orchestrator."
        )

    try:
        return OpenAI()
    except OpenAIError as exc:  # pragma: no cover - defensive branch for SDK failures.
        raise OrchestratorError(f"Failed to initialise OpenAI client: {exc}") from exc


def _looks_risky(command: str) -> bool:
    """Heuristic to flag obviously dangerous or malformed commands."""

    red_flags: Iterable[str] = (
        "rm -rf /",
        "shutdown",
        "reboot",
        ":(){ :|:& };:",
        "mkfs",
    )
    if not command or command.strip() == "":
        return True
    if "\n" in command:
        return True
    lowered = command.lower()
    return any(flag in lowered for flag in red_flags)


def _confirm_command(command: str) -> bool:
    """Ask the user for confirmation if the command looks risky."""

    if not _looks_risky(command):
        return True

    print("⚠️  The generated command looks risky or malformed:")
    print(f"   → {command}")
    response = input("Proceed anyway? [y/N]: ").strip().lower()
    return response in {"y", "yes"}


def strategize(prompt: str, client: OpenAI) -> str:
    """Ask the language model for a single shell command."""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a DevOps Strategist: reply with one shell command only.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
    except OpenAIError as exc:
        raise OrchestratorError(f"OpenAI request failed: {exc}") from exc

    try:
        cmd = resp.choices[0].message.content.strip()
    except (AttributeError, IndexError) as exc:
        raise OrchestratorError("OpenAI response was missing a command suggestion.") from exc

    if not cmd:
        raise OrchestratorError("OpenAI returned an empty command suggestion.")

    print(f"[GPTˁ] → {cmd}")
    return cmd


def send_and_get_result(command: str) -> str:
    """Send a command to the remote executor and poll for the result."""

    try:
        response = requests.post(
            f"{FLASK_BASE}/run",
            data={"command": command},
            timeout=DEFAULT_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise OrchestratorError(f"Failed to dispatch command to remote executor: {exc}") from exc

    print("[Orchestrator] Command sent, polling for result…")

    deadline = time.time() + MAX_RESULT_WAIT_SECONDS
    while time.time() < deadline:
        try:
            res = requests.get(f"{FLASK_BASE}/result", timeout=DEFAULT_TIMEOUT)
        except requests.RequestException as exc:
            raise OrchestratorError(f"Error polling for result: {exc}") from exc

        if res.status_code == 200:
            payload = res.text.strip()
            if payload:
                return payload

        time.sleep(1)

    raise OrchestratorError(
        "Timed out waiting for remote executor response. Consider checking the remote service."
    )


def main() -> int:
    """Entry point for the orchestrator CLI."""

    try:
        client = _ensure_openai_client()
    except OrchestratorError as exc:
        print(f"❌ {exc}")
        return 1

    try:
        user_prompt = input("📝 Enter your high-level instruction: ")
    except EOFError:
        print("No instruction provided; exiting.")
        return 0

    if not user_prompt.strip():
        print("Instruction cannot be empty; exiting.")
        return 0

    try:
        shell_cmd = strategize(user_prompt, client)
    except OrchestratorError as exc:
        print(f"❌ {exc}")
        return 1

    if not _confirm_command(shell_cmd):
        print("Aborted at user request.")
        return 0

    try:
        output = send_and_get_result(shell_cmd)
    except OrchestratorError as exc:
        print(f"❌ {exc}")
        return 1

    print("\n📤 Result from EC2:\n" + output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
