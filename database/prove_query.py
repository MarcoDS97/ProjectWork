from pymongo import MongoClient

client = MongoClient("mongodb+srv://projectwork:SpeSana@cluster0.ajv3ccw.mongodb.net/")
db = client['SpeSana']
prodotti = db['Products']
risultato = prodotti.find({"nutriscore_grade": 'a'}).sort("nutriscore_score")
collection = db["Nutriscore a"]
if "Nutriscore a" in db.list_collection_names():
    collection.drop()
collection.insert_many(risultato)
risultato = prodotti.find({"nutriscore_grade": 'e'}).sort("nutriscore_score")
collection = db["Nutriscore e"]
if "Nutriscore e" in db.list_collection_names():
    collection.drop()
collection.insert_many(risultato)

# category = "Snacks"
# # Query per cercare i prodotti di una certa categoria
# products_in_category = list(prodotti.find({"categories": "Snacks"}))
#
#
# # Stampa dei prodotti trovati
# print("Prodotti nella categoria", category)
# for product in products_in_category[:10]:
#     print(product["product_name"])
