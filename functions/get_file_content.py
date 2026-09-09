import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the content of a file. Use this when the user wants to view or inspect the contents of a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    """
    Reads the content of a file inside the permitted working directory.
    Returns the content as a string (truncated if too large) or an error message.
    """
    try:
        # Absolute path of the base working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Resolve the full target path, normalising any '..' or '.' segments
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Check if the target file is inside the working directory
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check that the target exists and is a regular file
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read the file, up to MAX_CHARS
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read(MAX_CHARS)
            # Check if there is more data
            extra = f.read(1)
            if extra:
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f'Error: {str(e)}'
