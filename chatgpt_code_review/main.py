import argparse
import json
# Adjust the import path according to the actual location and name of the refactored function
from analyze_repo import analyze_repo

def main():
    print("ShadDEBUG before parse arguments")
    parser = argparse.ArgumentParser(description="ChatGPT Code Review CLI")
    parser.add_argument("--repo_url", required=True, help="GitHub Repository URL")
    parser.add_argument("--extensions", nargs='+', help="File extensions to analyze")
    parser.add_argument("--openai_api_key", required=True, help="OpenAI API Key")

    args = parser.parse_args()
    print("ShadDEBUG after parse arguments - before results")

    # Call the refactored analyze_repo function
    results = analyze_repo(repo_url=args.repo_url, extensions=args.extensions, openai_api_key=args.openai_api_key)
    print("ShadDEBUG after results")

    # Output the results
    # Here you could choose to format the output as pretty-printed JSON for better readability
    print(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()
