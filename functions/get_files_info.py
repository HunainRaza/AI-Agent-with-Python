import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
            name="get_files_info",
            description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "directory": types.Schema(
                        type=types.Type.STRING,
                        description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
                    ),
                },
            ),
        )

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
                
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        file_lines = []
        
        for file in os.listdir(target_dir):
            # Get the full path of the item to check its size and if it's a dir
            item_path = os.path.join(target_dir, file)
            filesize = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            
            # Add the formatted string to our list
            file_lines.append(f'- {file}: file_size={filesize} bytes, is_dir={is_dir}')
        
        return "\n".join(file_lines)
    
    except Exception as e:
        return f'Error: {str(e)}'