# 🔐 PassManager

A secure, web-based password manager that stores all your passwords in one encrypted vault on your own computer. No cloud. No database. No tracking.

**One master password. Unlimited accounts. Total privacy.**

---

## 📖 What is PassManager?

PassManager is a self-hosted password manager that runs entirely on your own machine. Unlike cloud-based managers, your passwords never leave your computer.

You remember **one master password**. PassManager remembers the rest.

**Why use it?**
- Encrypted with AES-256-GCM + Argon2id (same standard as banks)
- No cloud, no database — just one encrypted file on disk
- Runs in your browser — works on laptop, phone, tablet
- 10 hacker-style color themes
- Keyboard navigation with numbers and arrows

---

## ✨ Features

**Core:**
- Master password authentication
- Add, edit, delete password entries (4 fields: Username, URL, Password, Notes)
- Copy password to clipboard (auto-clears in 20 seconds)
- Password generator (strong random passwords)
- Password strength meter
- Auto-lock after 5 minutes inactivity

**Advanced:**
- Password health check (weak / reused / old)
- Import from JSON, CSV, Excel
- Export to JSON, CSV, Excel
- Audit log (every action recorded)
- Automatic encrypted backups (last 10 kept)
- Brute-force protection (5 failed attempts → 5-minute lockout)
- Search entries by username, URL, or notes

**UI:**
- 10 horror/hacker color themes
- Dark & Light mode toggle
- Animated 3D background
- Lion intro animation (5 seconds, shows once per session)
- Keyboard shortcuts (1-9, arrows, Enter, Esc, C, N)
- Mobile responsive

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python + Flask + Flask-CORS |
| Frontend Server | Node.js + Express |
| Encryption | cryptography (AES-256-GCM), argon2-cffi |
| UI | HTML5 + CSS3 + Vanilla JavaScript |
| 3D Engine | Three.js |
| Storage | Encrypted JSON file (no database) |

---

## 📋 Requirements

You need these installed on your computer before running PassManager:

### 1. Miniconda (for Python)

Download: https://docs.conda.io/en/latest/miniconda.html

Install with default settings. Minimum Python version: 3.9

Verify it works — open terminal and type:
```
conda --version
python --version
```

You should see version numbers. If `conda` command not found, use **Anaconda Prompt** (Windows) instead of regular terminal.

### 2. Node.js

Download: https://nodejs.org/ (LTS version recommended)

Install with default settings. Minimum version: Node.js 16

Verify it works — open terminal and type:
```
node --version
npm --version
```

You should see version numbers.

### 3. Internet Connection

Only needed for the **first-time setup**. After that, PassManager works fully offline.

**Supported OS:** Windows 10/11, macOS 10.15+, Linux (Ubuntu, Debian, Fedora)

---

## 🚀 Installation & Setup

Follow these steps **one time only**:

### Step 1: Get the Project Folder

Copy the `passmanager` folder to your computer (e.g., `Desktop/passmanager`).

### Step 2: Open Terminal in Project Folder

**Windows:**
```
cd path\to\passmanager
```

**macOS / Linux:**
```
cd ~/Desktop/passmanager
```

**Verify you're in the right place** — type `dir` (Windows) or `ls` (Mac/Linux). You should see:
```
app.py
index.html
package.json
requirements.txt
server.js
start.py
stop.py
README.md
```

### Step 3: Activate Python Environment

```
conda activate base
```

Your terminal prompt should now show `(base)` at the beginning.

### Step 4: Run the Launcher

```
python start.py
```

**First-time run does everything automatically:**
1. Installs Python packages (Flask, cryptography, argon2-cffi, openpyxl)
2. Installs Node.js packages (Express, http-proxy-middleware)
3. Starts Flask backend (port 5000)
4. Starts Node.js frontend (port 4747)
5. Opens your browser

**Wait 1-2 minutes on first run.** After that, everything is fast.

### Step 5: Create Master Password

