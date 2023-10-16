import requests
import time


urls_to_check = [
    'https://www.rstronic-angers.com/',
    'https://www.rstronic-angers.com/boitier-ethanol-cholet-saumur-segre/',
    'https://www.rstronic-angers.com/reprogrammation-moteur-preparation-autos-motos-trucks-engins-agricoles/',
    'https://www.rstronic-angers.com/feed/',
    'https://www.nature-source.fr/les-superaliments-bio-puisez-dans-la-nature-pour-renforcer-votre-sante/',
]

def check_indexing_status(url):
    search_url = f'https://www.google.com/search?q=site:{url}'
    response = requests.get(search_url)

    if 'Aucun document ne correspond aux termes de recherche spécifiés' in response.text:
        return f"{url} is not indexed."
    else:
        return f"{url} is indexed."

for url in urls_to_check:
    status = check_indexing_status(url)
    print(status)
    time.sleep(3)
