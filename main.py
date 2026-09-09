import os
import argparse
import sys
from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from functions.schemas import available_tools
from functions.call_function import call_function


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("OPENROUTER_API_KEY not found in environment. Please set it in a .env file.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    # Agent loop: maximum 20 iterations
    for iteration in range(20):
        if args.verbose:
            print(f"\n--- Iteration {iteration + 1} ---")

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_tools,
            temperature=0,
        )

        if response.usage is None:
            raise RuntimeError("Usage information missing in response. The API request may have failed.")

        if args.verbose:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        # Get the assistant's message and add it to the conversation history
        message = response.choices[0].message
        messages.append(message)  # stores the assistant's turn

        # Check if the model requested tool calls
        if message.tool_calls:
            for tool_call in message.tool_calls:
                # Execute the tool and get a tool message
                tool_result = call_function(tool_call, verbose=args.verbose)
                messages.append(tool_result)
            # Continue the loop so the model sees the tool results
            continue
        else:
            # No tool calls – this is the final answer
            print(message.content)
            return  # exit successfully

    # If we exit the loop without a final answer
    print("Error: Maximum iterations (20) reached without a final response.")
    sys.exit(1)


if __name__ == "__main__":
    main()