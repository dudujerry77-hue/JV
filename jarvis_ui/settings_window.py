"""Windows desktop Settings window for Jarvis.

Shows how to start Jarvis Core and lets the owner save Groq / Google API
keys into the OS keyring via the local Core HTTP API (D-0011, D-0012).

Run with:
    python -m jarvis_ui.settings_window

Core must already be running for Save to work:
    python -m jarvis_core.service.main
"""

from __future__ import annotations

import json
import tkinter as tk
from tkinter import messagebox, ttk
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

DEFAULT_BASE = "http://127.0.0.1:8756"
TIMEOUT_S = 3

START_INSTRUCTIONS = """How to start Jarvis Core

1. Open PowerShell.
2. Go to your JV project folder:
     cd path\to\JV
3. Install once (first time only):
     pip install -e ".[dev]"
4. Start Core and leave this window open:
     python -m jarvis_core.service.main
5. Open this Settings app in another window:
     python -m jarvis_ui.settings_window

Core listens only on 127.0.0.1:8756 (local machine).
API keys are stored in Windows Credential Manager — never in project files.
"""


def _http_json(method: str, url: str, body: dict | None = None) -> tuple[int, dict | str]:
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=TIMEOUT_S) as resp:
            raw = resp.read().decode("utf-8")
            try:
                return resp.status, json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                return resp.status, raw
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            return exc.code, json.loads(raw) if raw else {"detail": str(exc)}
        except json.JSONDecodeError:
            return exc.code, {"detail": raw or str(exc)}
    except URLError as exc:
        return 0, {"detail": f"Cannot reach Jarvis Core: {exc.reason}"}


class SettingsWindow:
    def __init__(self, root: tk.Tk, base_url: str = DEFAULT_BASE) -> None:
        self.root = root
        self.base_url = base_url.rstrip("/")
        root.title("Jarvis Settings (TEST)")
        root.geometry("560x640")
        root.minsize(480, 520)

        main = ttk.Frame(root, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

        # --- Core status ---
        status_frame = ttk.LabelFrame(main, text="Jarvis Core status", padding=10)
        status_frame.pack(fill=tk.X, pady=(0, 10))

        self.status_var = tk.StringVar(value="Checking…")
        ttk.Label(status_frame, textvariable=self.status_var, wraplength=500).pack(
            anchor=tk.W
        )
        ttk.Button(status_frame, text="Refresh status", command=self.refresh_status).pack(
            anchor=tk.W, pady=(8, 0)
        )

        # --- How to start ---
        start_frame = ttk.LabelFrame(main, text="How to start Jarvis", padding=10)
        start_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        start_text = tk.Text(start_frame, height=14, wrap=tk.WORD, font=("Consolas", 9))
        start_text.pack(fill=tk.BOTH, expand=True)
        start_text.insert("1.0", START_INSTRUCTIONS)
        start_text.configure(state=tk.DISABLED)

        # --- API keys ---
        keys_frame = ttk.LabelFrame(main, text="API keys (saved to Windows keyring)", padding=10)
        keys_frame.pack(fill=tk.X)

        self.groq_status = tk.StringVar(value="Groq: unknown")
        self.google_status = tk.StringVar(value="Google AI: unknown")
        ttk.Label(keys_frame, textvariable=self.groq_status).grid(
            row=0, column=0, columnspan=3, sticky=tk.W
        )
        ttk.Label(keys_frame, textvariable=self.google_status).grid(
            row=1, column=0, columnspan=3, sticky=tk.W, pady=(0, 8)
        )

        ttk.Label(keys_frame, text="Groq key:").grid(row=2, column=0, sticky=tk.W)
        self.groq_entry = ttk.Entry(keys_frame, width=42, show="*")
        self.groq_entry.grid(row=2, column=1, padx=6, sticky=tk.EW)
        ttk.Button(
            keys_frame, text="Save Groq", command=lambda: self.save_key("groq", self.groq_entry)
        ).grid(row=2, column=2)

        ttk.Label(keys_frame, text="Google AI key:").grid(
            row=3, column=0, sticky=tk.W, pady=(6, 0)
        )
        self.google_entry = ttk.Entry(keys_frame, width=42, show="*")
        self.google_entry.grid(row=3, column=1, padx=6, pady=(6, 0), sticky=tk.EW)
        ttk.Button(
            keys_frame,
            text="Save Google",
            command=lambda: self.save_key("google", self.google_entry),
        ).grid(row=3, column=2, pady=(6, 0))

        keys_frame.columnconfigure(1, weight=1)

        note = ttk.Label(
            main,
            text="TEST build: keys are stored safely, but Jarvis does not call AI models yet.",
            foreground="#555",
        )
        note.pack(anchor=tk.W, pady=(10, 0))

        self.refresh_status()

    def refresh_status(self) -> None:
        code, body = _http_json("GET", f"{self.base_url}/health")
        if code == 200:
            self.status_var.set("Core is RUNNING on 127.0.0.1:8756")
        else:
            detail = body.get("detail", body) if isinstance(body, dict) else body
            self.status_var.set(
                f"Core is NOT running. Start it first.\n({detail})"
            )

        code, body = _http_json("GET", f"{self.base_url}/settings/keys/status")
        if code == 200 and isinstance(body, dict):
            keys = body.get("keys", {})
            self.groq_status.set(
                "Groq: set" if keys.get("groq") else "Groq: not set"
            )
            self.google_status.set(
                "Google AI: set" if keys.get("google") else "Google AI: not set"
            )
        else:
            self.groq_status.set("Groq: (Core offline)")
            self.google_status.set("Google AI: (Core offline)")

    def save_key(self, provider: str, entry: ttk.Entry) -> None:
        value = entry.get().strip()
        if not value:
            messagebox.showwarning("Missing key", f"Paste your {provider} API key first.")
            return

        code, body = _http_json(
            "POST",
            f"{self.base_url}/settings/keys",
            {"provider": provider, "key": value},
        )
        if code == 200:
            entry.delete(0, tk.END)
            messagebox.showinfo("Saved", f"{provider} key saved to Windows Credential Manager.")
            self.refresh_status()
        else:
            detail = body.get("detail", body) if isinstance(body, dict) else body
            messagebox.showerror(
                "Save failed",
                f"Could not save {provider} key.\n\n"
                f"Is Jarvis Core running?\n{detail}",
            )


def main() -> None:
    root = tk.Tk()
    try:
        root.call("tk", "scaling", 1.2)
    except tk.TclError:
        pass
    SettingsWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
