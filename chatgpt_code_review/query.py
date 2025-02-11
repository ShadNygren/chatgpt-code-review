import os
import logging
import time
import subprocess

from textwrap import dedent
from typing import Iterable

import openai
#from openai import OpenAI

import anthropic

from transformers import pipeline, set_seed

import tiktoken

#-------------------------------------------------




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


def run_pytype(filename):
    """Run pytype on the specified file and return the report as a string."""
    # Build the command to run pylint
    #command = ['pytype', filename, '--output-format=text']
    command = ['pytype', filename]
    
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Return the pylint output
    return result.stdout


def run_pylint(filename):
    """Run pylint on the specified file and return the report as a string."""
    # Build the command to run pylint
    command = ['pylint', filename, '--output-format=text']
    
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Return the pylint output
    return result.stdout


# Original renamed and suffixed since identical
def analyze_code_files(code_files: list[str], args, extensions: list[str] = None) -> Iterable[dict[str, str]]:
    """Analyze the selected code files and return recommendations."""
    return (analyze_code_file("/tmp/chatgpt-code-review/" + code_file, args=args, extensions=extensions) for code_file in code_files)

# This is the new version with support for local
# The original version was renamed and suffixed with _original
def analyze_code_file(code_file: str, args, extensions: list[str] = None) -> dict[str, str]:
    """Analyze a code file and return a dictionary with file information and recommendations."""
    print("ShadDEBUG -query.py analyze_code_file - args == " + str(args))
    with open(code_file, "r") as f:
        print("ShadDEBUG query.py - f.name = " + f.name)
        code_content = f.read()

    if not code_content:
        return {"code_file": code_file, "code_snippet": code_content, "recommendation": "No code found in file"}

    pylint_report = run_pylint(code_file)
    #print(pylint_report)
    pytype_report = run_pytype(code_file)

    analysis = None
    try:
        logging.info("Analyzing code file: %s", code_file)
        print("ShadDEBUG - query.py - code content = " + code_content)
        print("ShadDEBUG - query.py - extensions = " + str(extensions))
        #use_local_model = False
        if "llama" in args:
            print("ShadDEBUG - get_local_code_analysis in query.py")
            analysis = get_local_code_analysis(code=code_content, pylint_report=pylint_report, pytype_report=pytype_report)
        else:
            print("ShadDEBUG - query.py - get_code_analysis in query.py - NOT Using Llama")
            print("ShadDEBUG - query.py - FORCE THE USE OF ANTHROPIC")
            analysis = get_code_analysis_anthropic(code=code_content, pylint_report=pylint_report, pytype_report=pytype_report)
            if "anthropic" in args:
                print("ShadDEBUG - query.py - get_code_analysis in query.py - Using Anthropic")
                analysis = get_code_analysis_anthropic(code=code_content, pylint_report=pylint_report, pytype_report=pytype_report)
            elif "openai" in args:
                print("ShadDEBUG - query.py - get_code_analysis in query.py - Using OpenAI")
                analysis = get_code_analysis_openai(code=code_content, pylint_report=pylint_report, pytype_report=pytype_report)
        print("ShadDEBUG - query.py - get_code_analysis in query.py - Got analysis")    
    except Exception as e:
        print("ShadDEBUG Exception e = " + str(e))
        logging.error("Error analyzing code file: %s", code_file)
        analysis = f"Error analyzing code file: {e}"

    return {"code_file": code_file, "code_snippet": code_content, "recommendation": analysis}

