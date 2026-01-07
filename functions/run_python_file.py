import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if abs_file_path[-3::] != '.py':
           return f'Error: "{file_path}" is not a Python file' 

           
        command = ["python", abs_file_path]
        if args:
            command.extend(args)

        command_result: subprocess.CompletedProcess = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=3000,
        )

        result = []

        if command_result.returncode != 0:
            result.append(f"Process exited with code {command_result.returncode}")
        
        if command_result.stdout is None or command_result.stderr is None:
            result.append(f"No output produced")
        
        result.append(f"STDOUT: {command_result.stdout}")
        result.append(f"STDERR: {command_result.stderr}")

        return result
    except Exception as e:
        return f"Error: executing Python file: {e}" 