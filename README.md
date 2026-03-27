## FileComparison

A lightweight tool to compare files and directories byte-by-byte. Includes a desktop GUI. Works offline, no internet required.

---

### Quick Start (Download and Run)

#### Step 1: Clone the repo
```bash
git clone https://github.com/jvalin17/FileComparison.git
cd FileComparison
```

#### Step 2: Launch the app
```bash
# macOS / Linux (auto-installs tkinter if missing)
cd ui
./run.sh

# Windows
cd ui
run.bat
```

That's it. The `run.sh` script will:
1. Find Python 3 on your system
2. Check if tkinter is available
3. If not, install it automatically (Homebrew on macOS, dnf on Fedora, apt on Ubuntu/Debian)
4. Launch the app

> **Windows users:** tkinter comes pre-installed with Python from [python.org](https://www.python.org/downloads/). Just make sure to check "tcl/tk" during installation.

---

### Desktop GUI

A lightweight desktop app built with Python's built-in `tkinter`. No external dependencies.

**Features:**
- Compare files or entire directories
- Shows whether files are identical or different, with the reason why
- Shows the exact byte position where files first differ
- Color-coded results (green = match, red = mismatch)
- Adjustable speed (Tiny / Small / Standard / Large)
- Progress bar during comparison
- Read-only — never writes or modifies your files
- No internet, no network, fully offline

---

### Using as a Python Library

```python
from FileCompare.file_checker import compare_files_detailed, compare_directories

# Compare two files (returns match status, reason, and byte offset of first difference)
compare_files_detailed("file_a.txt", "file_b.txt")
# {'match': False, 'reason': 'content_mismatch', 'first_diff_offset': 1024}

# Compare two directories recursively
compare_directories("/path/to/dir_a", "/path/to/dir_b")
# {'matching': ['shared.txt'], 'differing': ['config.yml'],
#  'only_in_first': ['a.log'], 'only_in_second': ['b.log']}
```

| Function | Description | Returns |
|----------|-------------|---------|
| `compare_files(f1, f2, chunk_size=8192)` | Compares two files byte by byte | `True` / `False` |
| `compare_files_detailed(f1, f2, chunk_size=8192)` | Compares with diagnostics | `dict` with `match`, `reason`, `first_diff_offset` |
| `compare_directories(d1, d2, chunk_size=8192)` | Compares directories recursively | `dict` with `matching`, `differing`, `only_in_first`, `only_in_second` |

---

### Algorithm

1. If both paths point to the same file, return `True`
2. Compare file sizes — if different, return `False`
3. If both files are empty, return `True`
4. Read both files in chunks, comparing each pair
5. If any chunk differs, return `False`
6. If all chunks match, return `True`

| | Value |
|---|---|
| Time | O(n) where n = file size in bytes |
| Space | O(m) where m = chunk size |

---

### Project Structure

```
FileComparison/
├── FileCompare/
│   ├── file_checker.py              # Core algorithm (3 functions)
│   ├── FileComparisonTest.py        # Legacy tests (11 tests)
│   └── resources/                   # Test resource files
├── tests/
│   ├── test_compare_files.py        # 18 tests
│   ├── test_compare_files_detailed.py  # 8 tests
│   └── test_compare_directories.py  # 6 tests
├── build_exe.py                      # Build standalone executable
├── FileComparison.spec               # PyInstaller config
└── ui/
    ├── app.py                        # Entry point
    ├── file_compare_gui.py           # GUI (~285 lines)
    ├── run.sh                        # macOS/Linux launcher (auto-installs deps)
    └── run.bat                       # Windows launcher
```

### Download (No Python Required)

Pre-built standalone executables are available on the [Releases](https://github.com/jvalin17/FileComparison/releases) page. Download, unzip, and run — no Python installation needed.

> **macOS:** You may need to right-click > Open the first time (unsigned app).

---

### Building Standalone Executables

Build a standalone executable that runs without Python installed.

#### Prerequisites (build machine only)
```bash
pip install pyinstaller
```

#### Build
```bash
cd FileComparison
python3 build_exe.py
```

#### Output
| Platform | Output | Location |
|----------|--------|----------|
| macOS | `.app` bundle | `dist/FileComparison Tool.app` |
| Windows | `.exe` file | `dist/FileComparison Tool.exe` |
| Linux | Binary | `dist/FileComparison Tool` |

> **Note:** PyInstaller builds are platform-specific. Build on the target OS.

---

### Running Tests

```bash
cd FileComparison

# Run full test suite (32 tests)
python3 -m unittest discover -s tests -v
```
