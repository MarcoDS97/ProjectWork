import requests
from bs4 import BeautifulSoup


def trova_url_immagini(query):
    url = rf"https://www.google.com/search?q={query}&tbm=isch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    urls = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if src:
            urls.append(src)

    return urls


# Esempio di utilizzo
query = "cane"
urls = trova_url_immagini(query)
for url in urls:
    print(url)

# API_KEY = '42473691-dc0497f70d00de95d925c0bea'
# BASE_URL = 'https://pixabay.com/api/'
# query = input("Inserisci le parole chiave per la ricerca di immagini: ")
#
# params = {
#     'key': API_KEY,
#     'q': query,
#     'image_type': 'photo',  # Puoi impostare anche 'illustration', 'vector', etc.
#     'per_page': 10  # Numero di immagini da ottenere
# }
#
# response = requests.get(BASE_URL, params=params)
#
# data = response.json()
#
# if data['totalHits'] > 0:
#     for image in data['hits']:
#         print(image['webformatURL'])
# else:
#     print("Nessuna immagine trovata per le parole chiave inserite.")
