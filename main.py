import os
import sys
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai

# Load env and API key
load_dotenv(find_dotenv())
api_key = os.getenv("GEMINI_API_KEY")
print("✅ Using API key:", api_key[:6] + "..." if api_key else "❌ No key loaded")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in .env")
    sys.exit(1)

# Get prompt and flags
if len(sys.argv) < 2:
    print("❌ Error: Please provide a prompt as a command line argument.")
    sys.exit(1)

verbose = "--verbose" in sys.argv
args_without_flags = [arg for arg in sys.argv[1:] if arg != "--verbose"]
user_prompt = " ".join(args_without_flags).strip()

# Import tool schemas and dispatcher
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from function_dispatcher import call_function

# Configure Gemini
genai.configure(api_key=api_key)

# System prompt with tool usage rules
system_prompt = """
You are a helpful AI coding agent with access to the following tools:

- get_files_info: List files and directories.
- get_file_content: Read the content of files.
- run_python_file: Execute Python files with optional arguments.
- write_file: Write or overwrite files.

Your workflow for answering code-related questions MUST follow this process:

1. First, call 'get_files_info' on the root directory to understand the project structure.
2. Then, use 'get_file_content' to inspect relevant files needed to answer the question.
3. Only after inspecting the necessary files, provide a final response.
4. If further action is needed, repeat the tool use until you're confident in your answer.

⚠️ Do NOT try to answer questions without inspecting the code with tools.
"""

# List of available tools
tools = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]

# Gemini model setup
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=tools,
    system_instruction=system_prompt,
)

def main():
    # Initial messages with bootstrap and user input
    messages = [
        {"role": "user", "parts": [{"text": "Start by listing the files in the root directory."}]},
        {"role": "user", "parts": [{"text": user_prompt}]}
    ]

    for step in range(20):  # Max 20 interaction steps
        try:
            response = model.generate_content(messages, stream=False)

            if verbose:
                print(f"\n🔁 Step {step+1} - Raw response:\n{response}")

            for candidate in response.candidates:
                content = candidate.content
                new_message = {"role": content.role, "parts": []}

                for part in content.parts:
                    if hasattr(part, "text") and part.text:
                        new_message["parts"].append({"text": part.text})
                    elif hasattr(part, "function_call") and part.function_call:
                        new_message["parts"].append({"function_call": part.function_call})

                messages.append(new_message)

                # Handle tool usage
                for part in new_message["parts"]:
                    if "function_call" in part:
                        func_call = part["function_call"]

                        if verbose:
                            print(f"\n🛠️ Calling tool: {func_call.name} with args: {func_call.args}")

                        result = call_function(func_call, verbose=verbose)

                        # Add tool result as model message
                        messages.append({
                            "role": "model",
                            "parts": [{"text": str(result)}]
                        })
                        break  # Continue feedback loop after tool call
                else:
                    # No tool call: Final output
                    final_text = new_message["parts"][0].get("text", "✅ Done")
                    print("\n🧠 Final response:\n" + final_text)
                    return

        except Exception as e:
            print(f"❌ Error in feedback loop: {str(e)}")
            break

if __name__ == "__main__":
    main()
