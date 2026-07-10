"""Add markitdown MCP server block to all Hermes gateway agent config.yaml (idempotent)."""
from __future__ import annotations
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("pyyaml missing", file=sys.stderr)
    sys.exit(1)

AGENT_ROOT = Path(r"C:\DuKickAgent\agents")
# Gateway agents (skip thuno-8773 = Zalo webhook, no hermes gateway)
AGENTS = [
    "dukick-tong-8767",
    "dukick-truyenthong-8768",
    "dukick-pm-8769",
    "dukick-pmcreative-8770",
    "dukick-ketoan-8771",
    "hermes-hr-8772",
    "dukick-huy-8774",
]

SERVER_BLOCK = {
    "command": "C:/DukickAgent/venv/Scripts/python.exe",
    "args": ["C:/DuKickAgent/tools/markitdown_mcp_server.py"],
    "env": {"PYTHONIOENCODING": "utf-8"},
    "timeout": 120,
}

for name in AGENTS:
    cfg_path = AGENT_ROOT / name / "config.yaml"
    if not cfg_path.exists():
        print(f"[skip] {name}: no config.yaml")
        continue
    with open(cfg_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    servers = data.get("mcp_servers") or {}
    if "markitdown" in servers:
        print(f"[ok]   {name}: markitdown already present")
        continue
    servers["markitdown"] = SERVER_BLOCK
    data["mcp_servers"] = servers
    with open(cfg_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
    print(f"[add]  {name}: markitdown mcp_servers added")
print("done")