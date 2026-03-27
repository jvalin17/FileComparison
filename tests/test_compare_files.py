import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "FileCompare"))

from file_checker import compare_files


class TestCompareFiles(unittest.TestCase):

    def setUp(self):
        self.resources = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.pardir, "FileCompare", "resources"
        )

    # --- Existing tests (renamed to convention) ---

    def test_compare_files_one_letter_diff_returns_false(self):
        f1 = os.path.join(self.resources, "sample_doc_a.docx")
        f2 = os.path.join(self.resources, "sample_doc_b.docx")
        self.assertFalse(compare_files(f1, f2))

    def test_compare_files_extra_space_returns_false(self):
        f1 = os.path.join(self.resources, "sample_doc_a.docx")
        f2 = os.path.join(self.resources, "sample_doc_c.docx")
        self.assertFalse(compare_files(f1, f2))

    def test_compare_files_different_pdfs_returns_false(self):
        f1 = os.path.join(self.resources, "sample_pdf_a.pdf")
        f2 = os.path.join(self.resources, "sample_pdf_b.pdf")
        self.assertFalse(compare_files(f1, f2))

    def test_compare_files_both_empty_returns_true(self):
        f1 = os.path.join(self.resources, "text1.txt")
        f2 = os.path.join(self.resources, "text2.txt")
        self.assertTrue(compare_files(f1, f2))

    def test_compare_files_same_path_returns_true(self):
        f1 = os.path.join(self.resources, "sample_doc_a.docx")
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
        f1 = os.path.join(self.resources, "sample_doc_a.docx")
        f2 = os.path.join(self.resources, "sample_pdf_c.pdf")
        self.assertFalse(compare_files(f1, f2))

    def test_compare_files_invalid_path_returns_false(self):
        f1 = os.path.join(self.resources, "sample_doc_a.docx")
        f2 = os.path.join(self.resources, "this_file_does_not_exist.docx")
        self.assertFalse(compare_files(f1, f2))

    # --- New edge-case tests ---

    def test_compare_files_both_paths_invalid_returns_false(self):
        f1 = os.path.join(self.resources, "nonexistent_1.txt")
        f2 = os.path.join(self.resources, "nonexistent_2.txt")
        self.assertFalse(compare_files(f1, f2))

    def test_compare_files_empty_string_path_returns_false(self):
        f1 = ""
        f2 = os.path.join(self.resources, "sample_doc_a.docx")
        self.assertFalse(compare_files(f1, f2))

    def test_compare_files_symlink_same_file_returns_true(self):
        f1 = os.path.join(self.resources, "sample_doc_a.docx")
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
        f1 = os.path.join(self.resources, "sample_doc_a.docx")
        f2 = os.path.join(self.resources, "..", "resources", "sample_doc_a.docx")
        self.assertTrue(compare_files(f1, f2))


if __name__ == '__main__':
    unittest.main()
