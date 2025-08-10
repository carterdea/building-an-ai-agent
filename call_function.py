from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

# Dictionary mapping function names to their implementations
FUNCTION_MAP = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(function_call_part, verbose=False):
    """
    Handle the execution of function calls from the LLM.

    Args:
        function_call_part: The function call object from the LLM response (types.FunctionCall)
        verbose: Whether to print verbose output

    Returns:
        types.Content object with the function execution result
    """
    function_name = function_call_part.name
    args = dict(function_call_part.args)  # Create a copy of the args dictionary

    # Set the working directory to ./calculator
    args["working_directory"] = "./calculator"

    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")

    # Check if function exists
    if function_name not in FUNCTION_MAP:
        # Return error Content for unknown function
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Get the function from the map and execute it
    func = FUNCTION_MAP[function_name]
    try:
        result = func(**args)
    except Exception as e:
        result = f"Error executing {function_name}: {str(e)}"

    print(f"\nResult:\n{result}")

    # Return successful Content
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )
