import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function

load_dotenv()

def main():
    try:
        api_key = os.environ.get("GEMINI_API_KEY")

        if api_key is None:
            raise RuntimeError("GEMINI_API_KEY environment variable not found. Please ensure it is set in your .env file.")

        parser = argparse.ArgumentParser(description="Chatbot")
        parser.add_argument("user_prompt", type=str, help="User prompt")
        parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
        args = parser.parse_args()

        messages: list[types.Content] = [
            types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
        ]

        client = genai.Client(api_key=api_key)
        # The Agent Loop!
        for i in range(20):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
            )
            
            # 1. Add the model's response to the conversation history
            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)

            if args.verbose:
                prompt_tokens = response.usage_metadata.prompt_token_count
                response_tokens = response.usage_metadata.candidates_token_count
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {prompt_tokens}")
                print(f"Response tokens: {response_tokens}")

            # Check if the LLM decided to call any functions
            if response.function_calls:
                function_results = []
                
                for function_call in response.function_calls:
                    function_call_result = call_function(function_call=function_call, verbose=args.verbose)
                    
                    # Validation checks
                    if not function_call_result.parts:
                        raise ValueError("Function call result has no parts.")
                        
                    function_response = function_call_result.parts[0].function_response
                    if not function_response:
                        raise ValueError("Function call result has no function_response.")
                        
                    if not function_response.response:
                        raise ValueError("Function call result has no response field.")
                        
                    # Add to our list for later use
                    function_results.append(function_call_result.parts[0])
                    
                    if args.verbose:
                        print(f"-> {function_response.response}")
                        
                # 2. Add the executed function results back into the conversation history
                messages.append(types.Content(role="user", parts=function_results))
                
            else:
                # 3. No function calls? We are done! Print the final response and BREAK.
                print("Final response:")
                print(response.text)
                break
                
        else:
            # 4. If the loop runs 20 times and never breaks, it means the agent got stuck.
            print("Error: Agent reached maximum iterations without completing the task.")
            exit(1)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        exit(1)

# # 1. Check if the LLM decided to call a function!
# if response.function_calls:
#     for function_call in response.function_calls:
#         function_call_result = call_function(function_call=function_call)
#         print(f"Callinf function: {function_call_result}")
#         print(f"Calling function: {function_call.name}({function_call.args})")
# else:
#     # 2. If there are no function calls, print the text normally
#     print(response.text)
# def main():
#     print("Hello from ai-agent-with-python!")


if __name__ == "__main__":
    main()