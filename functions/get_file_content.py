import os
import sys
from google.genai import types

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MAX_FILE_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)


def get_file_content(working_directory, file_path):
    try:
        # Create full path and normalize it
        full_path = os.path.join(working_directory, file_path)
        full_path = os.path.abspath(full_path)

        # Normalize the working directory path
        working_directory = os.path.abspath(working_directory)

        # Check if the path is within the working directory
        if not full_path.startswith(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if the path is a file
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read the file content with truncation
        with open(full_path, "r") as f:
            content = f.read(MAX_FILE_CHARS + 1)

        # Check if content was truncated
        if len(content) > MAX_FILE_CHARS:
            content = (
                content[:MAX_FILE_CHARS]
                + f'[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'
            )

        return content
    except Exception as e:
        return f"Error: {str(e)}"
