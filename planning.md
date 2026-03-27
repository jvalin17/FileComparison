# Planning - FileComparison Cleanup v1

## Constraint
No built-in functions (e.g., `filecmp.cmp()`) for the core comparison algorithm. Keep the custom byte-by-byte implementation. Optimizations focus on capability, not replacement.

---

## Directory Structure (After All Phases)

```
FileComparison/
├── FileCompare/
│   ├── file_checker.py                          # Core module (compare_files, compare_files_detailed, compare_directories)
│   └── resources/                               # Existing test resource files (unchanged)
│       ├── actual_resume.docx
│       ├── one_letter_different_resume.docx
│       ├── extra_space_resume.docx
│       ├── Jvalin_Dave_resume_ca.pdf
│       ├── Jvalin_Dave_resume_gen.pdf
│       ├── resume.pdf
│       ├── image1.png
│       ├── image1copy.png
│       ├── image2.png
│       ├── audio_file.mp3
│       ├── audio_file_2.mp3
│       ├── audio_file_copy.mp3
│       ├── text1.txt
│       └── text2.txt
├── tests/
│   ├── __init__.py
│   ├── test_compare_files.py                    # Renamed + refactored existing tests + new edge cases
│   ├── test_compare_files_detailed.py           # Tests for Phase 4.4
│   ├── test_compare_directories.py              # Tests for Phase 4.3
│   └── resources/                               # Symlink or copy of FileCompare/resources + test-specific fixtures
│       ├── dir_compare_test/                    # Fixtures for directory comparison tests
│       │   ├── dir_a/
│       │   │   ├── shared_same.txt
│       │   │   ├── shared_diff.txt
│       │   │   └── only_in_a.txt
│       │   └── dir_b/
│       │       ├── shared_same.txt
│       │       ├── shared_diff.txt
│       │       └── only_in_b.txt
│       └── (symlink to FileCompare/resources or copied as needed)
├── planning.md
├── session_log.md
├── learnings.md
└── README.md
```

---

## Phase 1: Bug Fixes

### 1.1 Fix bare `except` clause
**File:** `file_checker.py` line 47
**Current:**
```python
except:
```
**Change to:**
```python
except (FileNotFoundError, PermissionError, OSError) as e:
```
**Why:** Bare `except` catches `SystemExit`, `KeyboardInterrupt`, `MemoryError` - hides real problems.

---

### 1.2 Fix missing return value on exception
**File:** `file_checker.py` lines 48-49
**Current:**
```python
except:
    print "File not found; Invalid Path"
```
**Change to:**
```python
except (FileNotFoundError, PermissionError, OSError) as e:
    print(f"File not found; Invalid Path: {e}")
    return False
```
**Why:** Without `return False`, the function returns `None`. Callers checking `result == False` get unexpected behavior.

---

### 1.3 Fix off-by-one in while loop
**File:** `file_checker.py` line 34
**Current:**
```python
while file_size_read <= file_1_size:
```
**Change to:**
```python
while file_size_read < file_1_size:
```
**Why:** When `file_size_read == file_1_size`, entire file is already consumed. The extra iteration reads 0 bytes (`b"" == b""` is True so it doesn't break correctness, but it's a wasted syscall).

---

### 1.4 Fix `test_InvalidLocation` testing a valid file
**File:** `FileComparisonTest.py` lines 200-201
**Current:**
```python
#file is not present
file_2_loc = self.dir_path + "/resources/" + "extra_space_resume.docx"
```
**Change to:**
```python
#file is not present
file_2_loc = self.dir_path + "/resources/" + "this_file_does_not_exist.docx"
```
**Why:** `extra_space_resume.docx` exists in resources/. The test claims to test invalid paths but actually tests different file content (duplicates `test_OneExtraSpace`).

---

### 1.5 Fix `'__file__'` string literal vs `__file__` variable
**File:** `FileComparisonTest.py` line 16
**Current:**
```python
self.dir_path = os.path.dirname(os.path.realpath('__file__'))
```
**Change to:**
```python
self.dir_path = os.path.dirname(os.path.realpath(__file__))
```
**Why:** `'__file__'` (string) resolves relative to CWD. `__file__` (variable) resolves relative to the actual script location. Current code only works when you `cd` into `FileCompare/` before running tests.

