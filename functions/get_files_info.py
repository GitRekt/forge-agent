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

def get_files_info(working_directory, directory="."):
    try:
        path=os.path.normpath(os.path.join(working_directory, directory))
        if os.path.commonpath([os.path.abspath(path), os.path.abspath(working_directory)]) != os.path.abspath(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(path):
            return f'Error: "{directory}" is not a directory'
        
        files=os.listdir(path)
        file_list=[]
        for filename in files:
            file_path=os.path.join(path,filename)
            is_dir=os.path.isdir(file_path)
            size=os.path.getsize(file_path)
            file_list.append(f'  - {filename}: file_size={size} bytes, is_dir={is_dir}')
        
        return "\n".join(file_list)
    
    except Exception as e:
        return f"Error: {str(e)}"
    
