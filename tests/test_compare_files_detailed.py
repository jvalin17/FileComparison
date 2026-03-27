import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "FileCompare"))

from file_checker import compare_files_detailed


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
        self.assertIn(result['reason'], ['size_mismatch', 'content_mismatch'])

    def test_compare_files_detailed_content_mismatch_returns_offset(self):
        f1 = os.path.join(self.resources, "actual_resume.docx")
        f2 = os.path.join(self.resources, "one_letter_different_resume.docx")
        result = compare_files_detailed(f1, f2)
        self.assertFalse(result['match'])
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
        with tempfile.TemporaryDirectory() as tmp:
            f1_path = os.path.join(tmp, "file_a.bin")
            f2_path = os.path.join(tmp, "file_b.bin")
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
