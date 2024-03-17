import os
import about
import display
import download
import forms
import query
import repo
import utils

env_file_path = ".env"
log_file = "app.log"
temp_dir = "/tmp/chatgpt-code-review"

#def analyze_repo(repo_url, extensions, openai_api_key):
def analyze_repo(repo_url, extensions, args):
    print("ShadDEBUG: before utils", flush=True)
    utils.load_environment_variables(env_file_path)
    utils.set_environment_variables()
    utils.configure_logging(log_file)

    recommendations = []

    with utils.TempDirContext(temp_dir):
        # Assuming the OpenAI API key and other necessary settings are handled appropriately within utils and other modules.
        
        print("repo_url = " + repo_url)
        print("extensions = " + str(extensions))
        # Clone the repository and list code files
        print("ShadDEBUG about to list_code_files_in_repository", flush=True)
        code_files = repo.list_code_files_in_repository(repo_url, extensions)
        
        if not code_files:
            return {"error": "No code files found with the specified extensions."}

        # Analyze the selected files
        selected_files = code_files  # Assuming you want to analyze all files found
        recommendations = query.analyze_code_files(selected_files, extensions, args)

    # Format the recommendations for output
    recommendation_list = []
    for rec in recommendations:
        formatted_recommendation = {
            "file": rec["code_file"],
            "recommendation": rec["recommendation"] or "No recommendations",
            "code_snippet": rec["code_snippet"]  # Consider including more details as needed
        }
        recommendation_list.append(formatted_recommendation)

    return recommendation_list

if __name__ == "__main__":
    # Example usage - this part will not be used in CLI or Lambda but is here for demonstration.
    repo_url = "https://github.com/your/repo"
    extensions = [".py", ".js"]  # Example extensions
    openai_api_key = "your_openai_api_key_here"
    results = analyze_repo(repo_url, extensions, openai_api_key)
    print(results)