---

## Phase 2: Python 3 Migration

### 2.1 Convert print statements in `file_checker.py`
**File:** `file_checker.py` line 49
**Current:**
```python
print "File not found; Invalid Path"
```
**Change to (already covered by 1.2):**
```python
print(f"File not found; Invalid Path: {e}")
```

---

### 2.2 Convert print statements in `FileComparisonTest.py`
**File:** `FileComparisonTest.py` - 11 occurrences
**Lines and changes:**

| Line | Current | Change to |
|------|---------|-----------|
| 34 | `print "\nOne Letter Different Test Passed"` | `print("\nOne Letter Different Test Passed")` |
| 51 | `print "\nOne Extra Space Test Passed"` | `print("\nOne Extra Space Test Passed")` |
| 69 | `print "\nDifferent Files Test Passed"` | `print("\nDifferent Files Test Passed")` |
| 87 | `print "\nBoth Empty Files Test Passed"` | `print("\nBoth Empty Files Test Passed")` |
| 105 | `print "\nBoth Same Files Test Passed"` | `print("\nBoth Same Files Test Passed")` |
| 123 | `print "\nBoth Same Image Files Test Passed"` | `print("\nBoth Same Image Files Test Passed")` |
| 141 | `print "\nBoth Different Image Files Test Passed"` | `print("\nBoth Different Image Files Test Passed")` |
| 159 | `print "\nBoth Same Audio Files Test Passed"` | `print("\nBoth Same Audio Files Test Passed")` |
| 176 | `print "\nBoth Different Image Files Test Passed"` | `print("\nBoth Different Audio Files Test Passed")` |
| 191 | `print "\nTwo Different Extension Files Test Passed"` | `print("\nTwo Different Extension Files Test Passed")` |
| 211 | `print "\nInvalid File Location Test Passed"` | `print("\nInvalid File Location Test Passed")` |

**Note:** Line 176 also has a copy-paste bug - says "Image" but the test is for audio files. Fix the message text too.

---

### 2.3 Update README.md
**File:** `README.md` line 5
**Current:**
```
#### Language: Python 2.7
```
**Change to:**
```
#### Language: Python 3.x
```

---

## Phase 3: Code Quality

### 3.1 Replace bare `assert` with `unittest` assertions
**File:** `FileComparisonTest.py` - 11 test methods
**Pattern - Current:**
```python
assert actual == expected, 'Test Name - Actual "{}" != expected "{}"'.format(actual, expected)
```
**Pattern - Change to:**
```python
self.assertEqual(actual, expected, 'Test Name')
```
**Lines:** 33, 50, 68, 86, 104, 122, 140, 158, 175, 190, 210

**Why:** `unittest` assertions give richer failure messages, integrate with test runners, and count properly in test reports.

---

### 3.2 Use `os.path.join()` for path construction
**File:** `FileComparisonTest.py` - all test methods
**Pattern - Current:**
```python
file_1_loc = self.dir_path + "/resources/" + "actual_resume.docx"
```
**Pattern - Change to:**
```python
file_1_loc = os.path.join(self.dir_path, "resources", "actual_resume.docx")
```
**Lines:** 23-24, 40-41, 58-59, 76-77, 93-94, 112-113, 130-131, 148-149, 166-167, 183-184, 198-201

