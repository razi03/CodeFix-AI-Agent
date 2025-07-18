import os
from google.generativeai import types

def write_file(file_path: str, content: str, working_directory: str | None = None) -> str:
    # Prepend working_directory if provided
    if working_directory:
        file_path = os.path.join(working_directory, file_path)

    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f'✅ Success: Wrote to "{file_path}"'
    except Exception as e:
        return f"❌ Error writing to file: {str(e)}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites content to a specified file.",
    parameters={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to write to, relative to the working directory.",
            },
            "content": {
                "type": "string",
                "description": "The content to write to the file.",
            }
        },
        "required": ["file_path", "content"]
    }
)
