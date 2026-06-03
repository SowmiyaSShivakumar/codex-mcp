#!/usr/bin/env python3
import os, sys
from pathlib import Path

REPO_ROOT = Path.cwd()
TEMPLATE = REPO_ROOT / "deployment" / "templates" / "aca-template.yaml"
ACA_DIR = REPO_ROOT / "deployment" / "aca"
ENV = os.getenv("DEPLOY_ENV", "dev")
ENV_FILE = REPO_ROOT / "deployment" / "environments" / f"{ENV}.env"

def load_env():
    env = {}
    for line in ENV_FILE.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env

def generate(server_name):
    ACA_DIR.mkdir(parents=True, exist_ok=True)
    template = TEMPLATE.read_text()
    env = load_env()
    config = template
    config = config.replace("{{SERVER_NAME}}", server_name)
    config = config.replace("{{IMAGE_TAG}}", os.getenv("IMAGE_TAG", "latest"))
    for k, v in env.items():
        config = config.replace(f"{{{{{k}}}}}", v)
    out = ACA_DIR / f"{server_name}.yaml"
    out.write_text(config)
    print(f"Generated: {out.name}")

if __name__ == "__main__":
    server = os.getenv("SERVER_NAME") or (sys.argv[1] if len(sys.argv) > 1 else None)
    if not server:
        print("Error: SERVER_NAME not provided")
        sys.exit(1)
    generate(server)