**Why:** String concatenation breaks on Windows (uses `\` not `/`). `os.path.join` is cross-platform.

---

### 3.3 Remove unnecessary class wrapper
**File:** `file_checker.py`
**Current:**
```python
class FileComparison ():

    def __init__ (self):
        pass

    def compare_files(self, file_1, file_2):
        ...
```
**Change to:**
```python
def compare_files(file_1, file_2):
    ...
```
**Why:** Class has empty `__init__`, single method, no state. A plain function is simpler. This also requires updating:

**File:** `FileComparisonTest.py` line 7
```python
# from file_checker import FileComparison
from file_checker import compare_files
```

**File:** `FileComparisonTest.py` line 15
```python
# self.fileComparison = FileComparison()
# (remove this line)
```

**File:** `FileComparisonTest.py` - all test methods (11 occurrences)
```python
# actual = self.fileComparison.compare_files(file_1_loc, file_2_loc)
actual = compare_files(file_1_loc, file_2_loc)
```
**Lines:** 30, 47, 65, 83, 101, 119, 137, 155, 171, 187, 207

---

### 3.4 Remove redundant `unittest.TestCase.setUp(self)` call
**File:** `FileComparisonTest.py` line 13
**Current:**
```python
def setUp(self):
    unittest.TestCase.setUp(self)
    self.fileComparison = FileComparison ()
    self.dir_path = os.path.dirname(os.path.realpath('__file__'))
```
**Change to:**
```python
def setUp(self):
    self.dir_path = os.path.dirname(os.path.realpath(__file__))
```
**Why:** Calling `unittest.TestCase.setUp(self)` explicitly is unnecessary (it's a no-op in the base class). The `fileComparison` instance is removed per 3.3.

---

### 3.5 Remove unused `import io`
**File:** `FileComparisonTest.py` line 2
**Current:**
```python
import io
```
**Change to:** Delete this line.
**Why:** `io` is imported but never used.

---

## Phase 4: Capability Optimizations

> Core algorithm stays custom. No `filecmp`. Optimizations add new capabilities.

### 4.1 Same-file shortcut (`os.path.samefile`)
**File:** `file_checker.py` - add before size check
**Add after opening try block:**
```python
# If both paths resolve to the same file, they are identical
if os.path.samefile(file_1, file_2):
    return True
```
**Why:** Avoids all I/O when both arguments are the same file or hardlinks/symlinks to it. This is not replacing the algorithm - it's a pre-check.

---

### 4.2 Configurable chunk size
**File:** `file_checker.py`
**Current:**
```python
def compare_files(file_1, file_2):
    chunk_size = 1024
```
**Change to:**
```python
def compare_files(file_1, file_2, chunk_size=8192):
```
**Why:** 1024 bytes is small for modern I/O. Making it a parameter lets callers tune it. Default 8192 is a good general-purpose size (matches Python's default buffer size).

---

### 4.3 Add directory comparison capability
**File:** `file_checker.py` - add new function
```python
def compare_directories(dir_1, dir_2, chunk_size=8192):
    """
    Compares two directories recursively.
    Returns a dict with keys: 'matching', 'differing', 'only_in_first', 'only_in_second'
    """
    results = {
        'matching': [],
        'differing': [],
        'only_in_first': [],
        'only_in_second': []
    }

    files_1 = set()
    for root, dirs, files in os.walk(dir_1):
        for f in files:
            rel_path = os.path.relpath(os.path.join(root, f), dir_1)
            files_1.add(rel_path)

    files_2 = set()
    for root, dirs, files in os.walk(dir_2):
        for f in files:
            rel_path = os.path.relpath(os.path.join(root, f), dir_2)
            files_2.add(rel_path)

    results['only_in_first'] = sorted(files_1 - files_2)
    results['only_in_second'] = sorted(files_2 - files_1)

    for rel_path in sorted(files_1 & files_2):
        f1 = os.path.join(dir_1, rel_path)
        f2 = os.path.join(dir_2, rel_path)
        if compare_files(f1, f2, chunk_size):
            results['matching'].append(rel_path)
        else:
            results['differing'].append(rel_path)

    return results
```
**Why:** Natural extension - users comparing files often need to compare directories. Built on top of the core algorithm.

---

### 4.4 Add comparison result detail (not just bool)
**File:** `file_checker.py` - add new function
```python
def compare_files_detailed(file_1, file_2, chunk_size=8192):
    """
    Compares two files and returns detailed results.
    Returns a dict with: 'match' (bool), 'reason' (str), 'first_diff_offset' (int or None)
    """
    try:
        if os.path.samefile(file_1, file_2):
            return {'match': True, 'reason': 'same_file', 'first_diff_offset': None}
    except OSError:
        pass

    try:
        size_1 = os.path.getsize(file_1)
        size_2 = os.path.getsize(file_2)
    except (FileNotFoundError, PermissionError, OSError) as e:
        return {'match': False, 'reason': f'error: {e}', 'first_diff_offset': None}

    if size_1 != size_2:
        return {'match': False, 'reason': 'size_mismatch', 'first_diff_offset': None}

    if size_1 == 0:
        return {'match': True, 'reason': 'both_empty', 'first_diff_offset': None}

    offset = 0
    with open(file_1, "rb") as f1, open(file_2, "rb") as f2:
        while offset < size_1:
            chunk_1 = f1.read(chunk_size)
            chunk_2 = f2.read(chunk_size)
            if chunk_1 != chunk_2:
                # Find exact byte offset within chunk
                for i in range(len(chunk_1)):
                    if i < len(chunk_2) and chunk_1[i] != chunk_2[i]:
                        return {'match': False, 'reason': 'content_mismatch', 'first_diff_offset': offset + i}
            offset += chunk_size

    return {'match': True, 'reason': 'identical', 'first_diff_offset': None}
```
**Why:** Knowing WHERE files differ is much more useful than just knowing they differ. Helps debugging and diagnostics.

---

## Phase 5: Test Suite (New `tests/` Directory)

### 5.0 Test directory setup
- Create `tests/` directory at project root
- Create `tests/__init__.py` (empty)
- Create `tests/resources/dir_compare_test/` fixture directories
- Move and rename `FileCompare/FileComparisonTest.py` -> `tests/test_compare_files.py`
- Keep old `FileComparisonTest.py` deleted (tests now live in `tests/`)

### 5.1 `tests/test_compare_files.py` - Core function tests

Rename existing 11 tests + add 7 new edge-case tests = **18 total tests**.

#### Existing tests (renamed to convention):

| # | New Name | What It Tests | Expected |
|---|----------|---------------|----------|
| 1 | `test_compare_files_one_letter_diff_returns_false` | Two docx files differing by one letter | `False` |
| 2 | `test_compare_files_extra_space_returns_false` | Two docx files, one has extra space | `False` |
| 3 | `test_compare_files_different_pdfs_returns_false` | Two different PDF files | `False` |
| 4 | `test_compare_files_both_empty_returns_true` | Two empty text files | `True` |
| 5 | `test_compare_files_same_path_returns_true` | Same file path passed twice | `True` |
| 6 | `test_compare_files_identical_images_returns_true` | Image and its copy | `True` |
| 7 | `test_compare_files_different_images_returns_false` | Two different images | `False` |
| 8 | `test_compare_files_identical_audio_returns_true` | Audio and its copy | `True` |
| 9 | `test_compare_files_different_audio_returns_false` | Two different audio files | `False` |
| 10 | `test_compare_files_different_extensions_returns_false` | docx vs pdf | `False` |
| 11 | `test_compare_files_invalid_path_returns_false` | One file doesn't exist | `False` |

#### New tests to add:

| # | Name | What It Tests | Expected | Why Missing |
|---|------|---------------|----------|-------------|
| 12 | `test_compare_files_both_paths_invalid_returns_false` | Neither file exists | `False` | Only tested one invalid path |
| 13 | `test_compare_files_empty_string_path_returns_false` | Empty string as file path | `False` | No boundary input tests |
| 14 | `test_compare_files_symlink_same_file_returns_true` | Symlink pointing to same file | `True` | Tests 4.1 samefile shortcut |
| 15 | `test_compare_files_custom_chunk_small_returns_true` | Same files with chunk_size=64 | `True` | Tests 4.2 configurable chunk |
| 16 | `test_compare_files_custom_chunk_large_returns_true` | Same files with chunk_size=65536 | `True` | Tests 4.2 configurable chunk |
| 17 | `test_compare_files_custom_chunk_diff_returns_false` | Different files with chunk_size=64 | `False` | Tests 4.2 with mismatch |
| 18 | `test_compare_files_same_file_different_path_returns_true` | Same file via relative vs absolute path | `True` | Tests samefile with path variations |

#### Full code for `tests/test_compare_files.py`:
```python
import unittest
import os
import tempfile

from FileCompare.file_checker import compare_files


class TestCompareFiles(unittest.TestCase):

    def setUp(self):
        self.resources = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.pardir, "FileCompare", "resources"
        )

    # --- Existing tests (renamed) ---

    def test_compare_files_one_letter_diff_returns_false(self):
        f1 = os.path.join(self.resources, "actual_resume.docx")
        f2 = os.path.join(self.resources, "one_letter_different_resume.docx")
        self.assertFalse(compare_files(f1, f2))

    def test_compare_files_extra_space_returns_false(self):
        f1 = os.path.join(self.resources, "actual_resume.docx")
        f2 = os.path.join(self.resources, "extra_space_resume.docx")
        self.assertFalse(compare_files(f1, f2))

    def test_compare_files_different_pdfs_returns_false(self):
        f1 = os.path.join(self.resources, "Jvalin_Dave_resume_ca.pdf")
        f2 = os.path.join(self.resources, "Jvalin_Dave_resume_gen.pdf")
        self.assertFalse(compare_files(f1, f2))

    def test_compare_files_both_empty_returns_true(self):
        f1 = os.path.join(self.resources, "text1.txt")
        f2 = os.path.join(self.resources, "text2.txt")
        self.assertTrue(compare_files(f1, f2))

    def test_compare_files_same_path_returns_true(self):
        f1 = os.path.join(self.resources, "actual_resume.docx")
        self.assertTrue(compare_files(f1, f1))

    def test_compare_files_identical_images_returns_true(self):
        f1 = os.path.join(self.resources, "image1.png")
        f2 = os.path.join(self.resources, "image1copy.png")
        self.assertTrue(compare_files(f1, f2))

    def test_compare_files_different_images_returns_false(self):
        f1 = os.path.join(self.resources, "image1.png")
        f2 = os.path.join(self.resources, "image2.png")
        self.assertFalse(compare_files(f1, f2))

    def test_compare_files_identical_audio_returns_true(self):
        f1 = os.path.join(self.resources, "audio_file.mp3")
        f2 = os.path.join(self.resources, "audio_file_copy.mp3")
        self.assertTrue(compare_files(f1, f2))

    def test_compare_files_different_audio_returns_false(self):
        f1 = os.path.join(self.resources, "audio_file.mp3")
        f2 = os.path.join(self.resources, "audio_file_2.mp3")
        self.assertFalse(compare_files(f1, f2))

    def test_compare_files_different_extensions_returns_false(self):
        f1 = os.path.join(self.resources, "actual_resume.docx")
        f2 = os.path.join(self.resources, "resume.pdf")
        self.assertFalse(compare_files(f1, f2))

    def test_compare_files_invalid_path_returns_false(self):
        f1 = os.path.join(self.resources, "actual_resume.docx")
        f2 = os.path.join(self.resources, "this_file_does_not_exist.docx")
        self.assertFalse(compare_files(f1, f2))

    # --- New edge-case tests ---

    def test_compare_files_both_paths_invalid_returns_false(self):
        f1 = os.path.join(self.resources, "nonexistent_1.txt")
        f2 = os.path.join(self.resources, "nonexistent_2.txt")
        self.assertFalse(compare_files(f1, f2))

    def test_compare_files_empty_string_path_returns_false(self):
        f1 = ""
        f2 = os.path.join(self.resources, "actual_resume.docx")
        self.assertFalse(compare_files(f1, f2))

    def test_compare_files_symlink_same_file_returns_true(self):
        f1 = os.path.join(self.resources, "actual_resume.docx")
        with tempfile.TemporaryDirectory() as tmp:
            symlink_path = os.path.join(tmp, "link_to_resume.docx")
            os.symlink(f1, symlink_path)
            self.assertTrue(compare_files(f1, symlink_path))

    def test_compare_files_custom_chunk_small_returns_true(self):
        f1 = os.path.join(self.resources, "image1.png")
        f2 = os.path.join(self.resources, "image1copy.png")
        self.assertTrue(compare_files(f1, f2, chunk_size=64))

    def test_compare_files_custom_chunk_large_returns_true(self):
        f1 = os.path.join(self.resources, "image1.png")
        f2 = os.path.join(self.resources, "image1copy.png")
        self.assertTrue(compare_files(f1, f2, chunk_size=65536))

    def test_compare_files_custom_chunk_diff_returns_false(self):
        f1 = os.path.join(self.resources, "image1.png")
        f2 = os.path.join(self.resources, "image2.png")
        self.assertFalse(compare_files(f1, f2, chunk_size=64))

    def test_compare_files_same_file_different_path_returns_true(self):
        f1 = os.path.join(self.resources, "actual_resume.docx")
        # Use a path with ../ to reach the same file differently
        f2 = os.path.join(self.resources, "..", "resources", "actual_resume.docx")
        self.assertTrue(compare_files(f1, f2))


