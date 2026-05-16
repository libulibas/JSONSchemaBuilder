import os, sys
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv()
MODEL = "claude-sonnet-4-20250514"

def claude(prompt, system="", max_tokens=2000):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("Set ANTHROPIC_API_KEY (copy .env.example to .env).")
    c = Anthropic(api_key=key)
    kw = dict(model=MODEL, max_tokens=max_tokens,
              messages=[{"role": "user", "content": prompt}])
    if system:
        kw["system"] = system
    r = c.messages.create(**kw)
    return "".join(b.text for b in r.content if b.type == "text")



import json

def build(description: str) -> str:
    sys_p = ("Output ONLY a valid JSON Schema (draft 2020-12) for the described "
             "structure. No prose.")
    raw = claude(description, system=sys_p)
    raw = raw.strip().strip("`")
    if raw.startswith("json"):
        raw = raw[4:]
    try:
        return json.dumps(json.loads(raw), indent=2)
    except Exception:
        return raw

if __name__ == "__main__":
    d = " ".join(sys.argv[1:]) or \
        "A user with id, email, optional age, and a list of role strings"
    print(build(d))
