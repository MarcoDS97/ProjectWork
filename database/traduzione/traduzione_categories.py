import pymongo
import deepl
import json
import csv


client = pymongo.MongoClient("mongodb+srv://projectwork:SpeSana@cluster0.ajv3ccw.mongodb.net/")
db = client["SpeSana"]
products = db["Products"]

dati = products.find({}, {"_id": 0, "categories": 1})
# Ci sono 177614 categorie in totale, come set sono 8466, ci sono 15487 prodotti senza categoria
categories = {}

for array in dati:
    try:
        for cat in array['categories']:
            clean = cat
            if cat in categories.keys():
                continue
            if ":" in cat:
                clean = clean.split(":")[1].strip()
            if "." in cat:
                clean = clean.split(".")[1].strip()
            if "-" in cat:
                clean = clean.replace("-", " ").strip()

            categories[cat] = clean
    except:
        pass

key = "" #Key DeepL
translator = deepl.Translator(key)
usage = translator.get_usage()

for orig, clean in categories.items():
    trad = translator.translate_text(clean, target_lang="IT")
    categories[orig] = str(trad.text)
    if usage.character.count > (usage.character.limit * 0.98):
        print("98%")
        break

with open("test1.json", "w", encoding="utf-8") as filejson:
    json.dump(categories, filejson)

with open("test11.csv", "w", encoding="utf-8", newline="") as file:
    header = ["original", "translate"]
    writer = csv.writer(file)
    writer.writerow(header)
    for elem in categories.items():
        writer.writerow(elem)