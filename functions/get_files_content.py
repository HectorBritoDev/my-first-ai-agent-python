import os
from config import MAX_CHARS

def get_files_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_file_path]) != abs_working_dir:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'        
        
        with open(target_file_path) as f:
            file_content_string = f.read(MAX_CHARS)
        
    except Exception as e:
        return f"Error getting file content: {e}"
    