When browser opens:
1. Enter a **strong master password** (e.g., `MyStr0ng!Pass2024`)
2. Confirm it
3. Click **Create Vault**

⚠️ **Never forget this password!** There is no recovery option — by design, for security.

---

## ▶️ How to Use

### Daily Workflow

| Task | What to Do |
|------|------------|
| Open app | Open browser → `http://localhost:4747` |
| Unlock | Enter master password |
| Add password | Click **➕ Add Entry** |
| Copy password | Click **📋** on any entry |
| Generate password | Click **🎲 Generator** |
| Search | Type in the search bar |
| Lock vault | Click **🔒** in header |
| View health report | Click **⚠️ Weak Passwords** card |

### Add New Entry

When you click **➕ Add Entry**, you fill 4 fields:
1. **Username / Email**
2. **URL**
3. **Password** (with 🎲 Generate button)
4. **Notes**

Click **Add Entry** to save. That's it.

### Access from Phone / Other Devices

1. Make sure phone is on **same WiFi** as computer
2. Look at the **Network URL** printed in terminal (e.g., `http://192.168.1.105:4747`)
3. Open that URL in phone's browser
4. Login with same master password

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `1` - `9` | Open entry #1-9 detail page |
| `↑` / `↓` | Navigate between entries |
| `Enter` | Open selected entry |
| `Esc` | Close modal / deselect |
| `C` | Copy selected entry's password |
| `N` | New entry form |

### Color Themes

Click **🎨** button in header to switch between 10 color schemes:
Blood Red, Toxic Green, Phantom Purple, Midnight Blue, Demon Orange, Witch Cyan, Vampire Crimson, Ghost White, Hellfire, Void Magenta.

Your choice is saved automatically.

### Lock / Unlock

- Vault auto-locks after **5 minutes** of inactivity
- Click **🔒** in header to lock manually
- Re-enter master password to unlock

---

## 🔄 Managing Servers (start.py & stop.py)

PassManager runs two servers in the background. Here's how to control them:

### Starting Servers

```
python start.py
```

**What happens:**
- If servers are **already running**: just opens browser (fast)
- If servers are **not running**: starts them (takes a few seconds)

### Stopping Servers

```
python stop.py
```

Stops both Flask and Node servers and cleans up background processes.

### Do Servers Run After Terminal Close?

**Yes!** Servers run detached from terminal. You can:
- ✅ Close the terminal — servers keep running
- ✅ Sleep your laptop — servers resume after wake
- ❌ Shutdown / Restart laptop — servers stop (run `start.py` again)

### Recommended Daily Flow

**Morning:** Just open browser → `http://localhost:4747`

**If browser says "Backend offline":** Run `python start.py` once

**End of day (optional):** `python stop.py` to save resources

**Computer restart:** Run `python start.py` after login

---

## 📁 Project Structure

```
passmanager/
├── app.py               # Python Flask backend
├── server.js            # Node.js frontend server
├── package.json         # Node.js config
├── index.html           # Complete web UI
├── requirements.txt     # Python dependencies
├── start.py             # One-click launcher
├── stop.py              # Stop background servers
├── README.md            # This file
│
├── vault.json           # 🔐 Your encrypted vault (auto-created)
├── backups/             # 📦 Encrypted backups (auto-created)
├── audit.log            # 📋 Security log (auto-created)
└── node_modules/        # Node packages (auto-created)
```

### What Each File Does

| File | Purpose |
|------|---------|
| `app.py` | Handles encryption, decryption, and all API endpoints |
| `server.js` | Serves `index.html` and proxies API to Flask |
| `package.json` | Node.js dependencies list |
| `index.html` | The entire web UI — login, dashboard, modals |
| `requirements.txt` | Python packages list |
| `start.py` | One command to launch everything |
| `stop.py` | Stops servers cleanly |

---

## ⚙️ How It Works

### Architecture

