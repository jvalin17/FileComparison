import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "FileCompare"))

from file_utilities import collect_file_paths, collect_file_paths_absolute, compute_file_hash


class TestFileUtilities(unittest.TestCase):

    def test_collect_file_paths_returns_relative_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            open(os.path.join(temp_dir, "a.txt"), "w").close()
            sub = os.path.join(temp_dir, "sub")
            os.makedirs(sub)
            open(os.path.join(sub, "b.txt"), "w").close()

            result = collect_file_paths(temp_dir)

            self.assertIn("a.txt", result)
            self.assertIn(os.path.join("sub", "b.txt"), result)
            self.assertEqual(len(result), 2)

    def test_collect_file_paths_absolute_returns_full_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "a.txt")
            open(file_path, "w").close()

            result = collect_file_paths_absolute(temp_dir)

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0], file_path)
            self.assertTrue(os.path.isabs(result[0]))

    def test_compute_file_hash_identical_files_returns_same_hash(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            content = b"identical content for hashing"
            file_a = os.path.join(temp_dir, "a.txt")
            file_b = os.path.join(temp_dir, "b.txt")
            for path in (file_a, file_b):
                with open(path, "wb") as f:
                    f.write(content)

            hash_a = compute_file_hash(file_a)
            hash_b = compute_file_hash(file_b)

            self.assertEqual(hash_a, hash_b)

    def test_compute_file_hash_different_files_returns_different_hash(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_a = os.path.join(temp_dir, "a.txt")
            file_b = os.path.join(temp_dir, "b.txt")
            with open(file_a, "wb") as f:
                f.write(b"content A")
            with open(file_b, "wb") as f:
                f.write(b"content B")

            hash_a = compute_file_hash(file_a)
            hash_b = compute_file_hash(file_b)

            self.assertNotEqual(hash_a, hash_b)


if __name__ == "__main__":
    unittest.main()
