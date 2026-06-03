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
        folder = REPO_ROOT / "mcp-servers" / parts[1]  # parts[0] = mcp-servers, parts[1] = server name
        if len(parts) > 2 and parts[0] == "mcp-servers" and folder.is_dir() and (folder / "AGENTS.md").exists():
            changed_servers.add(parts[1])

for server in sorted(changed_servers):
    print(server)
