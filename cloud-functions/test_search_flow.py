
import sys
import json
import logging
import os
from unittest.mock import MagicMock

# Mock flask module
mock_flask = MagicMock()
sys.modules['flask'] = mock_flask

# Mock Request class
class MockRequest:
    def __init__(self, json_data):
        self._json_data = json_data

    def get_json(self, silent=True):
        return self._json_data

mock_flask.Request = MockRequest

# Set environment variable to use mock data
os.environ['USE_MOCK_DATA'] = 'true'

# Now import main
try:
    import main
except ImportError as e:
    print(f"Failed to import main: {e}")
    sys.exit(1)

def test_search_flow():
    print("=== DialogFlow CX Search Flow Tester ===")
    print("This tool simulates a webhook request for book searches.")
    print("Type 'quit' to exit.")
    print("========================================")
    
    while True:
        query = input("\nEnter book title (or 'quit'): ").strip()
        if query.lower() == 'quit':
            break
            
        if not query:
            continue
            
        print(f"\nSearching for: {query}...")
    
        # Construct a sample Dialogflow CX webhook request
        request_json = {
            "sessionInfo": {
                "session": "projects/project-id/locations/location-id/agents/agent-id/sessions/test-session",
                "parameters": {
                    "book_title": query,
                    "search_type": "general"
                }
            },
            "intentInfo": {
                "lastMatchedIntent": "projects/project-id/locations/location-id/agents/agent-id/intents/intent-id",
                "displayName": "book.search"
            },
            "pageInfo": {
                "currentPage": {
                    "displayName": "Search Page",
                    "name": "projects/project-id/locations/location-id/agents/agent-id/flows/flow-id/pages/page-id"
                },
                "currentFlow": {
                    "displayName": "Book Search Flow",
                    "name": "projects/project-id/locations/location-id/agents/agent-id/flows/flow-id"
                }
            }
        }
        
        try:
            request = MockRequest(request_json)
            
            # Call the webhook handler
            response = main.handle_webhook(request)
            
            # Extract and print readable response
            messages = response.get('fulfillmentResponse', {}).get('messages', [])
            
            print("\n--- RESPONSE ---")
            for msg in messages:
                if 'text' in msg:
                    print(f"Message: {msg['text']['text'][0]}")
                elif 'listSelect' in msg: # List response in v3beta1/CX might be different structure in helper, checking utils.py
                    # utils.py create_list_response returns {'listSelect': {'items': ...}} which is correct for CX custom payload or similar
                    # Check utils.py again
                    pass
            
            # Print full JSON for debugging
            # print(json.dumps(response, indent=2))
            
            # Helper to print rich content
            if 'fulfillmentResponse' in response:
                 # Check for list
                 for msg in response['fulfillmentResponse'].get('messages', []):
                     if 'payload' in msg and 'richContent' in msg['payload']:
                         # This handles standard CX custom payloads if they were used
                         pass
                     # Check for the specific structure used in utils.py
                     if 'listSelect' in msg:
                         print("Lists:")
                         for item in msg['listSelect'].get('items', []):
                             print(f" - {item.get('title')}: {item.get('description')}")
            
        except Exception as e:
            print(f"Error during test: {e}")

if __name__ == "__main__":
    test_search_flow()
