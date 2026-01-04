import unittest
from get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
    def test_invalid_directory_root(self):
        results = get_files_info("calculator", "/bin")
        self.assertEqual(results, 'Error: Cannot list "/bin" as it is outside the permitted working directory')

    def test_invalid_directory_outside(self):
        results = get_files_info('calculator', '../')
        self.assertEqual(results, 'Error: Cannot list "../" as it is outside the permitted working directory')

    def test_existing_subdirectory(self):
        results = get_files_info('calculator', 'pkg')
        lines = results.split('\n')

        self.assertEqual(lines[0], "Result for 'pkg' directory:")

        # Parse remaining lines into a dict for order-independent comparison
        file_entries = {}
        for line in lines[1:]:
            # Parse "  - filename: file_size=X bytes, is_dir=Y"
            parts = line.strip().lstrip('- ').split(': ', 1)
            file_entries[parts[0]] = parts[1]

        self.assertIn('calculator.py', file_entries)
        self.assertIn('render.py', file_entries)
        self.assertRegex(file_entries['calculator.py'], r'file_size=\d+ bytes, is_dir=False')
        self.assertRegex(file_entries['render.py'], r'file_size=\d+ bytes, is_dir=False')

    def test_existing_directory(self):
        results = get_files_info('calculator')
        self.assertIn('main.py', results)
        self.assertIn('tests.py', results)
        
if __name__ == "__main__":
    unittest.main()