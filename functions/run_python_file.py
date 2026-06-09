import os, subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command-line arguments to pass to the script",
                items=types.Schema(type=types.Type.STRING) # This tells it the array contains strings
            ),
        },
        required=["file_path"]
    ),
)

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        
        # Safely combine the working directory and the requested file path
        target_file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        # Verify the target file is actually inside the working directory
        valid_target = os.path.commonpath([working_dir_abs, target_file_abs]) == working_dir_abs
        if not valid_target:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        # 1. Check if the file is a python file
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
            
        # 2. Build the command list
        command = ["python", target_file_abs]
        if args is not None:
            command.extend(args)
            
        # 3. Run the subprocess
        result = subprocess.run(
            command,
            cwd=working_dir_abs, # Set the working directory
            capture_output=True, # Capture stdout and stderr
            text=True,           # Decode output to strings
            timeout=30           # 30-second timeout
        )
        
        # 4. Format the output string
        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
            
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        else:
            if result.stdout:
                output.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output.append(f"STDERR:\n{result.stderr}")
                
        return "\n".join(output)
        
    except Exception as e:
        return f"Error executing Python file: {e}"