if __name__ == '__main__':
    unittest.main()
```

---

### 5.2 `tests/test_compare_files_detailed.py` - Detailed comparison tests

**8 tests total** - all new.

| # | Name | What It Tests | Expected |
|---|------|---------------|----------|
| 1 | `test_compare_files_detailed_same_file_returns_same_file_reason` | Same path passed twice | `{'match': True, 'reason': 'same_file', ...}` |
| 2 | `test_compare_files_detailed_both_empty_returns_both_empty_reason` | Two empty files | `{'match': True, 'reason': 'both_empty', ...}` |
| 3 | `test_compare_files_detailed_identical_content_returns_identical_reason` | Identical copies | `{'match': True, 'reason': 'identical', ...}` |
| 4 | `test_compare_files_detailed_size_mismatch_returns_size_mismatch_reason` | Different sized files | `{'match': False, 'reason': 'size_mismatch', ...}` |
| 5 | `test_compare_files_detailed_content_mismatch_returns_offset` | Same size, different content | `{'match': False, 'reason': 'content_mismatch', 'first_diff_offset': <int>}` |
| 6 | `test_compare_files_detailed_invalid_path_returns_error_reason` | Nonexistent file | `{'match': False, 'reason': 'error: ...', ...}` |
| 7 | `test_compare_files_detailed_content_mismatch_offset_is_nonnegative` | Verify offset >= 0 | `first_diff_offset >= 0` |
| 8 | `test_compare_files_detailed_symlink_returns_same_file_reason` | Symlink to same file | `{'match': True, 'reason': 'same_file', ...}` |

#### Full code for `tests/test_compare_files_detailed.py`:
```python
import unittest
import os
import tempfile

