# from pymongo import MongoClient
# import pandas as pd
#
# client = MongoClient("mongodb+srv://projectwork:daita12@cluster0.hqm86xs.mongodb.net/")
# db = client['SpeSana']
# prodotti = db['Products']
# parola_cercata = "spaghetti"
# risultato = list(prodotti.find({"categories": {"$regex": f".*{parola_cercata}.*", "$options": "i"}}).sort("unique_scans_n", -1))
#
# for e in risultato:
#     print(e)

from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb+srv://projectwork:daita12@cluster0.hqm86xs.mongodb.net/")
db = client['SpeSana']
utenti = db['Users']

# parola_cercata = "nutella"
# risultato = list(prodotti.find({"product_name": {"$regex": f".*{parola_cercata}.*", "$options": "i"}}).sort("unique_scans_n", -1))
# print(risultato)
# print(len(risultato))
new_field = "recipes"
default_value = []

# Aggiornamento dei documenti nella collezione per aggiungere il nuovo campo con il valore predefinito
utenti.update_many(
    {},
    {"$set": {new_field: default_value}},
    upsert=True
)
new_field = "products_favorites"
default_value = []
utenti.update_many(
    {},
    {"$set": {new_field: default_value}},
    upsert=True
)
# risultato = utenti.find({})
#
# utenti = pd.DataFrame(risultato)


# risultato = prodotti.find({"categories": "Prodotti spalmabili"}).sort("unique_scans_n", -1).limit(10)
# for e in risultato:
#     print(e)
# category = "Snacks"
# # Query per cercare i prodotti di una certa categoria
# products_in_category = list(prodotti.find({"categories": "Snacks"}))
#
#
# # Stampa dei prodotti trovati
# print("Prodotti nella categoria", category)
# for product in products_in_category[:10]:
#     print(product["product_name"])


