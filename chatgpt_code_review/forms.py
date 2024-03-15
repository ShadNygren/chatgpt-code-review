import logging
import os
import openai
import repo
from utils import EXTENSION_TO_LANGUAGE_MAP

class RepoForm:
    """A class to manage repository form operations without Streamlit."""
    def __init__(self, repo_url: str, api_key: str, extensions: list[str], additional_extensions: str = ""):
        self.repo_url = repo_url
        self.api_key = api_key
        self.extensions = extensions
        if additional_extensions:
            self.extensions.extend([ext.strip() for ext in additional_extensions.split(",")])

        # Validate API key
        if not self.is_api_key_valid():
            raise ValueError("Invalid OpenAI API key.")

    def is_api_key_valid(self):
        """Checks if the OpenAI API key is valid."""
        return bool(self.api_key)

class AnalyzeFilesForm:
    """A class to manage file analysis operations without Streamlit."""
    def __init__(self, repo_url: str, extensions: list[str]):
        self.repo_url = repo_url
        self.extensions = extensions
        self.selected_files = []
    
    def analyze_files(self):
        """Analyzes files from a repository."""
        # Assuming repo.list_code_files_in_repository and other necessary logic
        # are adapted to work without Streamlit.
        code_files = repo.list_code_files_in_repository(self.repo_url, self.extensions)
        if not code_files:
            logging.error("No code files found.")
            return []
        
        self.selected_files = code_files  # This simplifies the example. Adjust according to your logic.
        # Here you would typically call the analysis function and return its results.
        return self.selected_files

# Example usage
if __name__ == "__main__":
    repo_url = "https://github.com/example/repo"
    api_key = os.getenv("OPENAI_API_KEY", "")
    extensions = [".py", ".js"]
    additional_extensions = ""

    # Create forms with direct parameters
    repo_form = RepoForm(repo_url, api_key, extensions, additional_extensions)
    analyze_form = AnalyzeFilesForm(repo_url, extensions)

    # Example: Analyze files
    analysis_results = analyze_form.analyze_files()
    print(analysis_results)
