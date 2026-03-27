# Planning - FileComparison Desktop GUI

## Overview
A desktop GUI wrapper around the FileComparison core algorithm using Python's built-in `tkinter`. Zero external dependencies. Works offline. OS agnostic (Windows, macOS, Linux).

## Constraints (from learnings.md)
- Core algorithm stays as-is — UI is a wrapper only
- No personal info in test data
- Plan before executing
- No unnecessary dependencies
- **Lightweight** — minimal code, no bloat, fast startup
- **No security bugs** — see Security section below
- **Read-only** — never write, modify, or manipulate user data

## Security Principles

1. **Read-only access** — files are opened in `rb` mode only (already enforced by core). UI never writes to user files.
2. **No shell execution** — no `os.system()`, `subprocess`, or `eval()`. Paths come from tkinter file dialogs or typed input only.
3. **Path validation** — validate paths exist via `os.path.exists()` before passing to core. No path traversal risk since core uses `os.path.getsize()` and `open()` which operate on the exact path given.
4. **No temp files** — no temporary files with user content are created. All comparison happens in memory with fixed-size chunks.
5. **No network** — no sockets, no HTTP, no DNS. Fully offline.
6. **No data leakage** — results are displayed in the UI only. Nothing is logged, cached, or written to disk.
7. **Input sanitization** — chunk size comes from a fixed dropdown (not free text). Paths come from OS file dialogs or are validated before use.

## Tech Stack
- **UI Framework:** `tkinter` (ships with Python 3 — no install needed)
- **Styling:** `tkinter.ttk` (themed widgets, modern look)
- **File dialogs:** `tkinter.filedialog` (built-in)
- **Threading:** `threading` (built-in — keeps UI responsive during large file comparisons)
- **Core engine:** `FileCompare/file_checker.py` (existing)

**Dependencies: NONE.** Everything is Python stdlib.

## Directory Structure

```
FileComparison/
├── FileCompare/
│   └── file_checker.py              # Core algorithm (unchanged)
├── tests/                            # Existing test suite (unchanged)
├── ui/
│   ├── planning.md
│   ├── session_log.md
│   ├── app.py                        # Main entry point (launches the GUI)
│   ├── file_compare_gui.py           # GUI class with all UI logic
│   └── run.sh / run.bat              # Auto-run scripts for macOS/Linux and Windows
└── README.md
```

---

## UI Design

### Window Layout

```
┌─────────────────────────────────────────────────────────┐
│  FileComparison Tool                            [─][□][✕]│
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─── Mode ────────────────────────────────────────┐    │
│  │ (●) Compare Files   ( ) Compare Directories     │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  Path 1: [____________________________________] [Browse]│
│  Path 2: [____________________________________] [Browse]│
│                                                         │
│  ┌─── Options ─────────────────────────────────────┐    │
│  │ Chunk Size: [8192  ▼]   [✓] Show detailed results│   │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│                    [ Compare ]                          │
│                                                         │
│  ┌─── Results ─────────────────────────────────────┐    │
│  │                                                  │    │
│  │  Status: ✓ Files are IDENTICAL                   │    │
│  │  Reason: identical                               │    │
│  │  File 1 size: 17,354 bytes                       │    │
│  │  File 2 size: 17,354 bytes                       │    │
│  │                                                  │    │
│  │  --- Directory Mode ---                          │    │
│  │  Matching:      file1.txt, file2.txt             │    │
│  │  Differing:     config.yml                       │    │
│  │  Only in Dir 1: readme.md                        │    │
│  │  Only in Dir 2: notes.txt                        │    │
│  │                                                  │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ┌─── Status Bar ──────────────────────────────────┐    │
│  │ Ready                                            │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### Features by Mode

**File Compare Mode:**
- Two file path inputs with Browse buttons (file dialog)
- Chunk size dropdown (64, 1024, 8192, 65536)
- "Show detailed results" checkbox
  - OFF: calls `compare_files()` — shows True/False
  - ON: calls `compare_files_detailed()` — shows reason + byte offset
- Shows file sizes for both files
- Color-coded result: green for match, red for mismatch

**Directory Compare Mode:**
- Two directory path inputs with Browse buttons (directory dialog)
- Chunk size dropdown
- Results show 4 lists: matching, differing, only_in_first, only_in_second
- Counts for each category

---

## Phases

### Phase 1: GUI + Logic (single file)
**File:** `ui/file_compare_gui.py`

One file, one class. Keeps it simple and lightweight.

- Main window with title and fixed layout
- Mode selector: radio buttons (Files / Directories)
- Two path inputs with Browse buttons
  - File mode: `filedialog.askopenfilename()`
  - Directory mode: `filedialog.askdirectory()`
- Options: chunk size dropdown (fixed values: 64, 1024, 8192, 65536), "Detailed results" checkbox (file mode only)
- Compare button — validates inputs, calls core function, displays results
- Scrollable read-only results text area with color tags (green/red)
- Status bar
- Keyboard: Enter = Compare, Ctrl+L = Clear results
- Background thread for comparison (UI stays responsive)
- **No data manipulation** — paths go in, results come out, nothing written

Security enforced in this file:
- Paths validated with `os.path.exists()` / `os.path.isfile()` / `os.path.isdir()` before use
- Chunk size from fixed dropdown only (no free text)
- No `eval`, `exec`, `subprocess`, `os.system`

### Phase 2: Entry Point & Auto-Run Scripts
**Files:** `ui/app.py`, `ui/run.sh`, `ui/run.bat`

**`app.py`** — minimal launcher:
```python
#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "FileCompare"))

from file_compare_gui import FileCompareGUI

if __name__ == "__main__":
    app = FileCompareGUI()
    app.run()
```

**`run.sh`** (macOS/Linux):
```bash
#!/bin/bash
cd "$(dirname "$0")"
python3 app.py
```

**`run.bat`** (Windows):
```bat
@echo off
cd /d "%~dp0"
python app.py
if errorlevel 1 python3 app.py
pause
```

### Phase 3: Update README
- Add UI section to README with launch instructions for all 3 OS
- Document features

---

## Execution Order

```
Phase 1 (GUI + Logic)        -> Single file with all UI and wiring
Phase 2 (Entry Point)        -> app.py, run.sh, run.bat
Phase 3 (README)             -> Documentation
```

Each phase = separate commit. App is fully functional after Phase 1+2.
