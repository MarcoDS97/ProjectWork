from pymongo import MongoClient

client = MongoClient("mongodb+srv://projectwork:daita12@cluster0.hqm86xs.mongodb.net/")
db = client['SpeSana']
prodotti = db['Users']
# risultato = prodotti.find({"nutriscore_grade": 'a'}).sort("nutriscore_score")
# collection = db["Nutriscore a"]
# if "Nutriscore a" in db.list_collection_names():
#     collection.drop()
# collection.insert_many(risultato)
# risultato = prodotti.find({"nutriscore_grade": 'e'}).sort("nutriscore_score")
# collection = db["Nutriscore e"]
# if "Nutriscore e" in db.list_collection_names():
#     collection.drop()
# collection.insert_many(risultato)

risultato = prodotti.find({"categories": "Prodotti spalmabili"}).sort("unique_scans_n", -1).limit(10)
for e in risultato:
    print(e)
# category = "Snacks"
# # Query per cercare i prodotti di una certa categoria
# products_in_category = list(prodotti.find({"categories": "Snacks"}))
#
#
# # Stampa dei prodotti trovati
# print("Prodotti nella categoria", category)
# for product in products_in_category[:10]:
#     print(product["product_name"])
