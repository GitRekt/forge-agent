import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import MAX_ITERS
from prompts import system_prompt
from functions.call_function import available_functions, call_function

def main():
    parser = argparse.ArgumentParser(description="Gemini Chat")
    parser.add_argument(
        "content", type=str, help="User Prompt"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY env variable is not set.")

    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.content)])]
    
    # generate_content(args, client, messages)
    for _ in range(MAX_ITERS):
        text = generate_content(args, client, messages)
        if text:
            print("Final response:", text)
            return
        
    print(f"No text response received after {MAX_ITERS} iterations.")
    exit(1)


def generate_content(args, client: genai.Client, messages: list[types.Content]):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)
    
    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, args.verbose)

        if not function_call_result.parts:
            raise RuntimeError("Function call result has no parts")

        function_response = function_call_result.parts[0].function_response
        if function_response is None:
            raise RuntimeError("Function call result has no function response")

        if function_response.response is None:
            raise RuntimeError("Function call response payload is empty")

        if args.verbose:
            print(f"-> {function_response.response}")

        function_responses.append(function_call_result.parts[0])

    messages.append(types.Content(
            role="user",
            parts=function_responses)
    )
    # if not response.usage_metadata:
    #     raise RuntimeError("Gemini API response appears to be malformed.") 
    
    # if args.verbose:
    #     print("User prompt:", args.content)
    #     print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    #     print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    # if not response.function_calls:
    #     print("Response:", response.text)
    #     return
    


if __name__ == "__main__":
    main()
