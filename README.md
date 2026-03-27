## FileComparison

Compares files and directories byte-by-byte to determine if they are identical.

#### Language: Python 3.x

#### Functions

| Function | Description | Returns |
|----------|-------------|---------|
| `compare_files(file_1, file_2, chunk_size=8192)` | Compares two files byte by byte | `True` if identical, `False` otherwise |
| `compare_files_detailed(file_1, file_2, chunk_size=8192)` | Compares two files with diagnostics | `dict` with `match`, `reason`, `first_diff_offset` |
| `compare_directories(dir_1, dir_2, chunk_size=8192)` | Compares two directories recursively | `dict` with `matching`, `differing`, `only_in_first`, `only_in_second` |

#### Usage

```python
from FileCompare.file_checker import compare_files, compare_files_detailed, compare_directories

# Simple comparison
compare_files("file_a.txt", "file_b.txt")  # True or False

# Detailed comparison (shows where files differ)
compare_files_detailed("file_a.txt", "file_b.txt")
# {'match': False, 'reason': 'content_mismatch', 'first_diff_offset': 1024}

# Directory comparison
compare_directories("/path/to/dir_a", "/path/to/dir_b")
# {'matching': ['shared.txt'], 'differing': ['config.yml'], 'only_in_first': ['a.log'], 'only_in_second': ['b.log']}
```

#### Algorithm

1. If both paths point to the same file (via `os.path.samefile`), return `True`
2. Compare file sizes — if different, return `False`
3. If both files are empty, return `True`
4. Read both files in configurable chunks (default 8192 bytes), comparing each pair
5. If any chunk differs, return `False`
6. If all chunks match, return `True`

#### Complexity

| | Value |
|---|---|
| Time | O(n) where n = file size in bytes |
| Space | O(m) where m = chunk size |

#### Desktop GUI

A lightweight desktop GUI with zero external dependencies (uses Python's built-in `tkinter`).

**Features:**
- Compare files or directories (toggle via radio buttons)
- Browse buttons for file/directory selection
- Configurable chunk size (64, 1024, 8192, 65536)
- Detailed mode: shows reason and exact byte offset of first difference
- Color-coded results (green = match, red = mismatch)
- Read-only — never writes or modifies your files

**Launch:**
```bash
# macOS / Linux
cd ui && ./run.sh

# Windows
cd ui && run.bat

# Direct
python3 ui/app.py
```

**Requirements:** Python 3 with tkinter. If tkinter is missing:
```bash
# macOS
brew install python-tk@3.14

# Ubuntu/Debian
sudo apt install python3-tk

# Windows — tkinter is included with the standard Python installer
```

#### Project Structure

```
FileComparison/
├── FileCompare/
│   ├── file_checker.py              # Core module (3 functions)
│   ├── FileComparisonTest.py        # Legacy tests (11 tests)
│   └── resources/                   # Test resource files
├── tests/
│   ├── test_compare_files.py        # 18 tests
│   ├── test_compare_files_detailed.py  # 8 tests
│   └── test_compare_directories.py  # 6 tests
└── ui/
    ├── app.py                        # Entry point
    ├── file_compare_gui.py           # GUI (single file, ~220 lines)
    ├── run.sh                        # macOS/Linux launcher
    └── run.bat                       # Windows launcher
```

#### Running Tests

```bash
# Run full test suite (32 tests)
python3 -m unittest discover -s tests -v

# Run legacy tests
cd FileCompare && python3 -m unittest FileComparisonTest -v
```

#### Tests (32 total)

**`test_compare_files.py` (18 tests)**
- Same files, different files, empty files, images, audio, PDFs, docx
- Edge cases: invalid paths, empty string, symlinks, custom chunk sizes, path variations

**`test_compare_files_detailed.py` (8 tests)**
- All 5 reason types: `same_file`, `both_empty`, `identical`, `size_mismatch`, `content_mismatch`
- Exact byte offset accuracy, error handling, symlink detection

**`test_compare_directories.py` (6 tests)**
- Identical dirs, different content, unique files, empty dirs, nested subdirectories
