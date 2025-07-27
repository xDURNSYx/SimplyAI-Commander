import time
import requests
from openai import OpenAI

client = OpenAI()
FLASK_BASE = "http://3.134.181.62:5000"

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

def send_and_get_result(command: str) -> str:
    r = requests.post(f"{FLASK_BASE}/run", data={"command": command})
    r.raise_for_status()
    print("[Orchestrator] Command sent, polling for result…")
    while True:
        res = requests.get(f"{FLASK_BASE}/result")
        if res.status_code == 200 and res.text.strip():
            return res.text.strip()
        time.sleep(1)

def main():
    user_prompt = input("📝 Enter your high-level instruction: ")
    shell_cmd = strategize(user_prompt)
    output = send_and_get_result(shell_cmd)
    print("\n📤 Result from EC2:\n" + output)

if __name__ == "__main__":
    main()
