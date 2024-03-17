import argparse
import json
import logging
# Adjust the import path according to the actual location and name of the refactored function
from analyze_repo import analyze_repo

def main():
    logging.basicConfig(level=logging.INFO)  # Set up basic logging
    logging.info("ShadDEBUG before parse arguments")
    
    parser = argparse.ArgumentParser(description="ChatGPT Code Review CLI")
    parser.add_argument("--repo_url", required=True, help="GitHub Repository URL")
    parser.add_argument("--extensions", nargs='+', help="File extensions to analyze")
    parser.add_argument("--local", nargs="*")
    parser.add_argument("--openai", nargs="*")
    parser.add_argument("--anthropic", nargs="*")
    #parser.add_argument("--openai_api_key", required=True, help="OpenAI API Key")

    args = parser.parse_args()
    logging.info("ShadDEBUG after parse arguments - before results")

    # Call the refactored analyze_repo function
    #results = analyze_repo(repo_url=args.repo_url, extensions=args.extensions, openai_api_key=args.openai_api_key)
    results = analyze_repo(repo_url=args.repo_url, extensions=args.extensions)

    logging.info("ShadDEBUG after results")

    # Output the results
    # Here you could choose to format the output as pretty-printed JSON for better readability
    logging.info(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()

