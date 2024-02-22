import pandas as pd
from pymongo import MongoClient

percorso = r"csv\prodotti.csv"
df1 = pd.read_csv(percorso, delimiter=';')
percorso = r"csv\utenti.csv"
df2 = pd.read_csv(percorso, delimiter=',')
percorso = r"csv\traduzione_categories.csv"
df3 = pd.read_csv(percorso, delimiter=',')

client = MongoClient("mongodb+srv://projectwork:daita12@cluster0.ajv3ccw.mongodb.net/")
db = client['SpeSana']
collection = db['Products']
data1 = df1.to_dict(orient='records')
diz = df3.to_dict(orient='records')
for e in data1:
    if isinstance(e["categories"], str):
        categories = e["categories"]
        categories = categories.split(",")
        categories = [elem.strip() for elem in categories]
        for i, a in enumerate(categories):
            for f in diz:
                if f['original'] == a:
                    categories[i] = f["translate"]
        e['categories'] = categories
    list_numbers = {"energy-kcal_100g", "fat_100g", "saturated-fat_100g", "carbohydrates_100g", "sugars_100g",
                    "fiber_100g", "proteins_100g", "salt_100g", "sodium_100g"}
    for string in list_numbers:
        numero_stringa = e[string]
        if isinstance(numero_stringa, str):
            numero_float = round(float(numero_stringa.replace(",", ".")), 2)
            e[string] = numero_float
    if isinstance(e["image_url"], float):
        e["image_url"] = "static/imgTest/img-not-found.jpg"
if "Products" in db.list_collection_names():
    collection.drop()
collection.insert_many(data1)

collection = db['Users']
data2 = df2.to_dict(orient='records')
for e in data2:
    favorites = e["Favorites"]
    if isinstance(favorites, str):
        list_favorites = favorites.split(",")
        e["Favorites"] = [e.strip() for e in list_favorites]
if "Users" in db.list_collection_names():
    collection.drop()
collection.insert_many(data2)
