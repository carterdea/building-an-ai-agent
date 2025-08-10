import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from prompts import system_prompt
from call_function import available_functions, call_function

def generate_content(client, prompt, verbose=False):
    """Generate content using the Gemini API with function calling support."""
    if verbose:
        print(f"User prompt: {prompt}")
    
    messages = [prompt]

    max_iterations = 20
    for iteration in range(max_iterations):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], 
                    system_instruction=system_prompt
                )
            )
            
            for candidate in response.candidates:
                messages.append(candidate.content)
            
            has_function_calls = False
            if response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        has_function_calls = True
                        break
            
            if not has_function_calls and response.candidates[0].content.parts:
                text_parts = []
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'text') and part.text:
                        text_parts.append(part.text)
                
                if text_parts:
                    final_text = '\n'.join(text_parts)
                    print(final_text)
                    if verbose:
                        print(f"\nCompleted in {iteration + 1} iteration(s)")
                    break
            
            if response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        function_call_result = call_function(part.function_call, verbose)
                        
                        if not (function_call_result.parts and 
                                len(function_call_result.parts) > 0 and
                                hasattr(function_call_result.parts[0], 'function_response') and
                                hasattr(function_call_result.parts[0].function_response, 'response')):
                            raise RuntimeError(f"Invalid function call result structure from {part.function_call.name}")
                        
                        if verbose:
                            print(f"-> {function_call_result.parts[0].function_response.response}")
                        
                        messages.append(function_call_result)
            
        except Exception as e:
            print(f"Error during generation: {str(e)}")
            if verbose:
                import traceback
                traceback.print_exc()
            break
    else:
        print(f"Warning: Reached maximum iterations ({max_iterations}) without completion")
    
    if verbose and response:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(f"Total tokens: {response.usage_metadata.total_token_count}")

def main():
    """Main function to handle CLI arguments and initialize the client."""
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables")
        sys.exit(1)
    
    client = genai.Client(api_key=api_key)
    
    if len(sys.argv) < 2:
        print("Usage: python main.py 'your prompt here' [--verbose]")
        sys.exit(1)
    
    verbose = "--verbose" in sys.argv
    if verbose:
        sys.argv.remove("--verbose")
    
    prompt = " ".join(sys.argv[1:])
    
    generate_content(client, prompt, verbose)

if __name__ == "__main__":
    main()
