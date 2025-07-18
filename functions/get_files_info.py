import os
from google.generativeai import types

def get_files_info(directory: str = ".", working_directory: str | None = None) -> str:
    """
    Lists files and directories in the specified path, including size and directory flag.

    Args:
        directory (str): Directory relative to working_directory to list files of.
        working_directory (str | None): Optional base directory to prepend.

    Returns:
        str: Multiline string with info about each file.
    """
    try:
        # Compose full path
        full_path = os.path.join(working_directory, directory) if working_directory else directory

        if not os.path.exists(full_path):
            return f'❌ Error: Directory "{directory}" does not exist.'
        if not os.path.isdir(full_path):
            return f'❌ Error: "{directory}" is not a directory.'

        files = os.listdir(full_path)
        result = []
        for f in sorted(files):  # sort alphabetically for consistent output
            path = os.path.join(full_path, f)
            try:
                is_dir = os.path.isdir(path)
                size = os.path.getsize(path) if not is_dir else 0
                result.append(f"{f}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as entry_error:
                result.append(f"{f}: ❌ Error retrieving info: {str(entry_error)}")

        return "\n".join(result)

    except Exception as e:
        return f"❌ Error: {str(e)}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory with file size and type info.",
    parameters={
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "The directory to list files from, relative to the working directory."
            }
        },
        "required": ["directory"]
    }
)
