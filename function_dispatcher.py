import os

# Import all tool implementations
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):
    """
    Executes the requested function from Gemini's tool call.
    
    Args:
        function_call_part: Gemini's function call object.
        verbose (bool): Whether to print detailed logs.

    Returns:
        str: Result or error message.
    """
    function_name = function_call_part.name
    args = dict(function_call_part.args or {})

    # Always print this exact line for CLI test detection
    print(f" - Calling function: {function_name}")

    # Inject working_directory for file-related tools if missing
    if function_name in {"get_files_info", "get_file_content", "run_python_file", "write_file"} and "working_directory" not in args:
        args["working_directory"] = "./calculator"

    # Map tool function names to actual implementations
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    func = function_map.get(function_name)
    if not func:
        error_msg = f"❌ Error: Unknown function: {function_name}"
        if verbose:
            print(error_msg)
        return error_msg

    try:
        result = func(**args)
        if verbose:
            print(f"✅ Function output:\n{result}")
        return result
    except Exception as e:
        error_msg = f"❌ Error calling function '{function_name}': {str(e)}"
        if verbose:
            print(error_msg)
        return error_msg
