#!/usr/bin/env python3
"""
Start Backend Server — handles platform module conflict
"""

import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
BACKEND_ROOT = PROJECT_ROOT / "ai-news-backend"

os.chdir(BACKEND_ROOT)

env = os.environ.copy()
env["PYTHONPATH"] = str(BACKEND_ROOT)

uvicorn_exe = BACKEND_ROOT / "venv" / "Scripts" / "uvicorn.exe"
if uvicorn_exe.exists():
    cmd = [str(uvicorn_exe), "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
else:
    venv_python = BACKEND_ROOT / "venv" / "Scripts" / "python.exe"
    python_exec = str(venv_python) if venv_python.exists() else sys.executable
    cmd = [python_exec, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

print(f"Starting backend server from {BACKEND_ROOT}")
print(f"Command: {' '.join(cmd)}")

subprocess.run(cmd, env=env)
