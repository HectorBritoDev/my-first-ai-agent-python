import os
from pathlib import Path

def get_files_info(working_directory, directory="."):
    
    try:
        target_dir_exists = Path(os.path.abspath(directory)).exists()
        
        if target_dir_exists is False:
            return f'Error: "{directory}" is not a directory'
        
        working_dir_abs = os.path.abspath(working_directory)

        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, directory)
        )
        print(target_dir)


        valid_target_dir = os.path.commonpath(
            [working_dir_abs, target_dir]
        ) == working_dir_abs

        # print('Is valid or not', valid_target_dir, 'tested values', f"target {target_dir} working {working_dir_abs}")
        if valid_target_dir is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory' 
    except Exception as e:
        return f'Error: {str(e)}'   
    
    return 'success'

    

    
print(get_files_info('calculators'))