from pymongo import MongoClient


client = MongoClient("mongodb+srv://projectwork:SpeSana@cluster0.ajv3ccw.mongodb.net/")
db = client['SpeSana']
prodotti = db['Products']
category = "Snacks"
# Query per cercare i prodotti di una certa categoria
products_in_category = list(prodotti.find({"categories": "Snacks"}))


# Stampa dei prodotti trovati
print("Prodotti nella categoria", category)
for product in products_in_category[:10]:
    print(product["product_name"])