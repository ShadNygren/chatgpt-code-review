import os
import logging
import time
import subprocess

from textwrap import dedent
from typing import Iterable

import openai
#from openai import OpenAI

from transformers import pipeline, set_seed

import tiktoken

#-------------------------------------------------

#client = OpenAI()
# Assuming `client` setup for OpenAI is correct
client = openai.OpenAI()

#-------------------------------------------------
# New Stuff for Local
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

# Add this line if you're using a specific model, like CodeLlama, from Hugging Face
#MODEL_NAME = "YourModelNameHere"  # Example: "EleutherAI/gpt-neo-2.7B"
MODEL_NAME = "WizardLM/WizardLM-13B-V1.2"

# Using original as implementation remains the same
#def get_num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
#    # Implementation remains the same
#    pass


def run_pylint(filename):
    """Run pylint on the specified file and return the report as a string."""
    # Build the command to run pylint
    command = ['pylint', filename, '--output-format=text']
    
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Return the pylint output
    return result.stdout


# Original renamed and suffixed since identical
def analyze_code_files(code_files: list[str]) -> Iterable[dict[str, str]]:
    """Analyze the selected code files and return recommendations."""
    return (analyze_code_file("/tmp/chatgpt-code-review/" + code_file) for code_file in code_files)

# This is the new version with support for local
# The original version was renamed and suffixed with _original
def analyze_code_file(code_file: str, use_local_model=False) -> dict[str, str]:
    """Analyze a code file and return a dictionary with file information and recommendations."""
    with open(code_file, "r") as f:
        print("ShadDEBUG f.name = " + f.name)
        code_content = f.read()

    if not code_content:
        return {"code_file": code_file, "code_snippet": code_content, "recommendation": "No code found in file"}

    pylint_report = run_pylint(code_file)
    #print(pylint_report)
    try:
        logging.info("Analyzing code file: %s", code_file)
        print("ShadDEBUG - code content = " + code_content)
        if use_local_model:
            print("ShadDEBUG - get_local_code_analysis in query.py")
            analysis = get_local_code_analysis(code_content, pylint_report)
        else:
            print("ShadDEBUG - get_code_analysis in query.py")
            analysis = get_code_analysis(code_content, pylint_report)
    except Exception as e:
        print("ShadDEBUG Exception e = " + str(e))
        logging.error("Error analyzing code file: %s", code_file)
        analysis = f"Error analyzing code file: {e}"

    return {"code_file": code_file, "code_snippet": code_content, "recommendation": analysis}

# This is new for local
def get_local_code_analysis(code: str, pylint_report: str) -> str:
    """Analyze code using a local model."""
    generator = pipeline('text-generation', model=MODEL_NAME, device=0)  # device=0 for GPU
    set_seed(42)

    prompt = dedent(f"""\
        {generate_analysis_prompt(code, pylint_report)}
    """)

    responses = generator(prompt, max_length=500, num_return_sequences=1)
    analysis = responses[0]['generated_text']
    
    # Process the analysis as needed to fit your output format
    return analysis.strip()

# Using original since implementation remains the same
#def get_code_analysis(code: str) -> str:
#    """Get code analysis from the OpenAI API. Implementation remains the same."""
#    pass

def read_prompt_from_file(filename):
    with open(filename, "r") as file:
        return file.read().strip()

def generate_analysis_prompt(code: str, pylint_report) -> str:
    """Generates a prompt for analyzing code. Can be shared by both OpenAI and local model functions."""
    # This function generates the prompt text that you were previously creating in get_code_analysis.
    # Refactor prompt generation here to avoid repetition.
    #prompt = read_prompt_from_file("prompt.txt")
    prompt = dedent(
        f"""\
        Please review the code below and identify any syntax or logical errors, suggest
        ways to refactor and improve code quality, enhance performance, address security
        concerns, and align with best practices. Provide specific examples for each area
        and limit your recommendations to three per category.

        Use the following response format, keeping the section headings as-is, and provide
        your feedback. Use bullet points for each response. The provided examples are for
        illustration purposes only and should not be repeated.

        **Syntax and logical errors (example)**:
        - Incorrect indentation on line 12
        - Missing closing parenthesis on line 23

        **Code refactoring and quality (example)**:
        - Replace multiple if-else statements with a switch case for readability
        - Extract repetitive code into separate functions

        **Performance optimization (example)**:
        - Use a more efficient sorting algorithm to reduce time complexity
        - Cache results of expensive operations for reuse

        **Security vulnerabilities (example)**:
        - Sanitize user input to prevent SQL injection attacks
        - Use prepared statements for database queries

        **Best practices (example)**:
        - Add meaningful comments and documentation to explain the code
        - Follow consistent naming conventions for variables and functions

        Code:
        ```
        {code}
        ```

        PyLint Report:
        ```
        {pylint_report}
        ```

        Your review:"""
    )
    #pass
    return prompt

