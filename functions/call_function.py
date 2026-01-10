from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def call_function(function_call: types.FunctionCall, verbose=False):
    if verbose is True:
        print(f"Calling function: {function_call.name}({function_call.args})")
    
    print(f" - Calling function: {function_call.name}")

    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

    function_name = function_call.name or ""
    
    if not function_map[function_name]:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    args = dict(function_call.args) if function_call.args else {}
    args['working_directory'] = './calculator'

    function_result = function_map[function_name](**args)

    return types.Content(
        role='tool',
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={'results': function_result}
            )
        ]
    )

    


    