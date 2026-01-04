import os
from pathlib import Path

def get_files_info(working_directory, directory="."):
    
    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, directory)
        )

        target_dir_exists = Path(os.path.abspath(target_dir)).exists()
        
        top_message = (
            f"Result for current directory:"
            if directory == '.'
            else f"Result for '{directory}' directory:"
        )

        if target_dir_exists is False:
            error_message = f'{top_message}\n    Error: Directory "{directory}" does not exist.'
            print(error_message)
            return error_message


        valid_target_dir = os.path.commonpath(
            [working_dir_abs, target_dir]
        ) == working_dir_abs

        if valid_target_dir is False:
            error_message = f'{top_message}\n    Error: Cannot list "{directory}" as it is outside the permitted working directory'
            print(error_message)
            return error_message

        files = os.scandir(target_dir)
        result_lines = [top_message]
        for file in files:
            result_lines.append(f"  - {file.name}: file_size={file.stat().st_size} bytes, is_dir={file.is_dir()}")


        result = "\n".join(result_lines)
        print(result)

        return result

    except Exception as e:
        return f'Error: {str(e)}'
