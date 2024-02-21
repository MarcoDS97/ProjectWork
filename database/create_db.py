import pandas as pd
from pymongo import MongoClient
from bing_image_urls import bing_image_urls

percorso = r"csv\prodotti.csv"
df1 = pd.read_csv(percorso, delimiter=';')
percorso = r"csv\utenti.csv"
df2 = pd.read_csv(percorso, delimiter=',')

client = MongoClient("mongodb+srv://projectwork:SpeSana@cluster0.ajv3ccw.mongodb.net/")
db = client['SpeSana']
collection = db['Products']
data1 = df1.to_dict(orient='records')
for e in data1:
    categories = e["categories"]
    if isinstance(categories, str):
        list_categories = categories.split(",")
        e["categories"] = [e.strip() for e in list_categories]
    list_numbers = {"energy-kcal_100g", "fat_100g", "saturated-fat_100g", "carbohydrates_100g", "sugars_100g",
                    "fiber_100g", "proteins_100g", "salt_100g", "sodium_100g"}
    for string in list_numbers:
        numero_stringa = e[string]
        if isinstance(numero_stringa, str):
            numero_float = round(float(numero_stringa.replace(",", ".")), 2)
            e[string] = numero_float
    # if isinstance(e["image_url"], float):
    #     e["image_url"] = bing_image_urls(e["product_name"], limit=1)[0]
if "Products" in db.list_collection_names():
    collection.drop()
collection.insert_many(data1)

# collection = db['Users']
# data2 = df2.to_dict(orient='records')
# for e in data2:
#     favorites = e["Favorites"]
#     if isinstance(favorites, str):
#         list_favorites = favorites.split(",")
#         e["Favorites"] = [e.strip() for e in list_favorites]
# if "Users" in db.list_collection_names():
#     collection.drop()
# collection.insert_many(data2)
