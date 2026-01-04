import os
from pathlib import Path

def get_files_info(working_directory, directory="."):
    
    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, directory)
        )

        target_dir_exists = Path(os.path.abspath(target_dir)).exists()
        
        if target_dir_exists is False:
            return f'Error: "{target_dir}" is not a directory'


        valid_target_dir = os.path.commonpath(
            [working_dir_abs, target_dir]
        ) == working_dir_abs

        if valid_target_dir is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory' 
    
        files = os.scandir(target_dir)


        top_message = (
            f"Result for current directory:" 
            if directory == '.' 
            else f"Result for '{directory}' directory:"
        )
        result_lines = [top_message ]
        for file in files:
            result_lines.append(f"  - {file.name}: file_size={file.stat().st_size} bytes, is_dir={file.is_dir()}")

        return "\n".join(result_lines)

    except Exception as e:
        return f'Error: {str(e)}'
