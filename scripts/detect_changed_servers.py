#!/usr/bin/env python3
import subprocess
from pathlib import Path

REPO_ROOT = Path.cwd()

result = subprocess.run(
    ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
    capture_output=True, text=True
)

changed_servers = set()
for file in result.stdout.strip().split("\n"):
    parts = Path(file).parts
    if len(parts) > 1:
        folder = REPO_ROOT / parts[0]
        if folder.is_dir() and (folder / "AGENTS.md").exists():
            changed_servers.add(parts[0])

for server in sorted(changed_servers):
    print(server)