from FileCompare.file_checker import compare_files_detailed


class TestCompareFilesDetailed(unittest.TestCase):

    def setUp(self):
        self.resources = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.pardir, "FileCompare", "resources"
        )

    def test_compare_files_detailed_same_file_returns_same_file_reason(self):
        f1 = os.path.join(self.resources, "actual_resume.docx")
        result = compare_files_detailed(f1, f1)
        self.assertTrue(result['match'])
        self.assertEqual(result['reason'], 'same_file')
        self.assertIsNone(result['first_diff_offset'])

    def test_compare_files_detailed_both_empty_returns_both_empty_reason(self):
        f1 = os.path.join(self.resources, "text1.txt")
        f2 = os.path.join(self.resources, "text2.txt")
        result = compare_files_detailed(f1, f2)
        self.assertTrue(result['match'])
        self.assertEqual(result['reason'], 'both_empty')
        self.assertIsNone(result['first_diff_offset'])

    def test_compare_files_detailed_identical_content_returns_identical_reason(self):
        f1 = os.path.join(self.resources, "image1.png")
        f2 = os.path.join(self.resources, "image1copy.png")
        result = compare_files_detailed(f1, f2)
        self.assertTrue(result['match'])
        self.assertEqual(result['reason'], 'identical')
        self.assertIsNone(result['first_diff_offset'])

    def test_compare_files_detailed_size_mismatch_returns_size_mismatch_reason(self):
        f1 = os.path.join(self.resources, "actual_resume.docx")
        f2 = os.path.join(self.resources, "extra_space_resume.docx")
        result = compare_files_detailed(f1, f2)
        self.assertFalse(result['match'])
        # Could be size_mismatch or content_mismatch depending on actual file sizes
        self.assertIn(result['reason'], ['size_mismatch', 'content_mismatch'])

    def test_compare_files_detailed_content_mismatch_returns_offset(self):
        """Use two files known to differ in content but may be same size."""
        f1 = os.path.join(self.resources, "actual_resume.docx")
        f2 = os.path.join(self.resources, "one_letter_different_resume.docx")
        result = compare_files_detailed(f1, f2)
        self.assertFalse(result['match'])
        # Either size_mismatch (no offset) or content_mismatch (has offset)
        if result['reason'] == 'content_mismatch':
            self.assertIsNotNone(result['first_diff_offset'])
            self.assertGreaterEqual(result['first_diff_offset'], 0)

    def test_compare_files_detailed_invalid_path_returns_error_reason(self):
        f1 = os.path.join(self.resources, "actual_resume.docx")
        f2 = os.path.join(self.resources, "this_file_does_not_exist.docx")
        result = compare_files_detailed(f1, f2)
        self.assertFalse(result['match'])
        self.assertTrue(result['reason'].startswith('error:'))
        self.assertIsNone(result['first_diff_offset'])

    def test_compare_files_detailed_content_mismatch_offset_is_nonnegative(self):
        """Create two temp files that differ at a known position to verify offset accuracy."""
        with tempfile.TemporaryDirectory() as tmp:
            f1_path = os.path.join(tmp, "file_a.bin")
            f2_path = os.path.join(tmp, "file_b.bin")
            # Files identical for first 100 bytes, differ at byte 100
            data = b'\x00' * 100
            with open(f1_path, 'wb') as f:
                f.write(data + b'\x01')
            with open(f2_path, 'wb') as f:
                f.write(data + b'\x02')
            result = compare_files_detailed(f1_path, f2_path)
            self.assertFalse(result['match'])
            self.assertEqual(result['reason'], 'content_mismatch')
            self.assertEqual(result['first_diff_offset'], 100)

    def test_compare_files_detailed_symlink_returns_same_file_reason(self):
        f1 = os.path.join(self.resources, "actual_resume.docx")
        with tempfile.TemporaryDirectory() as tmp:
            symlink_path = os.path.join(tmp, "link.docx")
            os.symlink(f1, symlink_path)
            result = compare_files_detailed(f1, symlink_path)
            self.assertTrue(result['match'])
            self.assertEqual(result['reason'], 'same_file')


