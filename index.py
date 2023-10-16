import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Load the API credentials from your JSON key file
credentials = service_account.Credentials.from_service_account_file(
    'rsronic.json',
    scopes=['https://www.googleapis.com/auth/indexing']
)

# Create the API client
indexing_api = build('indexing', 'v3', credentials=credentials)

# List of URLs to be indexed
urls_to_index = [
    'https://www.rstronic-angers.com/',
    'https://www.rstronic-angers.com/boitier-ethanol-cholet-saumur-segre/',
    'https://www.rstronic-angers.com/reprogrammation-moteur-preparation-autos-motos-trucks-engins-agricoles/',
    # Add more URLs as needed
]

for url_to_index in urls_to_index:
    try:
        result = indexing_api.urlNotifications().publish(
            body={'url': url_to_index,
                  'type': 'URL_UPDATED'}
        ).execute()
        print(f"Indexing request for {url_to_index}: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Error submitting indexing request for {url_to_index}: {str(e)}")
