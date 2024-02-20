import json
import mysql.connector
import pymongo
from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://projectwork:SpeSana@cluster0.ajv3ccw.mongodb.net/")
db = client["SpeSana"]
products = db["Products"]
# print(db)

@app.route("/")
def homepage():

    return render_template("provaCard2.html")

@app.route("/product")
def product():
    prodotti = list(products.find({"brands": "Ferrero"}))

    return render_template("product.html", prodotti=prodotti)

if __name__ == '__main__':
    app.run(debug=True)