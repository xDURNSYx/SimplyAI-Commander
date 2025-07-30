import os
import time
import requests
from openai import OpenAI

client = OpenAI()
FLASK_BASE = os.getenv("FLASK_BASE", "http://3.134.181.62:5000")

def strategize(prompt: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a DevOps Strategist: reply with one shell command only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    cmd = resp.choices[0].message.content.strip()
    print(f"[GPTˁ] → {cmd}")
    return cmd

def send_and_get_result(command: str, timeout: int = 60) -> str:
    try:
        r = requests.post(f"{FLASK_BASE}/run", data={"command": command}, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to send command: {e}") from e

    print("[Orchestrator] Command sent, polling for result…")
    start = time.time()
    while time.time() - start < timeout:
        try:
            res = requests.get(f"{FLASK_BASE}/result", timeout=5)
            if res.status_code == 200 and res.text.strip():
                return res.text.strip()
        except requests.RequestException:
            pass
        time.sleep(1)
    raise TimeoutError("Timed out waiting for command result.")

def main():
    user_prompt = input("📝 Enter your high-level instruction: ")
    shell_cmd = strategize(user_prompt)
    try:
        output = send_and_get_result(shell_cmd)
        print("\n📤 Result from EC2:\n" + output)
    except Exception as err:
        print(f"❌ {err}")

if __name__ == "__main__":
    main()
