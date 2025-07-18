import os
from google.generativeai import types

def get_file_content(file_path: str, working_directory: str | None = None) -> str:
    # Prepend working_directory if provided
    if working_directory:
        file_path = os.path.join(working_directory, file_path)

    if not os.path.isfile(file_path):
        return f'❌ Error: File "{file_path}" does not exist.'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"❌ Failed to read file: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a given file.",
    parameters={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to read, relative to the working directory.",
            }
        },
        "required": ["file_path"]
    }
)
