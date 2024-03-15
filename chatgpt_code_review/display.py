import re
from typing import Optional

from utils import EXTENSION_TO_LANGUAGE_MAP

# This function remains unchanged as it does not depend on Streamlit
def extension_to_language(file_extension: str) -> Optional[str]:
    """Return the programming language corresponding to a given file extension."""
    return EXTENSION_TO_LANGUAGE_MAP.get(file_extension.lower(), None)

# Modify this function to simply return the markdown code
def display_code(code: str, extension: str) -> str:
    """Return the code snippet formatted as markdown in the specified language."""
    language = extension_to_language(extension)
    markdown_code = f"```{language}\n{code}\n```"
    return markdown_code

# This function remains unchanged as it does not depend on Streamlit
def escape_markdown(text: str) -> str:
    """Escape markdown characters in a string."""
    escape_chars = [
        "\\",
        "`",
        "*",
        "_",
        "{",
        "}",
        "[",
        "]",
        "(",
        ")",
        "#",
        "+",
        "-",
        ".",
        "!",
    ]
    regex = re.compile("|".join(map(re.escape, escape_chars)))
    return regex.sub(r"\\\g<0>", text)

# Assuming this function generates markdown for recommendations
# and does not directly depend on Streamlit for its core functionality
def generate_markdown(recommendations) -> str:
    markdown_str = "# ChatGPT Code Review Recommendations\n\n"

    for rec in recommendations:
        code_file = rec["code_file"]
        recommendation = rec["recommendation"] or "No recommendations"
        # Use escape_markdown to handle any markdown characters in file names or recommendations
        markdown_str += f"## {escape_markdown(code_file)}\n\n"
        markdown_str += f"{escape_markdown(recommendation)}\n\n"

    return markdown_str
