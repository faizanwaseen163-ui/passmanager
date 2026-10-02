#!/usr/bin/env python3
"""PassManager — Stop background servers"""
import os, sys, subprocess, time, socket
from pathlib import Path

BASE = Path(__file__).parent.resolve()
IS_WIN = sys.platform.startswith("win")

FLASK_PID = BASE / ".flask.pid"
NODE_PID  = BASE / ".node.pid"

def is_port_open(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect(("127.0.0.1", port))
        s.close(); return True
    except Exception:
        return False

def kill_pid(pid):
    try:
        if IS_WIN:
            subprocess.call(["taskkill", "/F", "/PID", str(pid)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            os.kill(pid, 15)
            time.sleep(0.5)
            try: os.kill(pid, 9)
            except: pass
        return True
    except Exception:
        return False

def kill_by_pid_file(pid_file, label):
    if not pid_file.exists():
        print(f"  {label}: no PID file found")
        return
    try:
        pid = int(pid_file.read_text().strip())
    except Exception:
        print(f"  {label}: invalid PID file")
        return
    if kill_pid(pid):
        print(f"  {label}: stopped (PID {pid})")
    else:
        print(f"  {label}: could not stop PID {pid} (may already be dead)")
    try: pid_file.unlink()
    except: pass

def kill_by_port(port, label):
    """Fallback — kill whatever is listening on the port"""
    try:
        if IS_WIN:
            out = subprocess.check_output(
                f'netstat -ano | findstr :{port}',
                shell=True, text=True, stderr=subprocess.DEVNULL
            )
            pids = set()
            for line in out.splitlines():
                parts = line.split()
                if parts and parts[-1].isdigit():
                    pids.add(parts[-1])
            for pid in pids:
                subprocess.call(["taskkill", "/F", "/PID", pid],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if pids:
                print(f"  {label}: killed PIDs {','.join(pids)} on port {port}")
        else:
            subprocess.call(f"lsof -ti:{port} | xargs -r kill -9",
                            shell=True, stderr=subprocess.DEVNULL)
            print(f"  {label}: killed processes on port {port}")
    except Exception as e:
        print(f"  {label}: fallback failed ({e})")

def main():
    print("\n" + "=" * 62)
    print("  PassManager — Stopping Background Servers")
    print("=" * 62)
    kill_by_pid_file(FLASK_PID, "Flask")
    kill_by_pid_file(NODE_PID,  "Node ")
    time.sleep(0.8)
    if is_port_open(5000):
        kill_by_port(5000, "Flask")
    if is_port_open(4747):
        kill_by_port(4747, "Node ")
    time.sleep(0.5)
    print("=" * 62)
    print("  ✅ Done. Servers stopped.")
    print("=" * 62 + "\n")

if __name__ == "__main__":
    main()