import os
import subprocess
from google.generativeai import types

def run_python_file(file_path: str, args: str = "", working_directory: str | None = None) -> str:
    # Prepend working directory if provided
    if working_directory:
        file_path = os.path.join(working_directory, file_path)

    if not os.path.isfile(file_path):
        return f'❌ Error: File "{file_path}" does not exist.'

    try:
        # Split args safely, handle empty string case
        args_list = args.split() if args else []

        result = subprocess.run(
            ["python", file_path, *args_list],
            text=True,
            capture_output=True,
            check=False,
            encoding="utf-8"
        )
        output = (result.stdout or "") + (result.stderr or "")
        return output.strip() if output.strip() else "No output returned."
    except Exception as e:
        return f"❌ Execution failed: {str(e)}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file and returns its output.",
    parameters={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The Python file to run, relative to the working directory.",
            },
            "args": {
                "type": "string",
                "description": "Optional arguments to pass to the script, as a space-separated string.",
            }
        },
        "required": ["file_path"]
    }
)
