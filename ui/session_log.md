# Session Log - FileComparison Desktop GUI

## Session 1 - 2026-03-27

### Actions Taken
1. **Clarified requirements** — Desktop GUI (tkinter), all 3 core functions, same repo in `ui/` directory.
2. **Reviewed learnings.md** — Applied constraints: preserve core algorithm, no dependencies, plan before executing.
3. **Created planning.md** — 3-phase plan with ASCII mockup, security principles, directory structure.
4. **Applied user feedback** — lightweight, no security bugs, read-only. Simplified plan from 5 phases to 3. Added Security Principles section.
5. **Updated learnings.md** — Added principle #6: lightweight, no security bugs, read-only.

### Build Log

#### Phase 1: GUI + Logic (`file_compare_gui.py`)
- **Status:** COMPLETE
- Wrote `file_compare_gui.py` (~220 lines, single class)
- Features: mode toggle, path inputs, browse buttons, chunk size dropdown, detailed checkbox, scrollable results, color-coded output, status bar, keyboard shortcuts
- Security: read-only, no shell exec, no temp files, no network, path validation, fixed dropdown values

#### Phase 1 — Tkinter Issue
- **Attempt 1 FAILED:** System Python 3.9.6 (`/usr/bin/python3`) — tkinter crashed with `macOS 26 (2603) or later required, have instead 16 (1603)`. System Python's tkinter binary was compiled for a newer macOS.
  ```
  Error: macOS 26 (2603) or later required, have instead 16 (1603) !
  Abort trap: 6
  ```
- **Attempt 2 FAILED:** Homebrew Python 3.14 (`/opt/homebrew/bin/python3.14`) — tkinter module not compiled.
  ```
  ModuleNotFoundError: No module named '_tkinter'
  ```
- **Resolution:** Asked user. User chose "Fix tkinter first". Ran `brew install python-tk@3.14`.
  - tcl-tk had a non-blocking symlink warning (conflicting with system Tcl.framework). Did NOT force overwrite.
  - python-tk@3.14 installed to `/usr/local/Cellar/python-tk@3.14/3.14.3`
  - Verified: `/usr/local/bin/python3.14 -c "import tkinter"` — SUCCESS.

#### Phase 1 — Verification
- Import smoke test: PASS
- GUI launch + auto-close (2s): PASS
- File comparison through GUI logic: PASS (image1.png vs image1copy.png → identical)
- Directory comparison through GUI logic: PASS (14 matching files)

#### Phase 2: Entry Point & Scripts
- **Status:** COMPLETE
- Created `app.py` (minimal launcher, 10 lines)
- Created `run.sh` (auto-detects Python with tkinter, tries python3.14 → python3 → python)
- Created `run.bat` (Windows, tries python → python3)
- Made `run.sh` executable

#### Phase 3: Update README
- **Status:** COMPLETE
- Added Desktop GUI section with features, launch instructions, tkinter install commands for all 3 OS
- Updated project structure to include `ui/` directory

### Decisions Made
- **Tkinter** chosen: zero dependencies, ships with Python 3, OS agnostic.
- **Single GUI file**: keeps it lightweight (~220 lines).
- **Read-only only**: core opens files in `rb` mode, UI never writes user data.
- **No shell execution**: no `os.system`, `subprocess`, `eval`.
- **No temp files, no network, no data leakage**.
- **Fixed chunk size dropdown**: no free-text input.
- **run.sh auto-detects** correct Python with tkinter support.
- **Python 3.14** via `/usr/local/bin/python3.14` is the working Python on this machine.

### Error Log

| # | What | Error | Resolution | Attempt |
|---|------|-------|------------|---------|
| 1 | tkinter on system Python 3.9.6 | `macOS 26 (2603) or later required` — Abort trap | Switched to Homebrew Python | 1/2 |
| 2 | tkinter on `/opt/homebrew/bin/python3.14` | `No module named '_tkinter'` | Installed python-tk@3.14 via brew | 2/2 |
| 3 | tcl-tk brew link | Symlink conflict with system Tcl.framework | Non-blocking, ignored (python-tk still works) | N/A |
