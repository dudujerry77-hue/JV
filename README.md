# Jarvis

A long-term personal AI operating system.

**Start here:** [`.jarvis/constitution.md`](.jarvis/constitution.md)

Any agent or contributor working on this project must read, in order:

1. `.jarvis/constitution.md`
2. `.jarvis/current_phase.md`
3. `.jarvis/project_state.json`
4. `.jarvis/agent_rules.md`

See `.jarvis/roadmap.md` for the phased plan and `.jarvis/decisions.md` for
the architectural decision log.

---

## How to start (TEST: Settings UI + key storage)

Branch: `test/settings-ui-api-keys` — marked as **TEST**. Not production.

### 1. Install (once)

```powershell
cd path\to\JV
pip install -e ".[dev]"
```

### 2. Start Jarvis Core (leave this window open)

```powershell
python -m jarvis_core.service.main
```

Core listens on `http://127.0.0.1:8756` only.

### 3. Open the Settings desktop window (second window)

```powershell
python -m jarvis_ui.settings_window
```

In the Settings window you can:

- See whether Core is running
- Read step-by-step start instructions
- Paste **Groq** and **Google AI** API keys and save them

Keys are stored in **Windows Credential Manager** (never in project files).

### 4. Run tests

```powershell
pytest
```

### What this TEST build does *not* do yet

- It does **not** call Groq or Gemini models
- It does **not** chat or answer questions
- It only stores keys safely and shows how to start Core
