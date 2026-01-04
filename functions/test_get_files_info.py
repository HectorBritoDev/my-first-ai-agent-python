import unittest
from get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
    def test_invalid_directory_root(self):
        results = get_files_info("calculator", "/bin")
        self.assertEqual(results, 'Error: Cannot list "/bin" as it is outside the permitted working directory')

    def test_invalid_directory_outside(self):
        results = get_files_info('calculator', '../')
        self.assertEqual(results, 'Error: Cannot list "../" as it is outside the permitted working directory')

    def test_existing_directory(self):
        results = get_files_info('calculator', 'pkg')
        self.assertEqual(results, 'success')
        
        
if __name__ == "__main__":
    unittest.main()