```
Browser (http://localhost:4747)
      ↓
Node.js Server (port 4747)
      ↓ /api requests
Flask Backend (port 5000)
      ↓
vault.json (encrypted file on disk)
```

### Encryption Flow

1. You enter master password
2. **Argon2id** derives a 32-byte key (with random salt)
3. Vault file is decrypted with **AES-256-GCM**
4. If successful → vault unlocked → data shown in UI
5. Every change re-encrypts and saves immediately

### What's Inside vault.json

```
{
  "version": 1,
  "kdf": "argon2id",
  "salt": "...",
  "nonce": "...",
  "ciphertext": "...",
  "checksum": "...",
  "created": "...",
  "modified": "..."
}
```

Your actual passwords are inside `ciphertext` — completely unreadable without your master password.

---

## 🔒 Security

### Encryption Details

| Feature | Implementation |
|---------|----------------|
| Key Derivation | Argon2id (64MB memory, 3 iterations) |
| Encryption | AES-256-GCM (authenticated) |
| Salt | 16 random bytes per vault |
| Nonce | 12 fresh bytes per save |
| Integrity | SHA-256 checksum |
| Atomic Writes | Temp file + rename (no corruption) |

### Protection Features

- **Brute-force protection** — 5 failed attempts → 5-minute lockout
- **Auto-lock** — 5 minutes of inactivity
- **Clipboard auto-clear** — 20 seconds after copy
- **Audit log** — every action recorded with timestamp
- **Encrypted backups** — last 10 backups kept automatically

### Best Practices

**Do:**
- Use a strong master password (12+ characters, mixed)
- Back up `vault.json` to USB or encrypted cloud regularly
- Only use on trusted networks (home, office)

**Don't:**
- Don't use on public WiFi
- Don't share your master password

---

## 🛠️ Troubleshooting

### conda: command not found
Use **Anaconda Prompt** (Windows) or add Miniconda to your system PATH.

### npm: command not found
Install Node.js from https://nodejs.org/

### Port 4747 already in use
Another app is using the port. Either:

**Option 1 — Change port:** open `server.js`, `start.py`, `stop.py` and replace `4747` with `5555` (or any free port)

**Option 2 — Kill the process using that port:**

Windows:
```
netstat -ano | findstr :4747
taskkill /F /PID <the_PID_number>
```

Linux / Mac:
```
lsof -i :4747
kill -9 <the_PID_number>
```

### "Backend offline" in browser
Flask backend not running. Fix:
```
python stop.py
python start.py
```

### Can't access from phone
1. Make sure phone is on same WiFi as computer
2. Allow port in Windows Firewall (run PowerShell as admin):
```
New-NetFirewallRule -DisplayName "PassManager" -Direction Inbound -Protocol TCP -LocalPort 4747 -Action Allow
```
3. Use Network URL (not localhost) — check terminal output

### Forgot master password
Unfortunately, there is **no recovery**. This is by design, for security.
- If you have a backup and remember its password, restore it
- Otherwise, delete `vault.json` and start fresh

### Vault file corrupted
Restore from the `backups/` folder:
```
copy backups\vault_LATEST.json vault.json
```

---

## ❓ FAQ

**Is this safe to use?**
Yes, if you use a strong master password and keep backups. The encryption (AES-256-GCM + Argon2id) is the same standard used by banks.

**Do I need internet?**
Only for the first-time setup. After that, it works fully offline.

**Can I use it on multiple devices?**
Yes, on the same WiFi network. For remote access, use port forwarding or a VPN.

**Where is my data stored?**
In `vault.json` in the project folder — encrypted. Nothing leaves your computer.

**What if I forget my master password?**
You lose access. No recovery possible. Keep backups and remember your password!

**Is there a mobile app?**
No native app, but the web UI works great on mobile browsers over same WiFi.

**How many passwords can I store?**
Unlimited. The vault file grows only slightly with each entry.

---

## 📜 License

MIT License

Copyright (c) 2026 PassManager

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

**Made with 🔐 for people who value privacy.**