#!/usr/bin/env python3
"""Hook PreToolUse (Bash): registra cada comando en .claude/logs/audit.jsonl."""
import json
import os
import sys
from datetime import datetime

# Claude Code envía los datos del comando por stdin como JSON
data = json.load(sys.stdin)

# Raíz del proyecto: usa la variable de Claude Code o, si falta, el cwd
project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()

# Una sola unión de rutas -> no se duplica ".claude/logs"
log_dir = os.path.join(project_dir, ".claude", "logs")
os.makedirs(log_dir, exist_ok=True)  # crea el directorio si no existe

registro = {
    "ts": datetime.now().astimezone().isoformat(timespec="seconds"),
    "session": data.get("session_id"),
    "cmd": data.get("tool_input", {}).get("command"),
}

# separators=(",", ":") => JSON compacto; una línea por registro (.jsonl)
with open(os.path.join(log_dir, "audit.jsonl"), "a", encoding="utf-8") as f:
    f.write(json.dumps(registro, ensure_ascii=False, separators=(",", ":")) + "\n")
