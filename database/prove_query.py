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
prodotti = db['Products']

pipeline = [
    {"$match": {"nutriscore_grade": "e", "unique_scans_n": {"$gte": 100}}},
    {"$sort": {"nutriscore_score": -1}},
    {"$group": {"_id": "$product_name", "doc": {"$first": "$$ROOT"}}},
    {"$replaceRoot": {"newRoot": "$doc"}},
    {"$limit": 20}
]

risultati = list(prodotti.aggregate(pipeline))

nutriscore_e = pd.DataFrame(risultati)

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



