from google.genai import types
from .get_files_info import schema_get_files_info, get_files_info
from .get_file_content import schema_get_files_content, get_file_content
from .run_python_file import schema_run_python_file, run_python_file
from .write_file_content import schema_write_file_content, write_file
from collections.abc import Callable

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_files_content, 
                        schema_run_python_file, schema_write_file_content],
)

# 1. Map the strings to the ACTUAL functions
function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
}

def call_function(
    function_call: types.FunctionCall, verbose: bool = False
) -> types.Content:
    try:
        # 2. Handle the verbose printing
        if verbose:
            print(f"Calling function: {function_call.name}({function_call.args})")
        print(f" - Calling function: {function_call.name}")

        function_name = function_call.name or ""
        
        # 3. Check if the function exists
        if function_name not in function_map:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
        
        # 4. Copy args and inject the secure working directory
        args = dict(function_call.args) if function_call.args else {}
        args["working_directory"] = "./calculator"
        
        # 5. Actually EXECUTE the function using **args
        function_result = function_map[function_name](**args)
        
        # 6. Return the formatted response
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
        
    except Exception:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )