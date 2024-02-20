import pandas as pd
from pymongo import MongoClient

percorso = r"csv\prodotti_in_pulizia.csv"
df1 = pd.read_csv(percorso, delimiter=';')
percorso = r"csv\utenti.csv"
df2 = pd.read_csv(percorso, delimiter=',')

client = MongoClient("mongodb+srv://projectwork:SpeSana@cluster0.ajv3ccw.mongodb.net/")
db = client['SpeSana']
# collection = db['Products']
# data1 = df1.to_dict(orient='records')
# for e in data1:
#     categories = e["categories"]
#     if isinstance(categories, str):
#         list_categories = categories.split(",")
#         e["categories"] = [e.strip() for e in list_categories]
# collection.insert_many(data1)
# print(collection)
# collection = db['Users']
# data2 = df2.to_dict(orient='records')
# collection.insert_many(data2)

prodotti = db['Products']
category = "Snacks"
# Query per cercare i prodotti di una certa categoria
products_in_category = list(prodotti.find({"categories": "Snacks"}))


# Stampa dei prodotti trovati
print("Prodotti nella categoria", category)
for product in products_in_category[:10]:
    print(product["product_name"])
