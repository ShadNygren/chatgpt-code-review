import json
from your_refactored_app import app

def lambda_handler(event, context):
    # Assuming the event is a JSON object with 'repo_url', 'extensions', and 'openai_api_key' keys.
    
    # Extract parameters from the event object
    repo_url = event.get('repo_url')
    extensions = event.get('extensions', [])  # Default to an empty list if not provided
    openai_api_key = event.get('openai_api_key')
    
    if not repo_url or not openai_api_key:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing required parameters: `repo_url` and `openai_api_key`')
        }
    
    try:
        # Call the refactored app function with parameters extracted from the event
        results = app(repo_url=repo_url, extensions=extensions, openai_api_key=openai_api_key)
        
        # Return the results as a JSON response
        return {
            'statusCode': 200,
            'body': json.dumps(results)
        }
    except Exception as e:
        # Handle exceptions and return a 500 error response
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error processing your request: {str(e)}')
        }
