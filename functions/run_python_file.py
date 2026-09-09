import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file within the working directory with optional arguments. Use this when the user wants to run or execute a Python script, e.g., 'run main.py'.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of command-line arguments to pass to the script",
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    """
    Runs a Python file inside the permitted working directory.
    Returns the combined stdout/stderr output or an error message.
    """
    try:
        # Resolve paths
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Validate that target is inside working directory
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check existence and that it's a regular file
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Check file extension
        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        # Build command
        command = ["python", target_file]
        if args:
            command.extend(args)

        # Run the subprocess with timeout and output capture
        result = subprocess.run(
            command,
            cwd=working_dir_abs,          # ensure we're in the working directory
            capture_output=True,
            text=True,
            timeout=30
        )

        # Assemble output string
        output_parts = []
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append("STDOUT:")
                output_parts.append(result.stdout.rstrip())
            if result.stderr:
                output_parts.append("STDERR:")
                output_parts.append(result.stderr.rstrip())

        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return "Error: executing Python file: Timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"