# This is new for local
def get_local_code_analysis(code: str, pylint_report: str, pytype_report: str) -> str:
    """Analyze code using a local model."""
    generator = pipeline('text-generation', model=MODEL_NAME, device=0)  # device=0 for GPU
    set_seed(42)

    prompt = dedent(f"""\
        {generate_analysis_prompt(code=code, pylint_report=pylint_report, pytype_report=pytype_report)}
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

def generate_analysis_prompt(code: str, pylint_report: str, pytype_report: str) -> str:
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

        PyType Report:
        ```
        {pytype_report}
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
def get_num_tokens_from_messages(messages, model: str):
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




def get_code_analysis_openai(code: str, pylint_report: str, pytype_report: str) -> str:
    """Get code analysis from the OpenAI API."""
    print("ShadDEBUG - get_code_analysis 1")

    #client_openai = OpenAI()
    # Assuming `client_openai` setup for OpenAI is correct
    client_openai = openai.OpenAI()

    prompt = generate_analysis_prompt(code=code, pylint_report=pylint_report, pytype_report=pytype_report)
    print("ShadDEBUG - get_code_analysis 2")

    #model="gpt-3.5-turbo"
    model="gpt-4-turbo-preview"
    
    messages = [{"role": "system", "content": prompt}]
    print("ShadDEBUG - get_code_analysis 2a")
    tokens_in_messages = get_num_tokens_from_messages(
        messages=messages, model=model
    )
    
    print("ShadDEBUG - get_code_analysis 2b")
    max_tokens = 4096
    #max_tokens = 32000
    
    tokens_for_response = max_tokens - tokens_in_messages

    print("ShadDEBUG - get_code_analysis 3")
    if tokens_for_response < 200:
        return "The code file is too long to analyze. Please select a shorter file."

    print("ShadDEBUG - get_code_analysis 4")
    logging.info("Sending request to OpenAI API for code analysis")
    logging.info("Max response tokens: %d", tokens_for_response)
    print("ShadDEBUG - get_code_analysis 5")
    response = client_openai.chat.completions.create(model=model,
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






def get_code_analysis_anthropic(code: str, pylint_report: str, pytype_report: str) -> str:
    """Get code analysis from the Ahtoropic API."""
    print("ShadDEBUG - get_code_analysis 1")

    client_anthropic = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHTOPIC_API_KEY")
        api_key="my_anthropic_api_key"
    )

    prompt = generate_analysis_prompt(code=code, pylint_report=pylint_report, pytype_report=pytype_report)
    print("ShadDEBUG - get_code_analysis 2")

    model="claude-3-sonnet-20240229"
    
    # This was the original for openai from the original code repo
    #messages = [{"role": "system", "content": prompt}]
    #
    # This is from anthropic documentation
    # https://docs.anthropic.com/claude/docs/upgrading-from-the-text-completions-api
    messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]

#    print("ShadDEBUG - get_code_analysis 2a")
#    tokens_in_messages = get_num_tokens_from_messages(
#        messages=messages, model=model
#    )
#    
#    print("ShadDEBUG - get_code_analysis 2b")
#    max_tokens = 4096
#    #max_tokens = 32000
#    
#    tokens_for_response = max_tokens - tokens_in_messages
    tokens_for_response = 4096
#
#    print("ShadDEBUG - get_code_analysis 3")
#    if tokens_for_response < 200:
#        return "The code file is too long to analyze. Please select a shorter file."

    print("ShadDEBUG - get_code_analysis 4")
    logging.info("Sending request to OpenAI API for code analysis")
#    logging.info("Max response tokens: %d", tokens_for_response)
    print("ShadDEBUG - get_code_analysis 5")
    response = client_anthropic.messages.create(model=model,
        messages=messages,
        system="You are an expert at doing software code reviews for the Python language",
        max_tokens=tokens_for_response,
        temperature=0)
    print("ShadDEBUG - query.py - get_code_analysis 6 - response == " + str(response))
    logging.info("Received response from OpenAI API")

    print("ShadDEBUG - query.py - get_code_analysis 7 - response.content == " + str(response.content))
    # Get the assistant's response from the API response
    assistant_response = response.content

    print("ShadDEBUG - query.py - get_code_analysis 8 - assistant_response.strip() == " + str(assistant_response.strip()))
    exit()
    return assistant_response.strip()
