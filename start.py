#!/usr/bin/env python3
"""
PassManager — Persistent Background Launcher

USAGE:
    python start.py        → First time: starts servers in background
                             Next time:  just opens browser (servers already running)
    python stop.py         → Stops both servers

Servers keep running even if you close the terminal.
"""
import os, sys, subprocess, time, webbrowser, socket
from pathlib import Path

BASE = Path(__file__).parent.resolve()
IS_WIN = sys.platform.startswith("win")

FLASK_PORT = 5000
NODE_PORT = 4747
FLASK_PID = BASE / ".flask.pid"
NODE_PID = BASE / ".node.pid"
FLASK_LOG = BASE / ".flask.log"
NODE_LOG = BASE / ".node.log"

# ================= HELPERS =================
def is_port_open(port):
    """Check if something is listening on 127.0.0.1:port"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.6)
        s.connect(("127.0.0.1", port))
        s.close()
        return True
    except Exception:
        return False

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

def get_python_exe():
    """On Windows use pythonw.exe for no-console background process"""
    if IS_WIN:
        pyw = Path(sys.executable).parent / "pythonw.exe"
        if pyw.exists():
            return str(pyw)
    return sys.executable

def spawn_detached(cmd, log_file):
    """Start process detached from this terminal — survives terminal close."""
    log = open(log_file, "a", encoding="utf-8", errors="ignore")

    if IS_WIN:
        DETACHED_PROCESS = 0x00000008
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        CREATE_NO_WINDOW = 0x08000000
        flags = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW
        return subprocess.Popen(
            cmd, cwd=BASE, creationflags=flags,
            stdin=subprocess.DEVNULL, stdout=log, stderr=log,
            close_fds=True,
        )
    else:
        return subprocess.Popen(
            cmd, cwd=BASE, start_new_session=True,
            stdin=subprocess.DEVNULL, stdout=log, stderr=log,
            close_fds=True,
        )

def wait_for_port(port, timeout=15):
    """Wait until port is open (or timeout)"""
    start = time.time()
    while time.time() - start < timeout:
        if is_port_open(port):
            return True
        time.sleep(0.4)
    return False

def banner(msg):
    print("\n" + "=" * 62 + f"\n  {msg}\n" + "=" * 62)

# ================= DEP CHECKS =================
def ensure_python_deps():
    missing = []
    for mod in ["flask", "flask_cors", "cryptography", "argon2", "openpyxl"]:
        try: __import__(mod)
        except ImportError: missing.append(mod)
    if missing:
        print(f"[Setup] Installing Python packages: {', '.join(missing)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install",
                               "-r", "requirements.txt", "--quiet"])
    return True

def ensure_node_deps():
    if not (BASE / "node_modules").exists():
        print("[Setup] Installing npm packages (first run only)...")
        r = subprocess.call(["npm", "install", "--silent"], cwd=BASE,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if r != 0:
            print("      ✗ npm install failed. Install Node.js first.")
            return False
    return True

# ================= START SERVERS =================
def start_flask():
    print(f"[Start] Flask backend (port {FLASK_PORT})...")
    py = get_python_exe()
    proc = spawn_detached([py, "app.py"], FLASK_LOG)
    FLASK_PID.write_text(str(proc.pid), encoding="utf-8")
    if wait_for_port(FLASK_PORT, 15):
        print(f"        ✓ Flask running (PID {proc.pid})")
        return True
    print("        ✗ Flask failed to start. Check .flask.log")
    return False

def start_node():
    print(f"[Start] Node frontend (port {NODE_PORT})...")
    node = "node.exe" if IS_WIN else "node"
    proc = spawn_detached([node, "server.js"], NODE_LOG)
    NODE_PID.write_text(str(proc.pid), encoding="utf-8")
    if wait_for_port(NODE_PORT, 15):
        print(f"        ✓ Node running (PID {proc.pid})")
        return True
    print("        ✗ Node failed to start. Check .node.log")
    return False

# ================= MAIN =================
def main():
    banner("PassManager — Background Launcher")

    flask_running = is_port_open(FLASK_PORT)
    node_running  = is_port_open(NODE_PORT)

    if flask_running and node_running:
        print("[Status] ✓ Servers already running in background.")
        print("         (No need to restart — opening browser...)")
    else:
        ensure_node_deps()
        ensure_python_deps()

        if not flask_running:
            if not start_flask():
                print("\n❌ Cannot start Flask. Check .flask.log for details.")
                return
        else:
            print(f"[Status] ✓ Flask already on port {FLASK_PORT}")

        if not node_running:
            if not start_node():
                print("\n❌ Cannot start Node. Check .node.log for details.")
                return
        else:
            print(f"[Status] ✓ Node already on port {NODE_PORT}")

    # Show URLs
    ip = get_local_ip()
    local_url   = f"http://localhost:{NODE_PORT}"
    network_url = f"http://{ip}:{NODE_PORT}"

    print("\n" + "=" * 62)
    print(f"  🌐 Local:   {local_url}")
    print(f"  🌐 Network: {network_url}")
    print("=" * 62)
    print("\n  ✅ Servers are running in the BACKGROUND.")
    print("     You can close this terminal — they will keep running.")
    print(f"\n  📌 Bookmark this URL: {network_url}")
    print("\n  🛑 To stop servers: python stop.py")
    print("=" * 62 + "\n")

    try:
        webbrowser.open(network_url)
    except Exception:
        pass

if __name__ == "__main__":
    main()