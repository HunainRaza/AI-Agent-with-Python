import os
from google.genai import types

schema_write_file_content = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file",
            ),
        },
        required=["file_path", "content"]
    ),
)

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        
        # Safely combine the working directory and the requested file path
        target_file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        # Verify the target file is actually inside the working directory
        valid_target = os.path.commonpath([working_dir_abs, target_file_abs]) == working_dir_abs
        if not valid_target:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_file_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        # 2. Create parent directories if they don't exist
        os.makedirs(os.path.dirname(target_file_abs), exist_ok=True)
        
        with open(target_file_abs, "w", encoding="utf-8") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f'Error: {str(e)}'
    