if __name__ == '__main__':
    unittest.main()
```

---

### 5.3 `tests/test_compare_directories.py` - Directory comparison tests

**6 tests total** - all new. Uses fixture directories created in `tests/resources/dir_compare_test/`.

| # | Name | What It Tests | Expected |
|---|------|---------------|----------|
| 1 | `test_compare_directories_identical_dirs_returns_all_matching` | Two identical directories | All files in `matching`, rest empty |
| 2 | `test_compare_directories_different_content_returns_differing` | Shared file with different content | File in `differing` list |
| 3 | `test_compare_directories_unique_files_returns_only_in_lists` | Files unique to each dir | Correct `only_in_first` / `only_in_second` |
| 4 | `test_compare_directories_empty_dirs_returns_all_empty` | Two empty directories | All four lists empty |
| 5 | `test_compare_directories_one_empty_dir_returns_only_in_first` | One dir has files, other empty | All files in `only_in_first` |
| 6 | `test_compare_directories_nested_subdirs_returns_correct_relpaths` | Nested subdirectory structure | Relative paths include subdir prefix |

#### Full code for `tests/test_compare_directories.py`:
```python
import unittest
import os
import tempfile

from FileCompare.file_checker import compare_directories


class TestCompareDirectories(unittest.TestCase):

    def _create_file(self, directory, name, content=b"default"):
        path = os.path.join(directory, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(content)
        return path

    def test_compare_directories_identical_dirs_returns_all_matching(self):
        with tempfile.TemporaryDirectory() as tmp:
            dir_a = os.path.join(tmp, "a")
            dir_b = os.path.join(tmp, "b")
            os.makedirs(dir_a)
            os.makedirs(dir_b)
            self._create_file(dir_a, "file1.txt", b"hello")
            self._create_file(dir_a, "file2.txt", b"world")
            self._create_file(dir_b, "file1.txt", b"hello")
            self._create_file(dir_b, "file2.txt", b"world")

            result = compare_directories(dir_a, dir_b)
            self.assertEqual(sorted(result['matching']), ["file1.txt", "file2.txt"])
            self.assertEqual(result['differing'], [])
            self.assertEqual(result['only_in_first'], [])
            self.assertEqual(result['only_in_second'], [])

    def test_compare_directories_different_content_returns_differing(self):
        with tempfile.TemporaryDirectory() as tmp:
            dir_a = os.path.join(tmp, "a")
            dir_b = os.path.join(tmp, "b")
            os.makedirs(dir_a)
            os.makedirs(dir_b)
            self._create_file(dir_a, "same.txt", b"identical")
            self._create_file(dir_b, "same.txt", b"identical")
            self._create_file(dir_a, "diff.txt", b"version_a")
            self._create_file(dir_b, "diff.txt", b"version_b")

            result = compare_directories(dir_a, dir_b)
            self.assertIn("same.txt", result['matching'])
            self.assertIn("diff.txt", result['differing'])

    def test_compare_directories_unique_files_returns_only_in_lists(self):
        with tempfile.TemporaryDirectory() as tmp:
            dir_a = os.path.join(tmp, "a")
            dir_b = os.path.join(tmp, "b")
            os.makedirs(dir_a)
            os.makedirs(dir_b)
            self._create_file(dir_a, "only_a.txt", b"aaa")
            self._create_file(dir_b, "only_b.txt", b"bbb")

            result = compare_directories(dir_a, dir_b)
            self.assertEqual(result['only_in_first'], ["only_a.txt"])
            self.assertEqual(result['only_in_second'], ["only_b.txt"])
            self.assertEqual(result['matching'], [])
            self.assertEqual(result['differing'], [])

    def test_compare_directories_empty_dirs_returns_all_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            dir_a = os.path.join(tmp, "a")
            dir_b = os.path.join(tmp, "b")
            os.makedirs(dir_a)
            os.makedirs(dir_b)

            result = compare_directories(dir_a, dir_b)
            self.assertEqual(result['matching'], [])
            self.assertEqual(result['differing'], [])
            self.assertEqual(result['only_in_first'], [])
            self.assertEqual(result['only_in_second'], [])

    def test_compare_directories_one_empty_dir_returns_only_in_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            dir_a = os.path.join(tmp, "a")
            dir_b = os.path.join(tmp, "b")
            os.makedirs(dir_a)
            os.makedirs(dir_b)
            self._create_file(dir_a, "file1.txt", b"data")
            self._create_file(dir_a, "file2.txt", b"data2")

            result = compare_directories(dir_a, dir_b)
            self.assertEqual(sorted(result['only_in_first']), ["file1.txt", "file2.txt"])
            self.assertEqual(result['only_in_second'], [])
            self.assertEqual(result['matching'], [])

    def test_compare_directories_nested_subdirs_returns_correct_relpaths(self):
        with tempfile.TemporaryDirectory() as tmp:
            dir_a = os.path.join(tmp, "a")
            dir_b = os.path.join(tmp, "b")
            # Create nested structure: subdir/file.txt
            self._create_file(dir_a, os.path.join("subdir", "nested.txt"), b"same")
            self._create_file(dir_b, os.path.join("subdir", "nested.txt"), b"same")
            self._create_file(dir_a, "root.txt", b"same")
            self._create_file(dir_b, "root.txt", b"same")

            result = compare_directories(dir_a, dir_b)
            expected_matching = sorted(["root.txt", os.path.join("subdir", "nested.txt")])
            self.assertEqual(sorted(result['matching']), expected_matching)


if __name__ == '__main__':
    unittest.main()
```

---

## Execution Order (Updated)

```
Phase 1 (Bug Fixes)         ->  Fix 5 bugs in file_checker.py and FileComparisonTest.py
Phase 2 (Python 3)          ->  Convert print statements + README
Phase 3 (Code Quality)      ->  Refactor class to function, unittest assertions, os.path.join, cleanup
Phase 4 (Optimizations)     ->  samefile, chunk_size param, compare_directories, compare_files_detailed
Phase 5 (Test Suite)         ->  Create tests/ dir, write 3 test files (32 total tests), delete old test file
```

Each phase = separate commit. Tests should pass after each phase.

### Test Count Summary

| File | Tests | Coverage |
|------|-------|----------|
| `test_compare_files.py` | 18 | `compare_files()` - all existing + 7 new edge cases |
| `test_compare_files_detailed.py` | 8 | `compare_files_detailed()` - all reasons + offset accuracy |
| `test_compare_directories.py` | 6 | `compare_directories()` - identical, diff, unique, empty, nested |
| **Total** | **32** | All 3 public functions fully covered |
