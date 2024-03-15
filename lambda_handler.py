import json
# Ensure the import statement matches the actual module and function name after refactoring
from your_refactored_app import analyze_repo

def lambda_handler(event, context):
    # Extract parameters from the event object
    repo_url = event.get('repo_url')
    extensions = event.get('extensions', [])  # Default to an empty list if not provided
    openai_api_key = event.get('openai_api_key')
    
    # Validate required parameters
    if not repo_url or not openai_api_key:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing required parameters: `repo_url` and `openai_api_key`.')
        }
    
    try:
        # Call the refactored analysis function
        results = analyze_repo(repo_url=repo_url, extensions=extensions, openai_api_key=openai_api_key)
        
        # Format and return the results as a JSON response
        return {
            'statusCode': 200,
            'body': json.dumps(results, ensure_ascii=False)
        }
    except Exception as e:
        # Handle exceptions and provide a meaningful error response
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error processing your request: {str(e)}')
        }
