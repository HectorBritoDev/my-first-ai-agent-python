import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")


    for _ in range(20):
        response = generate_content(client, messages, args.verbose)

        if response is None:
            print('execution completed')
            exit()

        model_respose = response['model_response']

        
        if len(model_respose.candidates) > 0:
            for candidate in model_respose.candidates:
                messages.append(
                     candidate.content
                )
        
        messages.append(types.Content(role="user", parts=response['function_responses']))



def generate_content(client, messages, verbose):
    model_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if not model_response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if verbose:
        print("Prompt tokens:", model_response.usage_metadata.prompt_token_count)
        print("Response tokens:", model_response.usage_metadata.candidates_token_count)

    if not model_response.function_calls:
        print("Response:")
        print(model_response.text)
        return

    function_responses = []
    for function_call in model_response.function_calls:
        result = call_function(function_call, verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_responses.append(result.parts[0])

    return {"model_response": model_response, "function_responses": function_responses}

if __name__ == "__main__":
    main()
