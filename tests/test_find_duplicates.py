import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "FileCompare"))

from file_checker import find_duplicates


class TestFindDuplicates(unittest.TestCase):

    def _write_file(self, path, content=b"default content"):
        with open(path, "wb") as f:
            f.write(content)

    def test_find_duplicates_identical_files_returns_one_group(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self._write_file(os.path.join(temp_dir, "a.txt"), b"same")
            self._write_file(os.path.join(temp_dir, "b.txt"), b"same")

            result = find_duplicates(temp_dir)

            self.assertEqual(result["total_groups"], 1)
            self.assertEqual(len(result["duplicates"]), 1)
            self.assertEqual(len(result["duplicates"][0]), 2)

    def test_find_duplicates_no_duplicates_returns_empty(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self._write_file(os.path.join(temp_dir, "a.txt"), b"unique content A")
            self._write_file(os.path.join(temp_dir, "b.txt"), b"unique content BB")

            result = find_duplicates(temp_dir)

            self.assertEqual(result["total_groups"], 0)
            self.assertEqual(result["duplicates"], [])
            self.assertEqual(result["unique_count"], 2)

    def test_find_duplicates_multiple_groups_returns_correct_count(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self._write_file(os.path.join(temp_dir, "a1.txt"), b"group A")
            self._write_file(os.path.join(temp_dir, "a2.txt"), b"group A")
            self._write_file(os.path.join(temp_dir, "b1.txt"), b"group B content")
            self._write_file(os.path.join(temp_dir, "b2.txt"), b"group B content")
            self._write_file(os.path.join(temp_dir, "unique.txt"), b"only one of these")

            result = find_duplicates(temp_dir)

            self.assertEqual(result["total_groups"], 2)
            self.assertEqual(result["total_files"], 5)
            self.assertEqual(result["unique_count"], 1)

    def test_find_duplicates_nested_subdirs_finds_duplicates(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sub = os.path.join(temp_dir, "subdir")
            os.makedirs(sub)
            self._write_file(os.path.join(temp_dir, "original.txt"), b"nested dup")
            self._write_file(os.path.join(sub, "copy.txt"), b"nested dup")

            result = find_duplicates(temp_dir)

            self.assertEqual(result["total_groups"], 1)
            self.assertEqual(len(result["duplicates"][0]), 2)

    def test_find_duplicates_different_sizes_not_grouped(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self._write_file(os.path.join(temp_dir, "short.txt"), b"abc")
            self._write_file(os.path.join(temp_dir, "long.txt"), b"abcdef")

            result = find_duplicates(temp_dir)

            self.assertEqual(result["total_groups"], 0)
            self.assertEqual(result["unique_count"], 2)

    def test_find_duplicates_empty_directory_returns_zero(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = find_duplicates(temp_dir)

            self.assertEqual(result["total_files"], 0)
            self.assertEqual(result["total_groups"], 0)
            self.assertEqual(result["unique_count"], 0)
            self.assertEqual(result["duplicates"], [])

    def test_find_duplicates_triplet_returns_group_of_three(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self._write_file(os.path.join(temp_dir, "x.txt"), b"triple")
            self._write_file(os.path.join(temp_dir, "y.txt"), b"triple")
            self._write_file(os.path.join(temp_dir, "z.txt"), b"triple")

            result = find_duplicates(temp_dir)

            self.assertEqual(result["total_groups"], 1)
            self.assertEqual(len(result["duplicates"][0]), 3)


if __name__ == "__main__":
    unittest.main()
