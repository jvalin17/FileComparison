import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "FileCompare"))

from file_checker import compare_directories


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
            self._create_file(dir_a, os.path.join("subdir", "nested.txt"), b"same")
            self._create_file(dir_b, os.path.join("subdir", "nested.txt"), b"same")
            self._create_file(dir_a, "root.txt", b"same")
            self._create_file(dir_b, "root.txt", b"same")

            result = compare_directories(dir_a, dir_b)
            expected_matching = sorted(["root.txt", os.path.join("subdir", "nested.txt")])
            self.assertEqual(sorted(result['matching']), expected_matching)


if __name__ == '__main__':
    unittest.main()
