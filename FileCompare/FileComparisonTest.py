import unittest
import io
import os

#importing file comparison function 
from file_checker import FileComparison

class TestFileComparison (unittest.TestCase):

    #setup test object, FileComparison class object and directory path
    def setUp(self):
        
        unittest.TestCase.setUp(self)
 
        self.fileComparison = FileComparison ()
        self.dir_path = os.path.dirname(os.path.realpath('__file__'))
    
    
    #compares two files in which one letter is different
    def test_OneLetterDifferent (self):
        
        #joins dir_path to actual files
        file_1_loc = self.dir_path + "/resources/" + "actual_resume.docx"
        file_2_loc = self.dir_path + "/resources/" + "one_letter_different_resume.docx"
        
        #expected value from FileComparison function
        expected = False

        #actual value from FileComparison function
        actual = self.fileComparison.compare_files (file_1_loc,file_2_loc)

        #checks expected and actual values
        assert actual == expected, 'One Letter Different Test - Actual "{}" != expected "{}"'.format(actual, expected)
        print "\nOne Letter Different Test Passed"
        
    #compares two files; one of which has extra space character
    def test_OneExtraSpace (self):
        
        #joins dir_path to actual files
        file_1_loc = self.dir_path + "/resources/" + "actual_resume.docx"
        file_2_loc = self.dir_path + "/resources/" + "extra_space_resume.docx"
        
        #expected value from FileComparison function
        expected = False

        #actual value from FileComparison function
        actual = self.fileComparison.compare_files (file_1_loc,file_2_loc)

        #checks expected and actual values
        assert actual == expected, 'One Extra Space Test - Actual "{}" != expected "{}"'.format(actual, expected)
        print "\nOne Extra Space Test Passed"
        
    
    #two different files are given s input
    def test_DifferentFiles (self):
        
        #joins dir_path to actual files
        file_1_loc = self.dir_path + "/resources/" + "Jvalin_Dave_resume_ca.pdf"
        file_2_loc = self.dir_path + "/resources/" + "Jvalin_Dave_resume_gen.pdf"
        
        #expected value from FileComparison function
        expected = False

        #actual value from FileComparison function
        actual = self.fileComparison.compare_files (file_1_loc,file_2_loc)

        #checks expected and actual values
        assert actual == expected, 'Different Files Test - Actual "{}" != expected "{}"'.format(actual, expected)
        print "\nDifferent Files Test Passed"
        

    #two empty files are given as input
    def test_BothEmptyFiles(self):
        
        #joins dir_path to actual files
        file_1_loc = self.dir_path + "/resources/" + "text1.txt"
        file_2_loc = self.dir_path + "/resources/" + "text2.txt"
        
        #expected value from FileComparison function
        expected = True

        #actual value from FileComparison function
        actual = self.fileComparison.compare_files (file_1_loc,file_2_loc)

        #checks expected and actual values
        assert actual == expected, 'Both Empty Files Test - Actual "{}" != expected "{}"'.format(actual, expected)
        print "\nBoth Empty Files Test Passed"
        

    #two same files are given as input
    def test_BothSameFiles(self):
        
        #joins dir_path to actual files
        file_1_loc = self.dir_path + "/resources/" + "actual_resume.docx"
        file_2_loc = self.dir_path + "/resources/" + "actual_resume.docx"
        
        #expected value from FileComparison function
        expected = True

        #actual value from FileComparison function
        actual = self.fileComparison.compare_files (file_1_loc,file_2_loc)

        #checks expected and actual values
        assert actual == expected, 'Both Same Files Test - Actual "{}" != expected "{}"'.format(actual, expected)
        print "\nBoth Same Files Test Passed"
        

    #two same images are given as input
    def test_SameImageFiles(self):
        
        #joins dir_path to actual files
        file_1_loc = self.dir_path + "/resources/" + "image1.png"
        file_2_loc = self.dir_path + "/resources/" + "image1copy.png"
        
        #expected value from FileComparison function
        expected = True

        #actual value from FileComparison function
        actual = self.fileComparison.compare_files (file_1_loc,file_2_loc)

        #checks expected and actual values
        assert actual == expected, 'Both Same Image Files - Actual "{}" != expected "{}"'.format(actual, expected)
        print "\nBoth Same Image Files Test Passed"
        

    #two different images are given as input
    def test_DifferentImageFiles(self):
        
        #joins dir_path to actual files
        file_1_loc = self.dir_path + "/resources/" + "image1.png"
        file_2_loc = self.dir_path + "/resources/" + "image2.png"
        
        #expected value from FileComparison function
        expected = False

        #actual value from FileComparison function
        actual = self.fileComparison.compare_files (file_1_loc,file_2_loc)

        #checks expected and actual values
        assert actual == expected, 'Both Different Image Files - Actual "{}" != expected "{}"'.format(actual, expected)
        print "\nBoth Different Image Files Test Passed"
        

    #two same audio files are given as input
    def test_SameAudioFiles(self):
        
        #joins dir_path to actual files
        file_1_loc = self.dir_path + "/resources/" + "audio_file.mp3"
        file_2_loc = self.dir_path + "/resources/" + "audio_file_copy.mp3"
        
        #expected value from FileComparison function
        expected = True

        #actual value from FileComparison function
        actual = self.fileComparison.compare_files (file_1_loc,file_2_loc)

        #checks expected and actual values
        assert actual == expected, 'Both Same Audio Files Test - Actual "{}" != expected "{}"'.format(actual, expected)
        print "\nBoth Same Audio Files Test Passed"
        
    #two different audio files are given as input
    def test_DifferentAudioFiles(self):
        
        #joins dir_path to actual files
        file_1_loc = self.dir_path + "/resources/" + "audio_file.mp3"
        file_2_loc = self.dir_path + "/resources/" + "audio_file_2.mp3"
        
        #expected value from FileComparison function
        expected = False

        #actual value from FileComparison function
        actual = self.fileComparison.compare_files (file_1_loc,file_2_loc)

        #checks expected and actual values
        assert actual == expected, 'Both Different Image Files - Actual "{}" != expected "{}"'.format(actual, expected)
        print "\nBoth Different Image Files Test Passed"
        
    #two different extension files are given as input
    def test_DifferentExtensionFiles(self):
        
        #joins dir_path to actual files
        file_1_loc = self.dir_path + "/resources/" + "actual_resume.docx"
        file_2_loc = self.dir_path + "/resources/" + "resume.pdf"
        
        #expected value from FileComparison function
        expected = False
        actual = self.fileComparison.compare_files (file_1_loc,file_2_loc)

        #checks expected and actual values
        assert actual == expected, 'Two Different Extension Files - Actual "{}" != expected "{}"'.format(actual, expected)
        print "\nTwo Different Extension Files Test Passed"
        

    #invalid file location is given as input 
    def test_InvalidLocation (self):
        
        #joins dir_path to actual files
        file_1_loc = self.dir_path + "/resources/" + "actual_resume.docx"

        #file is not present
        file_2_loc = self.dir_path + "/resources/" + "extra_space_resume.docx"
        
        #expected value from FileComparison function
        expected = False

        #actual value from FileComparison function
        actual = self.fileComparison.compare_files (file_1_loc,file_2_loc)

        #checks expected and actual values
        assert actual == expected, 'Invalid File Location Test - Actual "{}" != expected "{}"'.format(actual, expected)
        print "\nInvalid File Location Test Passed"
        
    
if __name__ == '__main__':
    unittest.main()

