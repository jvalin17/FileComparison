import unittest
import os

from file_checker import compare_files


class TestFileComparison(unittest.TestCase):

    def setUp(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

    def test_OneLetterDifferent(self):
        file_1_loc = os.path.join(self.dir_path, "resources", "actual_resume.docx")
        file_2_loc = os.path.join(self.dir_path, "resources", "one_letter_different_resume.docx")
        self.assertEqual(compare_files(file_1_loc, file_2_loc), False)
        print("\nOne Letter Different Test Passed")

    def test_OneExtraSpace(self):
        file_1_loc = os.path.join(self.dir_path, "resources", "actual_resume.docx")
        file_2_loc = os.path.join(self.dir_path, "resources", "extra_space_resume.docx")
        self.assertEqual(compare_files(file_1_loc, file_2_loc), False)
        print("\nOne Extra Space Test Passed")

    def test_DifferentFiles(self):
        file_1_loc = os.path.join(self.dir_path, "resources", "Jvalin_Dave_resume_ca.pdf")
        file_2_loc = os.path.join(self.dir_path, "resources", "Jvalin_Dave_resume_gen.pdf")
        self.assertEqual(compare_files(file_1_loc, file_2_loc), False)
        print("\nDifferent Files Test Passed")

    def test_BothEmptyFiles(self):
        file_1_loc = os.path.join(self.dir_path, "resources", "text1.txt")
        file_2_loc = os.path.join(self.dir_path, "resources", "text2.txt")
        self.assertEqual(compare_files(file_1_loc, file_2_loc), True)
        print("\nBoth Empty Files Test Passed")

    def test_BothSameFiles(self):
        file_1_loc = os.path.join(self.dir_path, "resources", "actual_resume.docx")
        file_2_loc = os.path.join(self.dir_path, "resources", "actual_resume.docx")
        self.assertEqual(compare_files(file_1_loc, file_2_loc), True)
        print("\nBoth Same Files Test Passed")

    def test_SameImageFiles(self):
        file_1_loc = os.path.join(self.dir_path, "resources", "image1.png")
        file_2_loc = os.path.join(self.dir_path, "resources", "image1copy.png")
        self.assertEqual(compare_files(file_1_loc, file_2_loc), True)
        print("\nBoth Same Image Files Test Passed")

    def test_DifferentImageFiles(self):
        file_1_loc = os.path.join(self.dir_path, "resources", "image1.png")
        file_2_loc = os.path.join(self.dir_path, "resources", "image2.png")
        self.assertEqual(compare_files(file_1_loc, file_2_loc), False)
        print("\nBoth Different Image Files Test Passed")

    def test_SameAudioFiles(self):
        file_1_loc = os.path.join(self.dir_path, "resources", "audio_file.mp3")
        file_2_loc = os.path.join(self.dir_path, "resources", "audio_file_copy.mp3")
        self.assertEqual(compare_files(file_1_loc, file_2_loc), True)
        print("\nBoth Same Audio Files Test Passed")

    def test_DifferentAudioFiles(self):
        file_1_loc = os.path.join(self.dir_path, "resources", "audio_file.mp3")
        file_2_loc = os.path.join(self.dir_path, "resources", "audio_file_2.mp3")
        self.assertEqual(compare_files(file_1_loc, file_2_loc), False)
        print("\nBoth Different Audio Files Test Passed")

    def test_DifferentExtensionFiles(self):
        file_1_loc = os.path.join(self.dir_path, "resources", "actual_resume.docx")
        file_2_loc = os.path.join(self.dir_path, "resources", "resume.pdf")
        self.assertEqual(compare_files(file_1_loc, file_2_loc), False)
        print("\nTwo Different Extension Files Test Passed")

    def test_InvalidLocation(self):
        file_1_loc = os.path.join(self.dir_path, "resources", "actual_resume.docx")
        file_2_loc = os.path.join(self.dir_path, "resources", "this_file_does_not_exist.docx")
        self.assertEqual(compare_files(file_1_loc, file_2_loc), False)
        print("\nInvalid File Location Test Passed")


if __name__ == '__main__':
    unittest.main()
