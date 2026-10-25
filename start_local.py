"""Convenience script to run both FastAPI backend and Vite frontend concurrently.

Usage:
  python scripts/start_local.py
"""

import subprocess
import sys
import os
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")


def start_services():
    print("=" * 70)
    print("STARTING COLLEGE FAQ CHATBOT (BACKEND + FRONTEND)")
    print("=" * 70)

    # 1. Start backend process
    print("\n[1/2] Starting FastAPI backend on http://127.0.0.1:8000 ...")
    backend_env = os.environ.copy()
    backend_env["PYTHONPATH"] = os.path.join(PROJECT_ROOT, "backend")
    
    backend_cmd = [
        sys.executable,
        "-m", "uvicorn",
        "app.main:app",
        "--app-dir", os.path.join(PROJECT_ROOT, "backend"),
        "--host", "127.0.0.1",
        "--port", "8000",
        "--reload"
    ]

    backend_proc = subprocess.Popen(backend_cmd, env=backend_env)
    time.sleep(2)

    # 2. Start frontend process
    print("\n[2/2] Starting Vite React frontend on http://localhost:5173 ...")
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    frontend_proc = subprocess.Popen([npm_cmd, "run", "dev"], cwd=FRONTEND_DIR)

    print("\n" + "=" * 70)
    print("SUCCESS: Both services are running!")
    print("  - Chat UI:      http://localhost:5173")
    print("  - Admin Portal: http://localhost:5173 (Click 'Admin' or enter token)")
    print("  - API Docs:     http://127.0.0.1:8000/docs")
    print("Press Ctrl+C to stop both services.")
    print("=" * 70)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down backend and frontend...")
        backend_proc.terminate()
        frontend_proc.terminate()
        backend_proc.wait()
        frontend_proc.wait()
        print("Services stopped.")


if __name__ == "__main__":
    start_services()
