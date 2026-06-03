#!/usr/bin/env python3
"""
Reads each mcp-*/AGENTS.md and mcp-*/.codex/skills/ as source of truth.
Writes aggregated output to root AGENTS.md and root .codex/skills/.
"""

import shutil
from pathlib import Path

REPO_ROOT = Path.cwd()
MCP_DIRS = sorted([d for d in REPO_ROOT.iterdir() if d.is_dir() and (d / "AGENTS.md").exists()])


def generate_root_agents_md():
    lines = []
    lines.append("# AGENTS.md\n\n")
    lines.append("> Auto-generated — do not edit manually.\n")
    lines.append("> Source of truth: each `mcp-*/AGENTS.md`.\n\n")
    lines.append("---\n\n")

    for mcp_dir in MCP_DIRS:
        agents_file = mcp_dir / "AGENTS.md"
        if not agents_file.exists():
            continue
        content = agents_file.read_text(encoding="utf-8").strip()
        lines.append(f"## {mcp_dir.name}\n\n")
        lines.append(content)
        lines.append("\n\n---\n\n")

    output = REPO_ROOT / "AGENTS.md"
    output.write_text("".join(lines), encoding="utf-8")
    print(f"Written: {output.relative_to(REPO_ROOT)}")


def sync_codex_skills():
    root_skills = REPO_ROOT / ".codex" / "skills"

    if root_skills.exists():
        shutil.rmtree(root_skills)
    root_skills.mkdir(parents=True)

    for mcp_dir in MCP_DIRS:
        src = mcp_dir / ".codex" / "skills"
        if not src.exists():
            continue
        dest = root_skills / mcp_dir.name
        shutil.copytree(src, dest)
        print(f"Copied: {src.relative_to(REPO_ROOT)} -> {dest.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    generate_root_agents_md()
    sync_codex_skills()
    print("Done.")
