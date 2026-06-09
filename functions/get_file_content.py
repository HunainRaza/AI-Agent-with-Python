import os
from google.genai import types

schema_get_files_content = types.FunctionDeclaration(
            name="get_file_content",
            description="Read file contents",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="Path to the file to read, relative to the working directory",
                    ),
                },
                required=["file_path"]
            ),
        )

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        
        # Safely combine the working directory and the requested file path
        target_file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        # Verify the target file is actually inside the working directory
        valid_target = os.path.commonpath([working_dir_abs, target_file_abs]) == working_dir_abs
        if not valid_target:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        MAX_CHARS = 10000

        with open(target_file_abs, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
        
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                
        return content
    
    
    except Exception as e:
        return f'Error: str{e}'