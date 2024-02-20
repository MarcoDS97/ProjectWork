import requests
from bs4 import BeautifulSoup
from imagesoup import ImageSoup

search_term = 'cane'
url = rf'https://www.google.no/search?q={search_term}&client=opera&hs=cTQ&source=lnms&tbm=isch&sa=X&safe=active&ved=0ahUKEwig3LOx4PzKAhWGFywKHZyZAAgQ_AUIBygB&biw=1920&bih=982&isz=l'
page = requests.get(url).text
soup = BeautifulSoup(page, 'html.parser')
thumbnails = []
print(soup.find_all('img'))
for raw_img in soup.find_all('img'):
    link = raw_img.get('src')

    if link and link.startswith("https://"):
        thumbnails.append(link)
        pass
    pass
print(thumbnails[1])
#
#
# soup = ImageSoup()
# images = soup.search('"Arya Stark"', n_images=10)
# arya = images[0]
# print(arya)

API_KEY = '42473691-dc0497f70d00de95d925c0bea'
BASE_URL = 'https://pixabay.com/api/'
query = input("Inserisci le parole chiave per la ricerca di immagini: ")

params = {
    'key': API_KEY,
    'q': query,
    'image_type': 'photo',  # Puoi impostare anche 'illustration', 'vector', etc.
    'per_page': 10  # Numero di immagini da ottenere
}

response = requests.get(BASE_URL, params=params)

data = response.json()

if data['totalHits'] > 0:
    for image in data['hits']:
        print(image['webformatURL'])
else:
    print("Nessuna immagine trovata per le parole chiave inserite.")