# Update the part where you call analyze_code_file to include use_local_model based on user's choice.

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# End New Stuff for Local
#-------------------------------------------------
# Original Stuff
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

# Define the function if it's not already imported from somewhere else
def get_num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
    """
    Calculate the number of tokens used by a list of messages.

    This is a simplified implementation. You might need to adjust
    it based on your actual requirements and the specifics of how
    the messages are structured and tokenized.
    """
    print("ShadDEBUG - get_num_tokens_from_messages 1")
    # Assuming 'tiktoken' can provide an encoding for the specified model,
    # and you've instantiated it correctly elsewhere in your code.
    encoding = tiktoken.encoding_for_model(model)
    print("ShadDEBUG - get_num_tokens_from_messages 2")
    num_tokens = 0
    for message in messages:
        print("ShadDEBUG - get_num_tokens_from_messages 2a str(message) = " + str(message))
        content = message.get("content", "")
        print("ShadDEBUG - get_num_tokens_from_messages 2b content = " + content)
        num_tokens += len(encoding.encode(content))
        print("ShadDEBUG - get_num_tokens_from_messages 2c")
    print("ShadDEBUG - get_num_tokens_from_messages 3")
    return num_tokens


def analyze_code_files_original(code_files: list[str]) -> Iterable[dict[str, str]]:
    """Analyze the selected code files and return recommendations."""
    return (analyze_code_file(code_file) for code_file in code_files)

# Renamed and suffixed with _original
def analyze_code_file_original(code_file: str) -> dict[str, str]:
    """Analyze a code file and return a dictionary with file information and recommendations."""
    with open(code_file, "r") as f:
        code_content = f.read()
        print("ShadDEBUG")
        print("ShadDEBUG code_content = " + code_content)

    if not code_content:
        return {
            "code_file": code_file,
            "code_snippet": code_content,
            "recommendation": "No code found in file",
        }

    try:
        logging.info("Analyzing code file: %s", code_file)
        analysis = get_code_analysis(code_content)
    except Exception as e:
        logging.info("Error analyzing code file: %s", code_file)
        analysis = f"Error analyzing code file: {e}"

    return {
        "code_file": code_file,
        "code_snippet": code_content,
        "recommendation": analysis,
    }


def get_code_analysis(code: str) -> str:
    """Get code analysis from the OpenAI API."""
    print("ShadDEBUG - get_code_analysis 1")
    prompt = generate_analysis_prompt(code=code, pylint_report=pylint_report)
    print("ShadDEBUG - get_code_analysis 2")

    model="gpt-3.5-turbo"
    #model="gpt-4-turbo-preview"
    messages = [{"role": "system", "content": prompt}]
    print("ShadDEBUG - get_code_analysis 2a")
    tokens_in_messages = get_num_tokens_from_messages(
        messages=messages, model=model
    )
    print("ShadDEBUG - get_code_analysis 2b")
    max_tokens = 4096
    tokens_for_response = max_tokens - tokens_in_messages

    print("ShadDEBUG - get_code_analysis 3")
    if tokens_for_response < 200:
        return "The code file is too long to analyze. Please select a shorter file."

    print("ShadDEBUG - get_code_analysis 4")
    logging.info("Sending request to OpenAI API for code analysis")
    logging.info("Max response tokens: %d", tokens_for_response)
    print("ShadDEBUG - get_code_analysis 5")
    response = client.chat.completions.create(model=model,
        messages=messages,
        max_tokens=tokens_for_response,
        n=1,
        temperature=0)
    print("ShadDEBUG - get_code_analysis 6")
    logging.info("Received response from OpenAI API")

    print("ShadDEBUG - get_code_analysis 7")
    # Get the assistant's response from the API response
    assistant_response = response.choices[0].message.content

    print("ShadDEBUG - get_code_analysis 8")
    return assistant_response.strip()
