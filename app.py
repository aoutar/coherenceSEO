from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import requests
import time
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
from openpyxl import Workbook
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET




app = Flask(__name__)


ALLOWED_EXTENSIONS = {'json'}

# Your existing code for indexing URLs
def index_urls(urls_to_index, credentials):
    indexing_api = build('indexing', 'v3', credentials=credentials)

    results = []

    for url_to_index in urls_to_index:
        try:
            result = indexing_api.urlNotifications().publish(
                body={'url': url_to_index, 'type': 'URL_UPDATED'}
            ).execute()
            results.append(f"Indexing request for {url_to_index}: {result}")
        except Exception as e:
            results.append(f"Error submitting indexing request for {url_to_index}: {str(e)}")

    return results

# Your existing code for obtaining credentials from a JSON key
def get_credentials(json_key_data):
    try:
        credentials = service_account.Credentials.from_service_account_file(
            json_key_data,
            scopes=['https://www.googleapis.com/auth/indexing']
        )
        return credentials
    except Exception as e:
        return None



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    
    input_urls = request.form.get('urls')

    #urls_to_check = request.form.get('urls').split('\n')
    
    urls_to_check = [url.strip() for url in input_urls.split('\n') if url.strip()]


    warning = None
    if len(urls_to_check) > 15:
        warning = 'You can only check up to 15 URLs. The excess URLs will be ignored.'


    def check_indexing_status(url):
        search_url = f'https://www.google.fr/search?q=site:{url}'
        response = requests.get(search_url)
        print("this is the response: "+response.text)

        if 'Aucun document ne correspond aux termes de recherche spécifiés' in response.text or 'Make sure all words are spelled correctly' in response.text:
            return f'{url} is not indexed.'
        else:
            return f'{url} is indexed.'

    results = []
    for i, url in enumerate(urls_to_check):
        if i >= 15:
            break
        status = check_indexing_status(url)
        results.append((status))
        time.sleep(3)
    
    response_data = {
        'results': results,
        'warning': warning  
    }

    #xlsx_file = export_results_to_xlsx(results)

    return jsonify(response_data)


@app.route('/submit-urls', methods=['GET','POST'])
def submit_to_index():

    if request.method == 'GET':
        return render_template('submit_urls.html')


    if request.method == 'POST':
        urls_to_index = request.form.get('urls').split('\n')
        json_key_content = request.form.get('json_key')  

        if not json_key_content:
            return jsonify(error="No JSON key content provided.")

        try:
            json_key_data = json.loads(json_key_content)
        except ValueError:
            return jsonify(error="Invalid JSON key content. Please check the formatting.")

        #credentials = get_credentials(json_key_data)

        try:
            credentials = service_account.Credentials.from_service_account_info(
            json_key_data,
            scopes=['https://www.googleapis.com/auth/indexing']
        )
            results = index_urls(urls_to_index, credentials)
            return jsonify(results=results)
    
        except Exception as e:
            return jsonify(error=f"Failed to obtain credentials from the provided JSON key: {str(e)}")


    return jsonify(error="An unknown error occurred.")

@app.route('/sitemap-extractor', methods=['GET', 'POST'])
def sitemap_extractor():
    if request.method == 'POST':
        sitemap_url = request.form.get('sitemap_url')
        urls = extract_urls_from_sitemap(sitemap_url)
        return jsonify({'urls': urls})
    return render_template('sitemap-extractor.html')

def extract_urls_from_sitemap(sitemap_url):
    try:
        response = requests.get(sitemap_url)
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            urls = [child.text for child in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
            return urls
    except Exception as e:
        return []
    return []




def export_results_to_xlsx(results):
    df = pd.DataFrame(results, columns=["URL", "Status"])
    output = "check_index_results.xlsx"

    df.to_excel(output, index=False)

    return output


# Function to check backlinks
def check_backlinks(input_url):
    try:
        search_url = f"https://www.google.com/search?q=link:{input_url}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all("cite")
            backlinks = [result.get_text() for result in results]
            return backlinks
        else:
            return None
    except Exception as e:
        return None




if __name__ == '__main__':
    app.run(debug=False)
    # input_url = input("Enter a URL to check backlinks: ")
    # backlinks = check_backlinks(input_url)

    # if backlinks:
    #     print("Backlinks:")
    #     for link in backlinks:
    #         print(link)
    # else:
    #     print("No backlinks found.")

