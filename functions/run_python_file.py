import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file relative to the working directory and captures its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file relative to the working directory",
            )
        },
        required=["file_path"],
    )
)

def run_python_file(working_directory, file_path, args=None):
    path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(path, file_path))
    if os.path.commonpath([target_path, path]) != path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'
    command = ["python", os.path.abspath(target_path)]
    if args:
        command.extend(args)
    try:
        CompletedProcess = subprocess.run(command, cwd=path, capture_output=True, text=True, timeout=30)
        output = []
        if CompletedProcess.returncode != 0:
            output.append(f"Process exited with code {CompletedProcess.returncode}.")
        elif CompletedProcess.stdout=='' and CompletedProcess.stderr=='':
            output.append("No output produced.")
        else:
            output.append(f"STDOUT:\n{CompletedProcess.stdout}\nSTDERR:\n{CompletedProcess.stderr}")
    except Exception as e:
        return f"Error: executing Python file: {e}"
    return "\n".join(output)
