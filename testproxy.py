import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit

# Function to extract inner pages from Google search results
def extract_inner_pages(domain):
    search_url = f"https://www.google.com/search?q=site:{domain}"
    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("div", class_="Gx5Zad")
        inner_pages = [result.find("a")["href"] for result in results]
        return inner_pages
    return []

# Function to check indexing status for a list of URLs
def check_indexing_status(urls_to_check, inner_pages):
    indexed_urls = []
    for url in urls_to_check:
        if any(url in inner_page for inner_page in inner_pages):
            indexed_urls.append(url)
    return indexed_urls

# List of URLs to check indexing status
urls_to_check = [
    "https://www.gtoenergies.fr/prestations/",
    "https://www.gtoenergies.fr/bornes-de-recharge-rennes/",
    "https://www.gtoenergies.fr/res"
]

# Main domain to search for
main_domain = "www.gtoenergies.fr"
inner_pages = extract_inner_pages(main_domain)
indexed_urls = check_indexing_status(urls_to_check, inner_pages)

print("Indexed URLs:")
for url in indexed_urls:
    print(url)
